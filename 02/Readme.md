# PRAKTIKUM MINGGU 02

Nama : Dwi Ismi Andriani<br>
Nim : 255410012<br>
Kelas : Informatika - 1<br>

Laporan praktikum minggu 02<br>
Topik : Komunikasi Antar Proses pada Sistem Terdistribusi<br>

# 1. Menampilkan proses yang ada pada komputer
<img width="571" height="473" alt="image" src="https://github.com/user-attachments/assets/6aa911ec-fda6-4381-8a94-11a46a03d6ff" />

## 2. Menjalankan salah satu aplikasi serta memperlihatkan prosesnya
## Langkah 1 — Buka Terminal
<img width="308" height="456" alt="image" src="https://github.com/user-attachments/assets/f9d075fc-50ee-4a2a-b826-89e2aab26b18" /><br>

## Langkah 2 — Jalankan aplikasi untuk diperiksa
<img width="145" height="30" alt="image" src="https://github.com/user-attachments/assets/31f16c87-6884-42e6-8c79-98045d0bb5eb" /><br>
<img width="444" height="360" alt="image" src="https://github.com/user-attachments/assets/8ca0e926-b3b5-4ec4-b8c4-2ad86a6c5646" 

## Langkah 3 — Perlihatkan proses dari aplikasi tersebut
<img width="251" height="68" alt="image" src="https://github.com/user-attachments/assets/f28ab67f-ac30-421b-ba89-6a935e687573" /><br>
Angka-angka di atas hanya contoh. Hasil pada laptopmu bisa berbeda. Kolom Id merupakan PID (Process ID), yaitu nomor identitas proses yang sedang berjalan.<br>
Jika ingin menampilkan informasi yang lebih jelas, gunakan:<br>

<img width="292" height="124" alt="image" src="https://github.com/user-attachments/assets/7708956f-cbab-43df-8e56-338ce277daf8" /> <br>

Pembahasan : Pada praktikum ini, dilakukan pemeriksaan proses aplikasi menggunakan Terminal PowerShell pada sistem operasi Windows. Perintah Get-Process digunakan untuk menampilkan daftar proses yang sedang berjalan pada komputer. Selanjutnya, perintah Start-Process notepad digunakan untuk menjalankan aplikasi Notepad. Setelah aplikasi terbuka, perintah Get-Process notepad digunakan untuk menampilkan informasi proses Notepad, seperti nama proses, ID proses (PID), dan penggunaan memori. Dengan demikian, dapat diketahui bahwa setiap aplikasi yang dijalankan memiliki proses yang dapat diperiksa melalui terminal.

## 3. Me-restart proses dan mematikan proses
## A. Mematikan proses aplikasi (Notepad)
## Langkah 1 — Jalankan Notepad
<img width="150" height="22" alt="image" src="https://github.com/user-attachments/assets/83dc48bb-7788-4322-b9b0-a26b3d0becdc" /><br>
<img width="358" height="325" alt="image" src="https://github.com/user-attachments/assets/d207ac5b-d5c0-44e1-b9a6-c4ce3a122862" /><br>

## Langkah 2 — Periksa PID Notepad
<img width="258" height="78" alt="image" src="https://github.com/user-attachments/assets/f338d249-a0c6-4837-a751-75f09cd7101b" />

## Langkah 3 — Matikan proses melalui terminal
<img width="379" height="72" alt="image" src="https://github.com/user-attachments/assets/e264052f-478f-45bd-99ea-378e365a434a" />

## Langkah 4 — Pastikan proses sudah mati
<img width="251" height="74" alt="image" src="https://github.com/user-attachments/assets/03f24ca3-2ca8-41fa-949c-c9b70e668a5f" />








