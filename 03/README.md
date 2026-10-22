# PRAKTIKUM MINGGU 03

Nama : Dwi Ismi Andriani <br>
Nim : 255410012 <br>
Kelas : Informatika - 1 <br>

Laporan praktikum ke - 03 <br>
Topik : Sinkronisasi Pada Sistem Terdistribusi <br>

# TUJUAN

1. Memahami konsep sinkronisasi waktu dan penerapan protokol NTP dalam sistem terdistribusi.
2. Memahami penggunaan Vector Clock untuk menentukan urutan kejadian (event) dalam sistem terdistribusi.
3. Memahami permasalahan race condition dan deadlock serta cara mencegahnya menggunakan mekanisme sinkronisasi.
4. Memahami cara kerja algoritma Raft dalam proses pemilihan koordinator (leader).
5. Mampu menjalankan, menganalisis, dan mengembangkan program Python terkait sinkronisasi pada sistem terdistribusi.

# DASAR TEORI

Sistem terdistribusi merupakan sistem yang terdiri dari beberapa komputer atau proses yang saling berkomunikasi untuk menjalankan tugas. Dalam sistem ini, sinkronisasi diperlukan agar proses dapat berjalan dengan teratur dan masalah akibat pelaksanaan tugas secara bersamaan dapat ditangani.<br>

Sinkronisasi waktu merupakan proses penyesuaian waktu antarkomputer menggunakan protokol seperti Network Time Protocol (NTP) dan Precision Time Protocol (PTP). Sinkronisasi ini membantu menjaga konsistensi waktu dalam komunikasi antarkomputer.<br>

Vector Clock adalah mekanisme pencatatan waktu logis yang digunakan untuk mengetahui hubungan urutan kejadian dalam sistem terdistribusi. Vector Clock memperbarui nilai penghitung berdasarkan kejadian yang berlangsung dan pesan yang diterima antarproses.<br>

Race condition terjadi ketika beberapa proses mengakses atau mengubah data bersama secara bersamaan sehingga hasilnya dapat berbeda bergantung pada urutan eksekusi. Sementara itu, deadlock merupakan kondisi ketika beberapa proses saling menunggu sumber daya sehingga tidak dapat melanjutkan eksekusi. Kedua masalah tersebut dapat ditangani melalui penerapan mekanisme sinkronisasi yang tepat.<br>

Algoritma Raft merupakan algoritma konsensus yang digunakan untuk membantu sejumlah node mencapai kesepakatan, termasuk dalam pemilihan pemimpin (leader). Dalam proses pemilihan, node dapat berperan sebagai follower, candidate, atau leader sesuai dengan kondisi dan hasil pemungutan suara.<br>

Melalui praktikum ini, konsep sinkronisasi waktu, Vector Clock, race condition, deadlock, dan algoritma Raft dipelajari melalui pelaksanaan program Python, pengamatan output, serta pembuatan modul dan simulasi sederhana.<br>

# PRAKTIK
## 3.1 Sinkronisasi Waktu

1. # Menginstall NetTime (Windows)<br>

   <img width="371" height="278" alt="image" src="https://github.com/user-attachments/assets/171ec544-15ca-489c-97d4-48ce0299a16a" /> <br>

2. Menjelaskan proses sinkronisasi tersebut <br>
   <img width="368" height="278" alt="image" src="https://github.com/user-attachments/assets/ed45219d-3cf8-4645-b63b-7be6a7c0dcaa" /> <br>

   Setelah mengistal, tekan tombol next sampai ke tombol install <br>
   <img width="367" height="279" alt="image" src="https://github.com/user-attachments/assets/89523c29-7308-432c-a8ae-4ea2ff89e5bb" /> <br>

   Setelah sellesai seperti gambar disini, NetTime berarti sudah terinstall <br>
   <img width="370" height="278" alt="image" src="https://github.com/user-attachments/assets/36c148dd-45f5-446d-9f86-7907ca81480d" /> <br>

<img src="images/01_Network_Time.png" width="700">

Klik Start untuk menghidupkan

<img src="images/02_Network_Time.png" width="700">

## 3.2 Vector Clock
1. Jalankan program tersebut, amati keluaran nya
class VectorClock:

```
    def __init__(self, num_processes, process_id):
        self.clocks = [0] * num_processes  # Initialize all clocks to zero
        self.process_id = process_id      # The ID of the current process

    def increment(self):
        """Increments the local clock for the current process."""
        self.clocks[self.process_id] += 1

    def send_message(self):
        """Prepares the vector clock for sending with a message."""
        self.increment()  # Increment local clock before sending
        return list(self.clocks) # Return a copy of the current vector clock

    def receive_message(self, received_clocks):
        """Updates the vector clock upon receiving a message."""
        for i in range(len(self.clocks)):
            self.clocks[i] = max(self.clocks[i], received_clocks[i])
        self.increment()  # Increment local clock after receiving and merging

    def __str__(self):
        return f"P{self.process_id}: {self.clocks}"

    def happens_before(self, other_vector_clock):
        """
        Determines if this vector clock happens before another.
        A happens before B if all elements in A are less than or equal to
        the corresponding elements in B, and at least one element in A is
        strictly less than the corresponding element in B.
        """
        if self.clocks == other_vector_clock.clocks:
            return False  # Same clocks, not "happens before"

        all_le = True  # All elements are less than or equal
        any_lt = False # At least one element is strictly less than

        for i in range(len(self.clocks)):
            if self.clocks[i] > other_vector_clock.clocks[i]:
                return False # Not "happens before" if any element is greater

            if self.clocks[i] < other_vector_clock.clocks[i]:
                any_lt = True

        return all_le and any_lt

    def is_concurrent(self, other_vector_clock):
        """
        Determines if two vector clocks are concurrent.
        Two events are concurrent if neither happens before the other.
        """
        return not (self.happens_before(other_vector_clock) or
                    other_vector_clock.happens_before(self))
```

Output:<br>
<img src="images/03_Vector_Clock.png" width="700">

2. Buat modul Python untuk class VectorClock tersebut dan buatlah contoh cara menggunakan modul tersebut

Buat Folder **"Modul Vclock"**<br>
<img src="images/04_Modul.png" width="700"><br>

Kemudian masukkan file **"vclocks.py"**<br>
<img src="images/06_vclocks.png" width="700"><br>

Masukkan terminal untuk vclocks<br>
<img src="images/07_vclocks.png" width="700"><br>

Kemudian masukkan lagi file **"Main.py"**<br>
<img src="images/08_Main.png" width="700"><br>

Masukkan terminal untuk Main<br>
<img src="images/09_Main.png" width="700"><br>
<img src="images/10_Main.png" width="700"><br>

Menambahkan file raft_Module.py dan simulasi_raft.py <br>
<img src="images/11_Main.png" width="700"><br>

## 3.3 Problem Tanpa Sinkronisasi
