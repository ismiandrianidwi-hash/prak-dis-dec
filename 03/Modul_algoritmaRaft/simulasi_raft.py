# Mengimpor fungsi simulasi dari modul Raft
from raft_module import run_simulation

if __name__ == "__main__":
    print("=== SIMULASI KONSENSUS RAFT Sederhana ===")
    run_simulation(steps=15)