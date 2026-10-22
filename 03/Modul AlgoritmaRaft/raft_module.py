import random
import time
from enum import Enum
from typing import List, Optional

class State(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3

class RaftNode:
    def __init__(self, node_id: int, all_nodes: List[int]):
        self.id = node_id
        self.nodes = all_nodes
        self.state = State.FOLLOWER
        self.current_term = 0
        self.voted_for: Optional[int] = None
        self.log: List[str] = []
        self.commit_index = 0
        self.last_heartbeat = time.time()
        self.election_timeout = self._random_timeout()

    def _random_timeout(self) -> float:
        return time.time() + random.uniform(1.0, 2.0)

    def on_heartbeat(self, term: int):
        if term >= self.current_term:
            self.current_term = term
            self.state = State.FOLLOWER
            self.voted_for = None
            self.last_heartbeat = time.time()
            self.election_timeout = self._random_timeout()

    def start_election(self):
        self.current_term += 1
        self.state = State.CANDIDATE
        self.voted_for = self.id
        votes = 1  # Memberikan suara untuk diri sendiri

        for node_id in self.nodes:
            if node_id == self.id:
                continue
            votes += 1  # Penyederhanaan: mengasumsikan semua node memberikan suara

        if votes > len(self.nodes) // 2:
            self.state = State.LEADER
            print(f"--> Node {self.id} terpilih menjadi LEADER pada term {self.current_term}")

    def append_entry(self, entry: str):
        if self.state == State.LEADER:
            self.log.append(entry)
            print(f"--> Leader ({self.id}) menembahkan log: {entry}")
            self.commit_index = len(self.log) - 1

    def tick(self):
        now = time.time()
        if self.state == State.LEADER:
            pass
        elif now > self.election_timeout:
            self.start_election()
        elif self.state == State.FOLLOWER and now - self.last_heartbeat > 2.0:
            self.election_timeout = self._random_timeout()
            self.start_election()

def run_simulation(steps: int = 15):
    node_ids = [1, 2, 3]
    nodes = [RaftNode(i, node_ids) for i in node_ids]

    for step in range(steps):
        time.sleep(0.5)
        print(f"\n--- Step {step + 1} ---")

        leaders = [n for n in nodes if n.state == State.LEADER]
        if leaders:
            leader = random.choice(leaders)
            for node in nodes:
                if node.id != leader.id:
                    node.on_heartbeat(leader.current_term)

            if step % 5 == 0:
                leader.append_entry(f"command-{step}")

        for node in nodes:
            node.tick()

        for node in nodes:
            print(f"Node {node.id}: {node.state.name} | Term: {node.current_term} | Log Len: {len(node.log)}")