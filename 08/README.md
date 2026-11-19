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
#### Cek & atur versi Python dengan uv:
