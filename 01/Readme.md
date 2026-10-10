# PRAKTIKUM MINGGU 01
Laporan praktikum minggu pertama<br>
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
## 1. Instalansi Git
![alt text](image.png)
Pada gambar tersebut merupakan tahap awal proses instalasi Git versi 2.56.0.2 pada sistem operasi Windows. Pada tahap ini ditampilkan informasi mengenai GNU General Public License (GPL) yang digunakan oleh Git. Untuk melanjutkan proses instalasi, pengguna dapat membaca informasi lisensi kemudian menekan tombol Install. Tahap ini menunjukkan bahwa installer Git sudah siap untuk melakukan proses pemasangan ke komputer.

## 2. Pemeriksaan Instalansi Git
<img width="170" height="113" alt="image" src="https://github.com/user-attachments/assets/0877af49-feb1-4362-a76d-323786291a21" /><br>
Pada tahap pemeriksaan instalasi, dilakukan pengecekan untuk memastikan Git telah berhasil terpasang pada komputer. Pemeriksaan dilakukan melalui Git Bash dengan menjalankan perintah git --version. Hasil yang ditampilkan berupa versi Git yang terpasang, sehingga dapat disimpulkan bahwa Git telah berhasil diinstal dan siap digunakan.

## 3. Konfigurasi Git
<img width="341" height="174" alt="image" src="https://github.com/user-attachments/assets/60442d46-7e63-4eb0-aa79-e1aac3c11420" /><br>
Pada tahap konfigurasi Git dilakukan pengaturan identitas pengguna berupa nama dan email menggunakan perintah git config --global. Konfigurasi ini digunakan untuk memberikan identitas pada setiap perubahan atau commit yang dibuat. Setelah konfigurasi dilakukan, pengaturan diperiksa menggunakan perintah git config --list untuk memastikan nama dan email telah tersimpan dengan benar.

## 4. Mengelola Repo Sendiri di Account Sendiri
Langkah-langkah:<br>
1. Buat repo kosong di Github, public maupun private
2. Clone repo kosong tersebut di komputer lokal
3. Perintah berikutnya terkait dengan perubahan repo serta sinkronisasi antara GitHub dengan lokal.

### Membuat Repo
1. Klik tanda + pada bagian atas setelah login, pilih New repository<br>
<img width="142" height="227" alt="image" src="https://github.com/user-attachments/assets/029a1868-c993-4635-bf17-bdf7e8de332f" /><br>
Pembuatan repository di GitHub dimulai dengan memilih menu New repository dari ikon + di bagian atas setelah login. Selanjutnya, isi detail proyek seperti nama, deskripsi, lisensi, serta visibilitas (Public atau Private).

2. Isikan nama, keterangan, serta lisensi. Jika dikehendaki, bisa membuat repo Private<br>
   <img width="455" height="206" alt="image" src="https://github.com/user-attachments/assets/f224fae9-aade-46b0-80b8-02133ddbf608" />
   Untuk bagian ini saya lupa screenshot saat membuat repositori, jadi saya buat diterminal command prompt. 

3. Klik Create Repository
  Setelah menekan tombol Create Repository, GitHub akan membuat repository baru sesuai konfigurasi yang ditentukan. Jika dibuat menggunakan pilihan default (tanpa mengaktifkan README, .gitignore, atau LICENSE), GitHub akan menghasilkan repository kosong dan menampilkan halaman petunjuk awal. Halaman tersebut     berisi alamat URL repository dengan format :<br>
[https://github.com/username/nama-repo](https://github.com/username/nama-repo)) yang siap digunakan untuk proses cloning ke komputer lokal.<br>
   <img width="426" height="173" alt="image" src="https://github.com/user-attachments/assets/b7069427-b397-4e21-b6e9-7b47d639ecaf" />


### Clone Repo
Proses clone digunakan untuk menduplikasikan remote repository dari GitHub ke komputer lokal. Langkah ini dilakukan dengan menjalankan perintah git clone <URL-repo> pada terminal atau command line.<br>
<img width="605" height="167" alt="image" src="https://github.com/user-attachments/assets/17007712-f867-4e98-9696-1772156685a9" />

### Mengelola Repo







