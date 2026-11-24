# PRAKTIKUM MINGGU 08

Nama : Dwi Ismi Andriani <br>
Nim : 255410012 <br>
Kelas : Informatika - 1 <br>

Laporan praktikum ke - 08 <br>
Topik :Arsitektur Microservices untuk Sistem Terdistribusi <br>

# TUJUAN
1. Memahami konsep penerapan arsitektur microservices pada pengembangan sistem terdistribusi.
2. Mampu mengelola lingkungan pengembangan Python dan instalasi pustaka menggunakan manajemen paket uv.
3. Mampu merancang basis data menggunakan SQLite dan melakukan pemetaan relasional objek menggunakan pustaka SQLModel.
4. Mampu membangun dan menguji layanan backend berupa RESTful API menggunakan framework FastAPI dan server Uvicorn.

# DASAR TEORI
#### 1. Arsitektur Microservices

Arsitektur microservices membagi perangkat lunak menjadi komponen-komponen terpisah antara bagian frontend dan backend. Bagian frontend menangani antarmuka serta interaksi pengguna, sedangkan bagian backend terdiri dari layanan-layanan independen yang menyediakan data atau fungsionalitas tertentu. Komunikasi antara frontend dan layanan backend umumnya menggunakan protokol seperti REST API, GraphQL, atau gRPC.

#### 2. REST API dan FastAPIRepresentational State Transfer (REST)

merupakan gaya arsitektur komunikasi berbasis HTTP yang memanfaatkan metode standar seperti GET untuk pertukaran data antar layanan. FastAPI adalah framework web modern berbasis Python yang dirancang untuk membangun REST API berkinerja tinggi, lengkap dengan validasi data otomatis dan serialisasi format JSON.

#### 3. ORM dan SQLModel

Object-Relational Mapping (ORM) adalah teknik pemrograman yang menghubungkan tabel pada basis data relasional dengan objek kelas dalam kode program. SQLModel menggabungkan kemampuan SQLAlchemy dan Pydantic untuk memetakan struktur tabel SQLite ke dalam kelas Python sekaligus memvalidasi tipe data secara otomatis.

#### 4. SQLite

SQLite adalah sistem manajemen basis data relasional ringan berbasis berkas tunggal (serverless) yang tidak memerlukan konfigurasi server terpisah, sehingga praktis digunakan untuk pengembangan layanan microservices berskala kecil hingga menengah.

#### 5. Manajemen Environment dengan uv dan Uvicorn

uv berfungsi sebagai pengelola versi Python, virtual environment, dan instalasi paket secara cepat. Sementara itu, Uvicorn merupakan implementasi server ASGI yang bertugas menjalankan aplikasi FastAPI agar dapat diakses melalui jaringan lokal maupun pengujian via peramban web dan perintah curl.

# PRAKTIK 
## 1. Persiapan Environment & Pustaka (PowerShell)
### Cek & atur versi Python dengan uv:

#### uv python list :

```
PS C:\Users\Asus\OneDrive\Desktop\prak-dis-dec\08> uv python list
cpython-3.16.0a1-windows-x86_64-none                 <download available>
cpython-3.16.0a1+freethreaded-windows-x86_64-none    <download available>
cpython-3.15.0-windows-x86_64-none                   C:\Users\Asus\AppData\Local\Programs\Python\Python315\python.exe
cpython-3.15.0-windows-x86_64-none                   <download available>
cpython-3.15.0+freethreaded-windows-x86_64-none      <download available>
cpython-3.14.8-windows-x86_64-none                   C:\Users\Asus\AppData\Roaming\uv\python\cpython-3.14.8-windows-x86_64-none\python.exe
cpython-3.14.8-windows-x86_64-none                   C:\Users\Asus\.local\bin\python3.14.exe
cpython-3.14.8-windows-x86_64-none                   C:\Users\Asus\AppData\Roaming\uv\python\cpython-3.14-windows-x86_64-none\python.exe
cpython-3.14.8+freethreaded-windows-x86_64-none      <download available>
cpython-3.13.16-windows-x86_64-none                  <download available>
cpython-3.13.16+freethreaded-windows-x86_64-none     <download available>
cpython-3.12.15-windows-x86_64-none                  <download available>
cpython-3.11.17-windows-x86_64-none                  <download available>
cpython-3.10.22-windows-x86_64-none                  <download available>
cpython-3.9.25-windows-x86_64-none                   <download available>
cpython-3.8.20-windows-x86_64-none                   <download available>
pypy-3.12.14-windows-x86_64-none                     <download available>
pypy-3.11.16-windows-x86_64-none                     <download available>
pypy-3.10.16-windows-x86_64-none                     <download available>
pypy-3.9.19-windows-x86_64-none                      <download available>
pypy-3.8.16-windows-x86_64-none                      <download available>
graalpy-3.13.0-windows-x86_64-none                   <download available>
graalpy-3.12.0-windows-x86_64-none                   <download available>
graalpy-3.11.0-windows-x86_64-none                   <download available>
graalpy-3.10.0-windows-x86_64-none                   <download available>
```

