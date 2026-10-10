# PRAKTIKUM MINGGU 01
Nama  : Dwi Ismi Andriani<br>
Nim   : 255410012<br>
Kelas : Informatika - 1<br>
<br>Laporan praktikum minggu pertama<br>
Topik : Pengenalan git, instalansi github serta mengkonfigurasinya

# 1. PENDAHULUAN
## TUJUAN PRAKTIKUM
Tujuan dari praktikum ini adalah untuk memahami dan melakukan proses instalasi Git pada sistem operasi Windows, mengetahui cara memeriksa keberhasilan instalasi Git, serta memahami penggunaan dasar Git melalui Command Prompt atau Git Bash.

## DASAR TEORI
Git merupakan sistem kontrol versi (version control system) yang digunakan untuk mengelola dan mencatat perubahan pada file atau proyek. Git membantu pengguna menyimpan riwayat perubahan sehingga setiap versi dari suatu proyek dapat dikelola dengan lebih terstruktur.<br>
Git dapat digunakan melalui antarmuka grafis (GUI) maupun melalui Command Line Interface (CLI), seperti Git Bash, Command Prompt, dan PowerShell. Pada sistem operasi Windows, Git dapat diinstal menggunakan installer Git atau melalui perintah winget.<br>
Setelah Git berhasil diinstal, keberhasilan instalasi dapat diperiksa menggunakan perintah git --version. Jika terminal menampilkan nomor versi Git, maka Git telah berhasil terpasang dan siap digunakan. <br>
Dalam penggunaannya, Git memiliki beberapa perintah dasar seperti git init untuk membuat repository, git add untuk menambahkan perubahan ke staging area, git commit untuk menyimpan perubahan ke dalam riwayat Git, serta git push untuk mengirim perubahan ke repository online seperti GitHub.<br>

# 2. PRAKTIKUM
# INSTALANSI GIT
## 1. Instalansi Git
<img width="493" height="379" alt="Screenshot 2026-10-10 195011" src="https://github.com/user-attachments/assets/392e229f-4df1-4b28-a143-2864ff8a019b" /><br>
Pada gambar tersebut merupakan tahap awal proses instalasi Git versi 2.56.0.2 pada sistem operasi Windows. Pada tahap ini ditampilkan informasi mengenai GNU General Public License (GPL) yang digunakan oleh Git. Untuk melanjutkan proses instalasi, pengguna dapat membaca informasi lisensi kemudian menekan tombol Install. Tahap ini menunjukkan bahwa installer Git sudah siap untuk melakukan proses pemasangan ke komputer.

## 2. Pemilihan Komponen yang Akan Di Install
<img width="493" height="379" alt="image" src="https://github.com/user-attachments/assets/c6f4cb15-b254-40e7-9b8e-7b09637ea630" /><br>
Pembahasan : Pada tahap ini, pengguna memilih komponen tambahan yang akan diinstal bersama Git, seperti integrasi Git Bash Here dan asosiasi file. Pengaturan bawaan (default) sudah cukup optimal dan dapat langsung dilanjutkan ke tahap berikutnya.

## 3. Proses Installing
<img width="493" height="379" alt="image" src="https://github.com/user-attachments/assets/2a0fbda3-4de8-4b67-8bc7-2f9eb554f864" /><br>
Pembahasan : Pada tahap ini, sistem melakukan penyalinan dan pemasangan file-file utama Git ke dalam direktori komputer secara otomatis. Proses ini mencakup ekstraksi paket instalasi, konfigurasi komponen pendukung, serta pembuatan shortcut agar perangkat lunak siap digunakan.

## 4. Finish
<img width="491" height="380" alt="image" src="https://github.com/user-attachments/assets/45d7143c-94e6-4c57-8a90-761e79cf6929" /><br>
Pembahasan : Pada tahap ini, proses instalasi Git telah selesai.

## 5. Pemeriksaan Instalansi Git
<img width="170" height="113" alt="image" src="https://github.com/user-attachments/assets/0877af49-feb1-4362-a76d-323786291a21" /><br>
Pembahasan : Pada tahap pemeriksaan instalasi, dilakukan pengecekan untuk memastikan Git telah berhasil terpasang pada komputer. Pemeriksaan dilakukan melalui Git Bash dengan menjalankan perintah git --version. Hasil yang ditampilkan berupa versi Git yang terpasang, sehingga dapat disimpulkan bahwa Git telah berhasil diinstal dan siap digunakan.

## 4. Konfigurasi Git
<img width="341" height="174" alt="image" src="https://github.com/user-attachments/assets/60442d46-7e63-4eb0-aa79-e1aac3c11420" /><br>
Pembahasan : Pada tahap konfigurasi Git dilakukan pengaturan identitas pengguna berupa nama dan email menggunakan perintah git config --global. Konfigurasi ini digunakan untuk memberikan identitas pada setiap perubahan atau commit yang dibuat. Setelah konfigurasi dilakukan, pengaturan diperiksa menggunakan perintah git config --list untuk memastikan nama dan email telah tersimpan dengan benar.

