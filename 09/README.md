# PRAKTIKUM MINGGU 08

Nama : Dwi Ismi Andriani <br>
Nim : 255410012 <br>
Kelas : Informatika - 1 <br>

Laporan praktikum ke - 09 <br>
Topik :Arsitektur Microservices untuk Sistem Terdistribusi: 
GraphQL dan gRPC <br>

# TUJUAN

1. Memahami konsep arsitektur microservices pada sistem terdistribusi dalam menghubungkan frontend dengan layanan backend.
2. Mampu membangun dan mengonfigurasi lingkungan pengembangan terisolasi menggunakan manajemen paket uv untuk masing-masing layanan server dan client.
3. Mampu mengimplementasikan layanan API berbasis GraphQL menggunakan pustaka Strawberry dan SQLModel untuk mengakses data pada basis data SQLite, serta melakukan pengujian melalui GraphiQL Explorer maupun client berbasis pustaka gql.
4. Mampu mendefinisikan struktur layanan menggunakan Protocol Buffers (.proto), melakukan kompilasi menjadi stub, serta membangun komunikasi client-server berbasis gRPC di atas bahasa pemrograman Python.

# DASAR TEORI
1. Arsitektur Microservices pada Sistem Terdistribusi

Microservices merupakan salah satu pendekatan arsitektur perangkat lunak yang banyak diterapkan dalam pengembangan sistem terdistribusi. Pada arsitektur ini, aplikasi dipecah menjadi dua bagian utama, yakni sisi frontend yang menangani antarmuka serta interaksi pengguna (UI/UX), dan sisi backend yang terdiri atas kumpulan layanan (services) independen. Komunikasi antara frontend dan backend umumnya diimplementasikan menggunakan protokol maupun paradigma pertukaran data modern seperti REST API, GraphQL, dan gRPC.

2. GraphQL

GraphQL adalah spesifikasi bahasa kueri (query language) untuk API di sisi server sekaligus mekanisme eksekusi kueri yang memberikan kendali penuh kepada client untuk menentukan struktur dan atribut data yang dibutuhkan. Berbeda dengan RESTful API yang mengandalkan banyak endpoint dengan format respons tetap, GraphQL umumnya mengekspos satu endpoint tunggal sehingga dapat mencegah terjadinya over-fetching maupun under-fetching data. Dalam ekosistem Python, pengembangan server GraphQL dapat dilakukan menggunakan pustaka Strawberry yang memanfaatkan type annotations Python untuk mendefinisikan skema dan resolver, sedangkan komunikasi di sisi client dapat dijalankan secara asinkron menggunakan pustaka gql.

3. gRPC dan Protocol Buffers

gRPC (gRPC Remote Procedure Calls) merupakan kerangka kerja komunikasi jarak jauh berkinerja tinggi yang memungkinkan satu node atau komputer memanggil metode pada node lain secara langsung seolah-olah merupakan objek lokal. Mekanisme komunikasi pada gRPC bertumpu pada Protocol Buffers (Protobuf) sebagai bahasa definisi antarmuka (Interface Definition Language) sekaligus format serialisasi data biner yang ringkas. Kontrak layanan, struktur pesan permintaan (request), dan pesan balasan (response) didefinisikan terlebih dahulu di dalam berkas berekstensi .proto. Berkas tersebut kemudian dikompilasi menggunakan perkakas grpc_tools.protoc untuk menghasilkan kode stub yang identik bagi sisi server maupun client.

4. Object-Relational Mapping (ORM) dengan SQLModel dan SQLite

SQLite adalah mesin basis data relasional tanpa server (serverless) yang menyimpan seluruh struktur tabel dan rekaman data di dalam satu berkas fisik tunggal. Untuk menjembatani manipulasi data antara objek dalam kode Python dan tabel relasional di SQLite, digunakan pustaka SQLModel. SQLModel memadukan kemampuan validasi tipe data dari Pydantic dan mesin kueri dari SQLAlchemy sehingga definisi model tabel dapat digunakan secara terpadu untuk operasional basis data maupun serialisasi skema API.

# PRAKTIK

### 1. Persiapan Struktur Direktori dan Database

<img src="images/01-per 09.png" width="700"> <br>

<img src="images/02-per 09.png" width="700"> <br>

Pembahasan : <br>

Pada tahap awal praktikum di dalam direktori kerja ~/OneDrive/Desktop/prak-dis-dec/09, dilakukan pembentukan struktur direktori proyek menggunakan perintah mkdir -p src/graphql/server src/graphql/client src/grpc/server src/grpc/client. Opsi -p (parents) digunakan agar sistem secara otomatis membuat direktori induk src beserta subdirektori turunan untuk layanan server dan client pada masing-masing arsitektur GraphQL dan gRPC dalam satu kali eksekusi perintah. Pemisahan direktori ini bertujuan agar konfigurasi lingkungan virtual (uv venv) serta dependensi paket setiap komponen dapat terisolasi dan dikelola secara mandiri sesuai standar arsitektur microservices. <br>