#### uv python install 3.14.4

<img src="images/01-pert 08.png" width="700"> <br>

#### uv python pin 3.14.4

<img src="images/02-pert 08.png" width="700"> <br>

Pembahasan : <br>

Pada tahap awal praktikum, dilakukan konfigurasi versi interpreter Python di dalam direktori kerja pertemuan 8 (...\prak-dis-dec\08) menggunakan manajer paket uv melalui terminal PowerShell. Berikut rincian eksekusi perintah yang dilakukan: <br>

1. Pemeriksaan Daftar Versi Python (uv python list)

Perintah ini digunakan untuk memeriksa daftar versi interpreter Python yang tersedia, baik yang sudah terpasang secara lokal maupun yang siap diunduh dari repositori uv. Berdasarkan keluaran terminal, sistem sebelumnya hanya memiliki Python 3.15.0 dan 3.14.8, sehingga versi 3.14.4 yang dipersyaratkan pada modul belum tersedia di sistem lokal.

2. Instalasi Python 3.14.4 (uv python install 3.14.4)

Setelah memastikan versi yang dibutuhkan belum tersedia, perintah ini dijalankan untuk mengunduh dan memasang interpreter cpython-3.14.4-windows-x86_64-none secara otomatis ke dalam direktori penyimpanan internal uv. Proses instalasi berhasil diselesaikan dalam waktu 14,89 detik.

3. Penguncian Versi Python (uv python pin 3.14.4)

Perintah terakhir ini membuat berkas konfigurasi .python-version berisi nilai 3.14.4 di dalam direktori proyek 08. Tujuannya adalah mengunci agar seluruh lingkungan virtual (virtual environment) serta eksekusi kode di dalam folder praktikum ini secara konsisten menggunakan Python 3.14.4.   

### Buat dan aktifkan virtual environment :
#### uv venv

<img src="images/03-pert 08.png" width="700"> <br>

####  .venv\Scripts\Activate.ps1

<img src="images/04-pert 08.png" width="700"> <br>

Pembahasan : <br>

Setelah menentukan versi Python yang digunakan pada direktori kerja, langkah berikutnya adalah mengisolasi lingkungan pengembangan proyek menggunakan virtual environment. Pembuatan lingkungan virtual ini bertujuan agar seluruh dependensi dan pustaka (library) yang akan diinstal tidak bercampur atau berbenturan dengan konfigurasi Python global pada sistem operasi Windows. Berikut rincian eksekusi perintah yang dilakukan: 

1. Pembuatan Virtual Environment (uv venv)

Perintah ini membuat direktori lingkungan virtual baru bernama .venv di dalam folder proyek 08. Berdasarkan keluaran terminal (Using CPython 3.14.4), uv secara otomatis mendeteksi berkas .python-version dari langkah sebelumnya dan menggunakan interpreter CPython 3.14.4 sebagai basis lingkungan virtual tersebut.

2. Aktivasi Virtual Environment (.venv\Scripts\Activate.ps1)

Berbeda dengan sistem operasi Linux yang menggunakan skrip aktivasi berbasis shell (source .venv/bin/activate) seperti pada modul, pada terminal PowerShell di Windows aktivasi dilakukan dengan menjalankan skrip .venv\Scripts\Activate.ps1. Eksekusi perintah ini berhasil tanpa kendala kebijakan eksekusi (Execution Policy), yang ditandai dengan kesiapan terminal untuk menggunakan interpreter serta paket di dalam lingkungan .venv pada tahap instalasi berikutnya.

