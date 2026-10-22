# Mengimpor class VectorClock dari modul vclocks.py
from vclocks import VectorClock

# --- Simulasi Sistem dengan 3 Proses ---
num_processes = 3

# Inisialisasi tiap proses
p0 = VectorClock(num_processes=num_processes, process_id=0)
p1 = VectorClock(num_processes=num_processes, process_id=1)
p2 = VectorClock(num_processes=num_processes, process_id=2)

print("=== Inisialisasi Clock ===")
print(p0)  # P0: [0, 0, 0]
print(p1)  # P1: [0, 0, 0]
print(p2)  # P2: [0, 0, 0]

print("\n=== Event 1: P0 Melakukan Local Event ===")
p0.increment()
print(p0)  # P0: [1, 0, 0]

print("\n=== Event 2: P0 Mengirim Pesan ke P1 ===")
msg_from_p0 = p0.send_message()  # P0 increment clock-nya sebelum kirim
p1.receive_message(msg_from_p0)  # P1 update max clock lalu increment
print(f"Pesan dari P0: {msg_from_p0}")
print(p0)  # P0: [2, 0, 0]
print(p1)  # P1: [2, 1, 0]

print("\n=== Event 3: P2 Melakukan Local Event ===")
p2.increment()
print(p2)  # P2: [0, 0, 1]

print("\n=== Event 4: P1 Mengirim Pesan ke P2 ===")
msg_from_p1 = p1.send_message()
p2.receive_message(msg_from_p1)
print(f"Pesan dari P1: {msg_from_p1}")
print(p1)  # P1: [2, 2, 0]
print(p2)  # P2: [2, 2, 2]

print("\n=== Cek Hubungan Kausalitas (Causality) ===")
print(f"Apakah P0 happens-before P1? {p0.happens_before(p1)}")
print(f"Apakah P1 happens-before P0? {p1.happens_before(p0)}")
print(f"Apakah P0 concurrent dengan P2?     {p0.is_concurrent(p2)}")