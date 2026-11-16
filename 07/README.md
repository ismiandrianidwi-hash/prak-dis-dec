# PRAKTIKUM MINGGU 07

Nama : Dwi Ismi Andriani <br>
Nim : 255410012 <br>
Kelas : Informatika - 1 <br>

Laporan praktikum ke - 07 <br>
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

## Tahap 1: Mengerjakan Tugas 0

#### 1. Pilih masing-masing 1 contoh vendor/layanan: <br>

- SaaS: Canva.

Uraian : <br>

Aplikasi desain grafis siap pakai berbasis cloud yang diakses langsung melalui browser tanpa perlu instalasi maupun pengelolaan server oleh pengguna. Layanan yang disediakan meliputi antarmuka penyuntingan drag-and-drop beserta jutaan template aset visual, penyimpanan dan kolaborasi proyek secara real-time di cloud, serta fitur otomasi berbasis AI (Magic Design).

- PaaS: Google App Engine.

Uraian : <br>

Platform cloud terkelola penuh (fully managed) untuk membangun dan menjalankan aplikasi web maupun backend tanpa perlu mengurus infrastruktur server dan sistem operasi. Layanan yang disediakan meliputi lingkungan eksekusi (runtime) multi-bahasa (Python, Node.js, Java, Go, dll.) serta kontainer kustom, fitur auto-scaling dan load balancing otomatis sesuai trafik pengguna, serta manajemen versi dan pencatatan log terintegrasi.

- IaaS: Misalnya Amazon Web Services (AWS EC2)

Uraian : <br>

Layanan penyediaan infrastruktur komputasi dasar berupa server virtual (virtual machines) di cloud. Layanan yang disediakan meliputi penyewaan sumber daya perangkat keras virtual (CPU, RAM, penyimpanan, dan jaringan) dengan skema pembayaran pay-as-you-go, serta kendali penuh bagi pengguna untuk memilih sistem operasi, mengatur keamanan jaringan (firewall), dan memasang perangkat lunak sendiri, sementara pusat data fisik dan virtualisasi dikelola sepenuhnya oleh AWS.

#### 2. Jelaskan secara umum arsitektur dari XaaS tersebut dalam bentuk visualisasi gambar.

<img src="images/01_Pert 07.png" width="700"> <br>

Pembahasan : <br>

Arsitektur umum Cloud Computing (XaaS) menggambarkan pembagian tanggung jawab pengelolaan antara pengguna dan penyedia layanan cloud di sepanjang lapisan infrastruktur hingga aplikasi. Pada model On-Premises, pengguna mengelola seluruh lapisan secara mandiri mulai dari jaringan, penyimpanan, server, virtualisasi, sistem operasi, middleware, runtime, data, hingga aplikasi. Pada IaaS, penyedia cloud mengelola lapisan fisik hingga virtualisasi, sementara pengguna mengelola sistem operasi ke atas. Selanjutnya, pada PaaS, penyedia cloud mengelola infrastruktur hingga lingkungan eksekusi (runtime), sehingga pengguna hanya fokus mengelola aplikasi dan data. Terakhir, pada SaaS, seluruh lapisan dari infrastruktur hingga perangkat lunak dikelola sepenuhnya oleh penyedia cloud, sehingga pengguna cukup memakai aplikasi yang tersedia secara langsung.

## Tahap 2: Mengambil Source Code & Menjalankan Flask Secara Lokal

### 1. Buat folder kerja dan unduh repositori Flask:

<img src="images/02_Pert 07.png" width="700"> <br>

Pembahasan : <br>

