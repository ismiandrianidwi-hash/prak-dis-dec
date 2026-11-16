# PRAKTIKUM MINGGU 06

Nama : Dwi Ismi Andriani <br>
Nim : 255410012 <br>
Kelas : Informatika - 1 <br>

Laporan praktikum ke - 06 <br>
Topik : Cloud Computing <br>

# TUJUAN
1. Memahami konsep dasar Cloud Computing dengan pendekatan XaaS (Everything as a Service) beserta pembagian layanannya (SaaS, PaaS, dan IaaS) serta arsitektur umumnya.

2. Mampu menyiapkan lingkungan pengembangan (virtual environment) Python dan menjalankan aplikasi berbasis web (Flask) secara lokal.

3. Mampu membungkus aplikasi web menjadi Containerized App (CA) dengan menyusun konfigurasi Dockerfile.

4. Mampu membangun (build) container image dan menjalankan kontainer aplikasi menggunakan dua container engine yang berbeda, yaitu Docker dan Podman, serta memahami perbedaan manajemen layanannya.

# DASAR TEORI

#### 1. Cloud Computing dan Konsep XaaS (Everything as a Service)

Cloud Computing merupakan model penyediaan sumber daya komputasi melalui jaringan internet yang mengadopsi pendekatan XaaS (Everything as a Service). Melalui pendekatan ini, penyedia layanan cloud (cloud provider) mengelola dan menyediakan berbagai infrastruktur maupun perangkat lunak, sementara konsumen mengakses serta memanfaatkannya sesuai kebutuhan dalam bentuk layanan. Secara umum, kategori XaaS terbagi menjadi tiga model utama:

- IaaS (Infrastructure as a Service): Layanan yang menyediakan sumber daya infrastruktur komputasi dasar secara virtual, seperti server virtual, penyimpanan (storage), dan jaringan. Pengguna memiliki kendali penuh atas sistem operasi dan aplikasi yang berjalan di atasnya.

- PaaS (Platform as a Service): Layanan yang menyediakan lingkungan atau platform siap pakai untuk pengembangan, pengujian, dan penerapan (deployment) aplikasi tanpa harus mengelola infrastruktur perangkat keras maupun sistem operasi di bawahnya.

- SaaS (Software as a Service): Layanan perangkat lunak siap pakai yang dijalankan dan dikelola sepenuhnya oleh penyedia cloud, sehingga pengguna akhir dapat langsung mengakses aplikasi melalui peramban (web browser) atau antarmuka klien.   

#### 2. Containerized App (CA)

Containerized App (CA) adalah aplikasi yang dikemas bersama seluruh dependensi, pustaka (libraries), dan konfigurasi lingkungannya ke dalam satu unit terisolasi yang disebut kontainer. Konsep kontainerisasi memastikan aplikasi dapat berjalan secara konsisten dan portabel di berbagai lingkungan komputasi tanpa mengalami masalah perbedaan konfigurasi sistem operasi host. Untuk membangun cetak biru (image) dari sebuah kontainer, digunakan berkas instruksi teks bernama Dockerfile yang mendefinisikan base image, direktori kerja, instalasi dependensi, eksposur port, hingga perintah eksekusi utama aplikasi.

#### 3. Docker dan Podman

Dalam ekosistem kontainerisasi, terdapat beberapa container engine yang digunakan untuk mengelola siklus hidup image dan kontainer:

- Docker: Platform kontainerisasi yang menggunakan arsitektur berbasis client-server. Perintah Docker CLI berkomunikasi dengan proses latar belakang (background daemon) bernama dockerd yang bertugas membangun, menjalankan, dan mendistribusikan kontainer

- Podman (Pod Manager): Container engine sumber terbuka yang kompatibel dengan standar OCI (Open Container Initiative) dan format Dockerfile. Berbeda dengan Docker, Podman dirancang dengan arsitektur daemonless (tidak memerlukan background service seperti dockerd) serta mendukung eksekusi kontainer tanpa hak akses root (rootless), sehingga menawarkan keamanan dan efisiensi sumber daya yang lebih baik.

#### 4. Flask dan Manajemen Lingkungan Python (uv)

Flask adalah micro-framework pengembangan web berbasis bahasa pemrograman Python yang ringan dan modular. Dalam pengembangan aplikasi Python modern, isolasi dependensi sangat penting dilakukan menggunakan virtual environment. uv merupakan perkakas manajemen paket dan lingkungan Python berkecepatan tinggi yang digunakan untuk menginisialisasi versi Python spesifik serta menginstal paket-paket yang dibutuhkan proyek (pyproject.toml) secara terisolasi sebelum aplikasi dikemas ke dalam kontainer.

# PRAKTIK