# MENGELOLA REPO SENDIRI DI AKUN SENDIRI
## Mengelola Repo Sendiri di Account Sendiri
Langkah-langkah:<br>
1. Buat repo kosong di Github, public maupun private
2. Clone repo kosong tersebut di komputer lokal
3. Perintah berikutnya terkait dengan perubahan repo serta sinkronisasi antara GitHub dengan lokal.

### Membuat Repo
1. Klik tanda + pada bagian atas setelah login, pilih New repository <br>
   <img width="142" height="227" alt="image" src="https://github.com/user-attachments/assets/029a1868-c993-4635-bf17-bdf7e8de332f" /><br>
   Pembuatan repository di GitHub dimulai dengan memilih menu New repository dari ikon + di bagian atas setelah login. Selanjutnya, isi detail proyek seperti nama, deskripsi, lisensi,        serta visibilitas (Public atau Private).

2. Isikan nama, keterangan, serta lisensi. Jika dikehendaki, bisa membuat repo Private<br>
   <img width="426" height="173" alt="image" src="https://github.com/user-attachments/assets/b7069427-b397-4e21-b6e9-7b47d639ecaf" /> <br>
   Untuk bagian ini saya lupa screenshot saat membuat repositori, jadi saya buat diterminal command prompt. 

3. Klik Create Repository<br>
  Setelah menekan tombol Create Repository, GitHub akan membuat repository baru sesuai konfigurasi yang ditentukan. Jika dibuat menggunakan pilihan default (tanpa mengaktifkan README,       .gitignore, atau LICENSE), GitHub akan menghasilkan repository kosong dan menampilkan halaman petunjuk awal. Halaman tersebut     berisi alamat URL repository dengan format :<br>
   [https://github.com/username/nama-repo](https://github.com/username/nama-repo)) yang siap digunakan untuk proses cloning ke komputer lokal.<br>

### Clone Repo
Proses clone digunakan untuk menduplikasikan remote repository dari GitHub ke komputer lokal. Langkah ini dilakukan dengan menjalankan perintah git clone <URL-repo> pada terminal atau command line.<br>
<img width="605" height="167" alt="image" src="https://github.com/user-attachments/assets/17007712-f867-4e98-9696-1772156685a9" />

### Mengelola Repo
Pengelolaan repository dilakukan di komputer lokal setelah proses clone dengan memutar siklus edit, add, commit, dan push ke GitHub. Pengelolaan ini dapat dilakukan langsung pada branch utama atau lebih aman melalui metode branching and merging yang memanfaatkan Pull Request. Selain itu, alur pengelolaan mencakup proses sinkronisasi (git pull) serta pembatalan perubahan lokal maupun commit yang sudah di-push menggunakan perintah git reset atau git revert.

# MENGELOLA REPO SENDIRI DI ORGANISASI
## Mengelola Repo Sendiri Di Organisasi
<img width="241" height="355" alt="image" src="https://github.com/user-attachments/assets/aabdf6bd-1e50-45b9-81e9-b29939324df8" /><br>
Pembahasan : Operasinnya sama saja seperti repo di akun sendiri

# MENGELOLA GIT UNTUK KOLABORASI
## 1. Melakukan Fork Repository
<img width="365" height="278" alt="image" src="https://github.com/user-attachments/assets/3a895675-9c1f-45fe-ba89-1411702e62a0" /><br>
Pembahasan : Fork digunakan untuk membuat salinan repository milik pengguna lain ke akun GitHub sendiri. Dengan demikian, kita dapat melakukan perubahan pada salinan tersebut tanpa langsung mengubah repository aslinya.

## 2. Melakukan Clone Repository
Tujuan: Mengunduh repository hasil fork ke komputer lokal.<br>
Langkah-langkah:<br>
1. Buka repository hasil fork di akun GitHub kamu.
2. Klik tombol Code, kemudian salin URL HTTPS repository.<br>
   <img width="195" height="159" alt="Screenshot 2026-10-10 205001" src="https://github.com/user-attachments/assets/e0b4fbd8-81d3-447a-b613-503af84535cb" />
6. Pilih akan ditempatkan di account mana.:<br>
   <img width="365" height="278" alt="Screenshot 2026-10-10 204902" src="https://github.com/user-attachments/assets/b8f628dc-874c-48d5-bcc7-cefc91c16a27" />
7. Setelah proses, repo dari upstream author sudah berada di account GitHub kita (kontributor)<br>
   <img width="475" height="214" alt="image" src="https://github.com/user-attachments/assets/2c552122-7a5f-414d-a7c9-793300be4596" /><br>
   Setelah proses tersebut, clone di komputer lokal:<br>
   <img width="657" height="139" alt="Screenshot 2026-10-10 210814" src="https://github.com/user-attachments/assets/aa932558-0470-4730-8b79-3797afb3a72c" />
   




   