Pada tahap ini, dilakukan pembuatan direktori kerja baru bernama src menggunakan perintah mkdir src dan berpindah ke dalamnya melalui cd src sebagai lokasi penyimpanan proyek praktikum. Selanjutnya, dijalankan perintah git clone [https://github.com/pallets/flask](https://github.com/pallets/flask) untuk menyalin seluruh repositori resmi framework Flask dari GitHub ke direktori lokal. Proses pengunduhan berjalan hingga selesai dan menghasilkan folder flask yang berisi kode sumber contoh aplikasi tutorial (examples/tutorial) yang akan dijadikan Containerized App (CA).

### 2. Salin folder tutorial menjadi flask-app:

<img src="images/03_Pert 07.png" width="700"> <br>

Pembahasan : <br>

Pada tahap ini, dilakukan penyalinan kode sumber aplikasi tutorial dari dalam repositori Flask yang telah diunduh ke direktori proyek baru bernama flask-app menggunakan perintah PowerShell Copy-Item -Recurse .\flask\examples\tutorial .\flask-app. Langkah ini bertujuan untuk memisahkan berkas proyek praktikum dari keseluruhan repositori utama Flask agar lebih terisolasi dan mudah dikelola. Setelah proses penyalinan selesai, dijalankan perintah cd flask-app untuk berpindah masuk ke dalam direktori root proyek tersebut sebagai lokasi utama eksekusi langkah-langkah selanjutnya.

### 3. Buat Virtual Environment Python 3.14 & instal dependensi menggunakan uv:

<img src="images/04_Pert 07.png" width="700"> <br>

Pembahasan : <br>

Pada tahap ini, dilakukan pembuatan lingkungan virtual (virtual environment) yang terisolasi di dalam direktori proyek flask-app menggunakan perkakas manajemen paket uv melalui perintah uv venv --python 3.14. Berdasarkan hasil eksekusi pada terminal, uv secara otomatis mendeteksi dan menggunakan interpreter CPython versi 3.14.8 untuk membentuk direktori lingkungan virtual baru bernama .venv. Isolasi lingkungan ini bertujuan untuk memastikan seluruh dependensi dan pustaka aplikasi Flask yang akan diinstal nantinya tidak bercampur atau berbenturan dengan paket Python global pada sistem operasi utama.<br>

Aktifkan virtual environment tersebut: <br>

PS C:\Users\Asus\OneDrive\Desktop\prak-dis-dec\07\src\flask-app> .\.venv\Scripts\Activate.ps1 <br>

Kemudian instal paket aplikasi secara editable:<br>

<img src="images/05_Pert 07.png" width="700"> <br>

Pembahasan : <br>

Pada tahap ini, dilakukan aktivasi lingkungan virtual menggunakan perintah .\.venv\Scripts\Activate.ps1, yang ditandai dengan munculnya prefiks (flask-app) pada baris perintah terminal sebagai indikator bahwa lingkungan terisolasi telah aktif. Selanjutnya, dijalankan perintah uv pip install -e . untuk memasang paket aplikasi flaskr dalam mode editable beserta seluruh dependensi utama yang dibutuhkan seperti flask, werkzeug, jinja2, click, itsdangerous, blinker, dan markupsafe. Proses instalasi berhasil diselesaikan dengan total 8 paket terpasang tanpa adanya galat yang menghambat eksekusi aplikasi.

### 4. Inisialisasi database dan jalankan Flask secara lokal:

<img src="images/06_Pert 07.png" width="700"> <br>

Browser http://127.0.0.1:5000 : <br>

<img src="images/07_Pert 07.png" width="700"> <br>

Pembahasan : <br>

Pada tahap ini, dilakukan inisialisasi basis data SQLite menggunakan perintah flask --app flaskr init-db yang berhasil dieksekusi dengan pesan konfirmasi "Initialized the database.". Selanjutnya, server pengembangan lokal dijalankan melalui perintah flask --app flaskr run, sehingga aplikasi aktif dan dapat diakses pada alamat [http://127.0.0.1:5000](http://127.0.0.1:5000). Pengujian melalui peramban web (browser) menunjukkan bahwa halaman utama aplikasi blog Flaskr berhasil dimuat dengan baik beserta menu navigasi Register dan Log In, yang juga tercatat pada log permintaan HTTP GET / dengan kode status 200 di terminal.

## Tahap 3: Membuat Containerized App dengan Docker

### 1. Buat file Dockerfile:

<img src="images/08_Pert 07.png" width="700"> <br>

Pembahasan :
Di dalam folder root flask-app, buat file baru tanpa ekstensi bernama Dockerfile, lalu isi dengan kode berikut (perhatikan perbaikan penulisan ADD . /app/ agar tidak error saat build).

### 2. Aktifkan Docker

<img src="images/09_Pert 07.png" width="700"> <br>

### 3. Build Docker Image

```
(flask-app) PS C:\Users\Asus\OneDrive\Desktop\prak-dis-dec\07\src\flask-app> docker build -f Dockerfile -t flaskr:1.0.0 .
[+] Building 356.3s (11/11) FINISHED                                                       docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                       0.1s
 => => transferring dockerfile: 232B                                                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.14                                             3.9s
 => [internal] load .dockerignore                                                                          0.1s
 => => transferring context: 2B                                                                            0.0s
 => [1/6] FROM docker.io/library/python:3.14@sha256:a7097ae62ea4cf4fec036282cbf97f0d0b7b4f9cb2862779511  294.6s
 => => resolve docker.io/library/python:3.14@sha256:a7097ae62ea4cf4fec036282cbf97f0d0b7b4f9cb286277951115  0.1s
 => => sha256:30a939f32c3666529658895da478296143998cbf9bbb6ede9e0ea68655ef8804 29.89MB / 29.89MB         111.8s
 => => sha256:bd2decaa66042884c6b07d78fdb33ff346fe35b29f7ec34cc18eca1548a6477d 249B / 249B                 1.0s
 => => sha256:7d9ddf92c2fd754219dc2783bdc40c04c9283f48a48741a7b00590eac48a1ac9 6.09MB / 6.09MB            23.4s
 => => sha256:696c1fe91c64662be9b13aa92628d62d6685ab94c0b55d185258a8f762133deb 237.23MB / 237.23MB       278.7s
 => => sha256:411d2dc8717dbb4bb0d3cfa27e6e0275fca455c5220029d7a14dc7a75fbe8665 67.82MB / 67.82MB         210.5s
 => => sha256:e8a88afca2bd37d4058d4b33d9d4d29b0557f8b811bb8c106942b5b51e1e4aad 25.63MB / 25.63MB          85.6s
 => => sha256:a6dd1c05fbba4f9028078a11f143cbb625d2408921eb8207bfa1dd1ad301276f 49.41MB / 49.41MB         102.0s
 => => extracting sha256:a6dd1c05fbba4f9028078a11f143cbb625d2408921eb8207bfa1dd1ad301276f                  3.5s
 => => extracting sha256:e8a88afca2bd37d4058d4b33d9d4d29b0557f8b811bb8c106942b5b51e1e4aad                  1.5s
 => => extracting sha256:411d2dc8717dbb4bb0d3cfa27e6e0275fca455c5220029d7a14dc7a75fbe8665                  4.8s
 => => extracting sha256:696c1fe91c64662be9b13aa92628d62d6685ab94c0b55d185258a8f762133deb                 13.0s
 => => extracting sha256:7d9ddf92c2fd754219dc2783bdc40c04c9283f48a48741a7b00590eac48a1ac9                  0.5s
 => => extracting sha256:30a939f32c3666529658895da478296143998cbf9bbb6ede9e0ea68655ef8804                  1.8s
 => => extracting sha256:bd2decaa66042884c6b07d78fdb33ff346fe35b29f7ec34cc18eca1548a6477d                  0.0s
 => [internal] load build context                                                                          2.1s
 => => transferring context: 5.03MB                                                                        2.0s
 => [2/6] RUN mkdir /app                                                                                   0.9s
 => [3/6] WORKDIR /app                                                                                     0.1s
 => [4/6] ADD . /app/                                                                                      0.2s
 => [5/6] RUN pip install -e .                                                                            22.6s
 => [6/6] RUN flask --app flaskr init-db                                                                   1.0s
 => exporting to image                                                                                    32.5s
 => => exporting layers                                                                                    1.8s
 => => exporting manifest sha256:645313e1a709712682644472671371aac13ea4190f156eb7739506769cdf0251          0.0s
 => => exporting config sha256:df4fde24c3fa7a50aa875776d239168746ca0c501a541c324f9ae30d0fb7ce2a            0.0s
 => => exporting attestation manifest sha256:082392ae01dd678ca766489f2d4b829327ab353538de0de99d6b243a4692  0.0s
 => => exporting manifest list sha256:cd0f1b037a51004bb73b6daa21d46a72bb43d32177a87377ec4b1531c95becd3     0.0s
 => => naming to docker.io/library/flaskr:1.0.0                                                            0.0s
 => => unpacking to docker.io/library/flaskr:1.0.0
```

Pembahasan : <br>

Pada tahap ini, dilakukan proses pembangunan (build) container image menggunakan Docker berdasarkan instruksi pada berkas Dockerfile melalui perintah docker build -f Dockerfile -t flaskr:1.0.0 .. Selama proses eksekusi, Docker mengunduh base image python:3.14 dari Docker Hub, membuat direktori kerja /app, menyalin seluruh berkas proyek ke dalam kontainer (ADD . /app/), menginstal dependensi aplikasi (pip install -e .), serta melakukan inisialisasi basis data (flask --app flaskr init-db). Keseluruhan 11 tahap pembangunan berjalan sukses hingga menghasilkan image lokal baru yang diberi label docker.io/library/flaskr:1.0.0.

### 4. Cek daftar image:

<img src="images/10_Pert 07.png" width="700"> <br>

Pembahasan :

Pada tahap ini, dilakukan verifikasi daftar container image yang tersimpan secara lokal menggunakan perintah docker image ls. Berdasarkan keluaran pada terminal, image hasil proses build sebelumnya telah terdaftar dengan nama flaskr:1.0.0, memiliki ID cd0f1b037a51, serta menempati penggunaan disk sebesar 1.65 GB (content size 424 MB). Selain itu, terlihat beberapa image lain dari praktikum sebelumnya (seperti apacheignite/ignite:3.1.0, load-balancing-bs_app, load-balancing-nginx, dan postgres) yang masih tersimpan di dalam mesin Docker lokal.

### 5. Jalankan kontainer Docker:

Browser http://localhost:5001 : <br>

<img src="images/11_Pert 07.png" width="700"> <br>

Terminal : <br>

<img src="images/12_Pert 07.png" width="700"> <br>

Pembahasan : <br>

Pada tahap ini, container image flaskr:1.0.0 dijalankan sebagai kontainer aktif menggunakan perintah docker run -p 5001:5000 flaskr:1.0.0 yang memetakan port 5000 di dalam kontainer ke port 5001 pada komputer lokal (host). Berdasarkan keluaran terminal, server Flask di dalam kontainer berhasil aktif dan mendengarkan permintaan pada seluruh antarmuka jaringan (0.0.0.0:5000). Pengujian melalui peramban web pada alamat http://localhost:5001 membuktikan bahwa aplikasi web Flaskr dapat diakses dengan normal serta tercatat pada log akses HTTP GET / dengan kode status 200 di terminal.

# KESIMPULAN

Berdasarkan praktikum Modul 7 ini, dapat disimpulkan bahwa penerapan konsep Cloud Computing (XaaS) dan teknologi kontainerisasi mempermudah proses pengemasan serta distribusi perangkat lunak secara terisolasi. Melalui pemanfaatan lingkungan virtual uv dan Docker, aplikasi web berbasis Flask (Flaskr) beserta seluruh dependensi dan basis datanya berhasil dikemas ke dalam container image (flaskr:1.0.0) berdasarkan konfigurasi Dockerfile. Kontainer tersebut kemudian berhasil dijalankan dan diakses melalui peramban pada host Windows melalui mekanisme pemetaan port (5001:5000), yang membuktikan bahwa kontainerisasi mampu menjaga konsistensi lingkungan eksekusi aplikasi tanpa bergantung pada konfigurasi sistem operasi utama.
