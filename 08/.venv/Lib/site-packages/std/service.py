"""Async lifecycle primitives for application and background services."""

from __future__ import annotations

import asyncio
import logging
import math
from abc import ABC, abstractmethod
from enum import StrEnum
from types import TracebackType
from typing import Protocol, runtime_checkable

logger = logging.getLogger(__name__)


class ServiceState(StrEnum):
    """Lifecycle states shared by service implementations."""

    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"

    def __str__(self) -> str:
        """Return the serialized state value."""
        return self.value


@runtime_checkable
class BackgroundServiceProtocol(Protocol):
    """Structural interface for objects that can be managed as services."""

    @property
    def state(self) -> ServiceState:
        """Return the current lifecycle state."""

    async def start(self) -> None:
        """Start the service."""

    async def stop(self) -> None:
        """Stop the service and release its resources."""

    async def is_healthy(self) -> bool:
        """Return whether the service is running and healthy."""


class Service(ABC):
    """Base class for an asynchronously managed application service.

    Implement :meth:`_start` and :meth:`_stop` to acquire and release resources.
    The public lifecycle is serialized, repeated starts while running and stops
    while idle or stopped are safe, and a failed service can be stopped to
    release resources before it is started again.
    """

    def __init__(self, name: str | None = None) -> None:
        """Create a service, defaulting its name to the concrete class name."""
        self._name = name or type(self).__name__
        self._state = ServiceState.IDLE
        self._lifecycle_lock = asyncio.Lock()

    @property
    def name(self) -> str:
        """Return the service's diagnostic name."""
        return self._name

    @property
    def state(self) -> ServiceState:
        """Return the current lifecycle state."""
        return self._state

    async def start(self) -> None:
        """Initialize resources and move the service to ``running``.

        Starting a running service is idempotent. If initialization raises,
        the service enters ``failed`` and the original exception is re-raised.
        Call :meth:`stop` before retrying so partially initialized resources
        can be released.
        """
        async with self._lifecycle_lock:
            if self._state is ServiceState.RUNNING:
                logger.debug("Service %s is already running", self._name)
                return
            if self._state not in (ServiceState.IDLE, ServiceState.STOPPED):
                raise RuntimeError(f"Cannot start service {self._name!r} in state {self._state}")

            self._state = ServiceState.STARTING
            logger.info("Starting service %s", self._name)
            try:
                await self._start()
            except BaseException:
                self._state = ServiceState.FAILED
                logger.exception("Failed to start service %s", self._name)
                raise
            self._state = ServiceState.RUNNING
            logger.info("Started service %s", self._name)

    async def stop(self) -> None:
        """Release service resources and move to ``stopped``.

        Stopping an idle or already stopped service is idempotent. A failed
        service may also be stopped, allowing implementations to clean up
        resources acquired before an error.
        """
        async with self._lifecycle_lock:
            if self._state in (ServiceState.IDLE, ServiceState.STOPPED):
                logger.debug("Service %s is already stopped", self._name)
                return
            if self._state not in (ServiceState.RUNNING, ServiceState.FAILED):
                raise RuntimeError(f"Cannot stop service {self._name!r} in state {self._state}")

            self._state = ServiceState.STOPPING
            logger.info("Stopping service %s", self._name)
            try:
                await self._stop()
            except BaseException:
                self._state = ServiceState.FAILED
                logger.exception("Failed to stop service %s", self._name)
                raise
            self._state = ServiceState.STOPPED
            logger.info("Stopped service %s", self._name)

    async def is_healthy(self) -> bool:
        """Return false unless running; convert health-check errors to false."""
        if self._state is not ServiceState.RUNNING:
            return False
        try:
            return await self._health_check()
        except Exception:
            logger.exception("Health check failed for service %s", self._name)
            return False

    async def __aenter__(self) -> Service:
        """Start the service when entering an async context."""
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Stop the service when leaving an async context."""
        await self.stop()

    @abstractmethod
    async def _start(self) -> None:
        """Acquire resources required while this service is running."""

    @abstractmethod
    async def _stop(self) -> None:
        """Release resources acquired by :meth:`_start`."""

    async def _health_check(self) -> bool:
        """Check health; override when the service has a meaningful probe."""
        return True


class BackgroundServiceError(RuntimeError):
    """Raised by :meth:`BackgroundService.wait` after its worker fails."""


class BackgroundService(Service, ABC):
    """A service that runs a long-lived coroutine in a managed task.

    Implement :meth:`run` and check :attr:`stop_event` while waiting for work.
    Shutdown first signals the event, then waits for ``shutdown_timeout``. If
    the worker does not exit, it is cancelled and given one further timeout to
    finish cancellation cleanup. A worker that exits before shutdown is marked
    failed; inspect :attr:`failure` or await :meth:`wait` for the cause.
    """

    def __init__(self, name: str | None = None, *, shutdown_timeout: float | None = 30.0) -> None:
        """Create a background service with an optional graceful-stop timeout."""
        super().__init__(name)
        if shutdown_timeout is not None and (
            not math.isfinite(shutdown_timeout) or shutdown_timeout < 0
        ):
            raise ValueError("shutdown_timeout must be finite and non-negative, or None")
        self._shutdown_timeout = shutdown_timeout
        self._stop_event = asyncio.Event()
        self._worker_task: asyncio.Task[None] | None = None
        self._failure: Exception | None = None

    @property
    def stop_event(self) -> asyncio.Event:
        """Return the event signaled before graceful shutdown begins."""
        return self._stop_event

    @property
    def failure(self) -> Exception | None:
        """Return the worker exception, or ``None`` while it has not failed."""
        return self._failure

    async def wait(self) -> None:
        """Wait for the worker to finish and raise if it exited unexpectedly."""
        task = self._worker_task
        if task is not None:
            await asyncio.shield(task)
        if self._failure is not None:
            raise BackgroundServiceError(
                f"Background service {self.name!r} failed"
            ) from self._failure

    async def _start(self) -> None:
        if self._worker_task is not None and not self._worker_task.done():
            raise RuntimeError(f"Background service {self.name!r} still has a worker task")
        self._stop_event = asyncio.Event()
        self._failure = None
        self._worker_task = asyncio.create_task(self._run_worker(), name=f"{self.name}.background")

    async def _stop(self) -> None:
        self._stop_event.set()
        task = self._worker_task
        if task is None:
            return
        if not task.done():
            _, pending = await asyncio.wait({task}, timeout=self._shutdown_timeout)
            if pending:
                logger.warning(
                    "Background service %s did not stop gracefully; cancelling worker",
                    self.name,
                )
                task.cancel()
                _, pending = await asyncio.wait({task}, timeout=self._shutdown_timeout)
            if pending:
                raise TimeoutError(f"Background service {self.name!r} did not finish cancellation")
        task.result()
        self._worker_task = None

    async def _health_check(self) -> bool:
        task = self._worker_task
        return task is not None and not task.done() and self._failure is None

    async def _run_worker(self) -> None:
        try:
            await self.run()
        except asyncio.CancelledError as exc:
            if not self._stop_event.is_set():
                self._record_failure(
                    RuntimeError(f"Background service {self.name!r} was cancelled unexpectedly"),
                    cause=exc,
                )
        except Exception as exc:
            self._record_failure(exc)
        else:
            if not self._stop_event.is_set():
                self._record_failure(
                    RuntimeError(f"Background service {self.name!r} exited unexpectedly")
                )

    def _record_failure(self, failure: Exception, *, cause: BaseException | None = None) -> None:
        self._failure = failure
        if cause is not None:
            failure.__cause__ = cause
        if self._state in (ServiceState.RUNNING, ServiceState.STOPPING):
            self._state = ServiceState.FAILED
        logger.error(
            "Background service %s failed",
            self.name,
            exc_info=(type(failure), failure, failure.__traceback__),
        )

    @abstractmethod
    async def run(self) -> None:
        """Run until :attr:`stop_event` is set or work fails."""


__all__ = [
    "BackgroundService",
    "BackgroundServiceError",
    "BackgroundServiceProtocol",
    "Service",
    "ServiceState",
]