## 2. Membuat Database & Tabel
### Instal pustaka FastAPI dan SQLModel:

```
(08) PS C:\Users\Asus\OneDrive\Desktop\prak-dis-dec\08> uv pip install --link-mode=copy "fastapi[standard]" sqlmodel
Resolved 61 packages in 27.78s
Prepared 30 packages in 7.03s
Installed 45 packages in 4.88s
 + agent-detector==2.0.0                                                                                        
 + certifi==2026.10.23                                                                                          
 + charset-normalizer==3.5.2                                                                                    
 + click==8.5.1                                                                                                 
 + colorama==0.4.6                                                                                              
 + detect-installer==0.2.1                                                                                      
 + dnspython==2.9.2                                                                                             
 + email-validator==2.4.0                                                                                       
 + fastapi-cli==0.0.34                                                                                          
 + fastapi-cloud-cli==0.28.0                                                                                    
 + fastar==0.12.0                                                                                               
 + googleapis-common-protos==1.76.0                                                                             
 + h11==0.16.0                                                                                                  
 + httpcore==1.0.9                                                                                              
 + httpcore2==2.16.2                                                                                            
 + httptools==0.9.0                                                                                             
 + httpx==0.28.1                                                                                                
 + httpx2==2.16.2                                                                                               
 + jinja2==3.1.6                                                                                                
 + markdown-it-py==4.3.0                                                                                        
 + markupsafe==3.0.4                                                                                            
 + mdurl==0.1.2                                                                                                 
 + opentelemetry-exporter-http-transport==0.66b2                                                                
 + opentelemetry-exporter-otlp-common==0.66b2                                                                   
 + opentelemetry-exporter-otlp-proto-common==1.45.2
 + opentelemetry-exporter-otlp-proto-http==1.45.2
 + opentelemetry-proto==1.45.2
 + opentelemetry-sdk==1.45.2
 + opentelemetry-semantic-conventions==0.66b2
 + protobuf==7.36.2
 + pydantic-extra-types==2.11.1
 + pygments==2.21.0
 + python-multipart==0.0.34
 + requests==2.34.2
 + rich==15.0.0
 + rich-toolkit==0.20.6
 + rignore==0.8.1
 + sentry-sdk==2.75.0
 + shellingham==1.5.4
 + truststore==0.10.5
 + typer==0.29.2
 + urllib3==2.8.0
 + uvicorn==0.54.0
 + watchfiles==1.3.0
 + websockets==17.4
 ```

 Pembahasan : <br>

 Selain pustaka inti fastapi, sqlmodel, pydantic, dan sqlalchemy, ditambahkan juga instalasi extras "fastapi[standard]" menggunakan mode salin yang sama agar server ASGI uvicorn serta utilitas pendukungnya terpasang lengkap sesuai kebutuhan eksekusi pada modul. 

### Buat database dan tabel sdm:
#### Pemilihan Paket Binari Windows
 <img src="images/05-pert 08.png" width="700"> <br>

 Pembahasan : <br>

 Pada kategori Precompiled Binaries for Windows (File Biner yang Sudah Dikompilasi untuk Windows), dipilih paket sqlite-tools-win-x64-3540100.zip yang berukuran sekitar 5,56 MiB. Paket ini dipilih karena berisi utilitas baris perintah lengkap—termasuk sqlite3.exe—yang kompatibel dengan arsitektur sistem operasi Windows 64-bit, berbeda dengan paket sqlite-dll yang hanya memuat pustaka dinamis tanpa antarmuka terminal, lalu ekstrak sqlite3.exe dan run .\sqlite3.exe departemen-sdm.db

#### Masukkan 

 <img src="images/06-pert 08.png" width="700"> <br>

 Pembahasan : <br>

 Pada tahap ini dilakukan inisialisasi berkas basis data lokal bernama departemen-sdm.db menggunakan antarmuka baris perintah sqlite3.exe versi 3.54.1. Selanjutnya, dibuat tabel sdm melalui kueri CREATE TABLE dengan tiga kolom utama, yakni id bertipe INTEGER PRIMARY KEY sebagai kunci utama otomatis, npp bertipe CHAR(6) untuk nomor pokok pegawai, serta nama bertipe VARCHAR(50) untuk nama pegawai. Tiga baris data karyawan kemudian dimasukkan menggunakan perintah INSERT INTO. Melalui kueri SELECT * FROM sdm; yang dipadukan dengan pengaturan .mode column dan .headers on, hasil verifikasi menampilkan ketiga data telah tersimpan secara terstruktur ke dalam basis data.

## 3. Membuat & Menjalankan REST API
### Buat file bernama service.py di dalam folder proyek yang sama

 <img src="images/07-pert 08.png" width="700"> <br>

 Pembahasan : <br>

Layanan REST API dibangun menggunakan bahasa Python dengan pustaka FastAPI dan SQLModel sebagai ORM untuk menghubungkan aplikasi dengan database SQLite (departemen-sdm.db). Struktur tabel sdm direpresentasikan melalui kelas model Sdm (yang memuat atribut id, npp, dan nama), sementara koneksi ke database dikelola menggunakan fungsi sesi get_session. Sebuah endpoint HTTP GET didaftarkan pada rute /sdm/ (@app.get("/sdm/")) untuk mengeksekusi perintah query select(Sdm) dan mengembalikan seluruh data karyawan dari tabel dalam format JSON. Layanan ini kemudian dijalankan secara lokal melalui server ASGI Uvicorn pada port 8000 dengan perintah uvicorn service:app --reload.

#### Jalankan server Uvicorn:

 <img src="images/08-pert 08.png" width="700"> <br>

 Pretty-print : <br>

 <img src="images/09-pert 08.png" width="700"> <br>

 Pembahasan : <br>

 Pengujian layanan dilakukan dengan mengakses rute endpoint secara spesifik melalui alamat [http://127.0.0.1:8000/sdm/](http://127.0.0.1:8000/sdm/) (atau http://localhost:8000/sdm/) pada peramban web (browser). Penambahan path /sdm/ diperlukan karena alamat utama (127.0.0.1:8000) tidak memiliki endpoint terdaftar sehingga akan mengembalikan respons {"detail":"Not Found"}. Ketika rute /sdm/ diakses, server merespons dengan mengirimkan seluruh data karyawan dalam format JSON mentah, dan dengan mengaktifkan fitur Pretty-print pada browser, struktur data JSON tersebut ditampilkan secara terformat dan berjenjang sehingga mudah dibaca dan diverifikasi.

# TUGAS
## 1. Buat Tabel Baru di SQLite

 <img src="images/10-pert 08.png" width="700"> <br>

Pembahasan : <br>

Pada tahap pertama tugas, dibuat sebuah berkas basis data SQLite baru bernama inventaris.db untuk menyimpan data inventaris barang. Di dalam basis data tersebut, dibentuk tabel baru bernama produk menggunakan perintah SQL CREATE TABLE yang dirancang berbeda dari contoh modul dengan mengimplementasikan satu primary key serta lima tipe data berbeda sesuai ketentuan tugas. Struktur tabel ini terdiri atas kolom id bertipe INTEGER PRIMARY KEY sebagai kunci utama unik yang bertambah otomatis, kode bertipe CHAR(6) untuk menyimpan kode unik produk sepanjang 6 karakter tetap, nama bertipe VARCHAR(50) untuk nama produk maksimal 50 karakter dinamis, stok bertipe INT untuk jumlah stok dalam bilangan bulat, harga bertipe FLOAT untuk nominal harga dalam bilangan desimal, serta tersedia bertipe BOOLEAN untuk menandai status ketersediaan barang. Keberhasilan pembuatan tabel ini kemudian diverifikasi melalui perintah .tables pada antarmuka SQLite yang memastikan bahwa tabel produk telah terdaftar dan siap digunakan pada tahap pengisian data berikutnya.

## 2. Isi 5 Data Menggunakan Script Python

 Kode Program Seed.py : <br>

  <img src="images/11-pert 08.png" width="700"> <br>

Jalankan skrip diatas melalui terminal PowerShell: <br>

<img src="images/12-pert 08.png" width="700"> <br>

Pembahasan : <br>

Pada tahap kedua, pengisian lima baris data ke dalam tabel produk pada basis data inventaris.db dilakukan secara terprogram menggunakan skrip Python (seed.py) dengan memanfaatkan pustaka SQLModel. Skrip ini mendefinisikan kelas model Produk untuk memetakan struktur tabel SQLite ke dalam objek Python (id, kode, nama, stok, harga, dan tersedia) serta menghubungkannya melalui create_engine("sqlite:///inventaris.db"). Lima objek data produk yang mencakup kelima tipe data berbeda kemudian ditambahkan ke dalam sesi basis data menggunakan metode session.add() dan disimpan secara permanen melalui perintah session.commit().

## 3. Buat Endpoint RESTful API
Service.py : <br>

<img src="images/14-pert 08.png" width="700"> <br>

Server Uvicorn : <br>

<img src="images/13-pert 08.png" width="700"> <br>

Pembahasan : 

Pada tahap ketiga tugas, berkas service.py diperbarui menggunakan kerangka kerja FastAPI dan SQLModel untuk membangun layanan RESTful API yang terhubung ke basis data tugas inventaris.db. Struktur tabel produk dipetakan melalui kelas model Produk beserta keenam atributnya (id, kode, nama, stok, harga, dan tersedia), sedangkan manajemen koneksi ke SQLite ditangani oleh fungsi get_session. Sebuah endpoint HTTP GET didaftarkan pada rute /produk/ melalui fungsi read_produk() yang menjalankan perintah kueri select(Produk) untuk mengambil dan mengembalikan seluruh daftar produk dari tabel dalam format JSON. <br>

## 4. Tampilkan Hasil dengan curl

Web : <br>

<img src="images/15-pert 08.png" width="700"> <br>

Pretty-print : <br>

<img src="images/16-pert 08.png" width="700"> <br>

Pembahasan : <br>

Layanan API kemudian dijalankan secara lokal menggunakan server Uvicorn (uvicorn service:app --reload) pada alamat [http://127.0.0.1:8000](http://127.0.0.1:8000). Pengujian awal melalui peramban web (browser) dengan mengakses alamat [http://127.0.0.1:8000/produk/](http://127.0.0.1:8000/produk/) menghasilkan status respons 200 OK pada log server dan menampilkan kelima data produk dalam format JSON mentah (raw). Setelah opsi Pretty-print pada peramban diaktifkan, data JSON tersebut diformat secara berjenjang dan rapi, yang memverifikasi bahwa seluruh data dengan lima tipe data berbeda (bilangan bulat, karakter, desimal, dan boolean) telah berhasil disajikan oleh endpoint dengan akurat.

# KESIMPULAN

Praktikum Modul 8 mengenai pembangunan layanan berbasis microservices telah berhasil dilaksanakan dengan mengintegrasikan basis data relasional SQLite bersama kerangka kerja FastAPI dan ORM SQLModel menggunakan bahasa pemrograman Python. Melalui tahapan latihan maupun pengerjaan tugas mandiri (inventaris.db dengan tabel produk), dapat ditarik beberapa poin kesimpulan utama:

- Pemodelan Basis Data dan ORM: SQLite mampu menyimpan skema tabel dengan beragam tipe data (INTEGER PRIMARY KEY, CHAR, VARCHAR, INT, FLOAT, dan BOOLEAN) secara ringan dalam satu berkas lokal, sementara pustaka SQLModel mempermudah pemetaan struktur tabel SQLite ke dalam kelas objek Python sehingga proses penyisipan data secara terprogram (seed.py) maupun pembacaan data menjadi lebih terstruktur dan aman dari kesalahan sintaks SQL.
- Penyajian Layanan RESTful API: Penggunaan FastAPI dan server ASGI Uvicorn memungkinkan pembuatan endpoint HTTP GET (/sdm/ dan /produk/) secara ringkas dan cepat, di mana data yang diambil dari basis data otomatis diserialisasi ke dalam format standar pertukaran data JSON dengan respons status 200 OK.
- Verifikasi Klien dan Interoperabilitas: Layanan REST API yang berjalan pada server lokal ([http://127.0.0.1:8000](http://127.0.0.1:8000)) terbukti dapat diakses dan diverifikasi secara konsisten oleh berbagai jenis klien (client-agnostic), baik melalui peramban web (browser) dengan bantuan fitur Pretty-print untuk mempermudah pembacaan struktur data maupun melalui antarmuka baris perintah menggunakan utilitas curl.
