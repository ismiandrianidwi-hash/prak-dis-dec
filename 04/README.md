#  PRAKTIKUM MINGGU 04

Nama : Dwi Ismi Andriani <br>
Nim : 255410012 <br>
Kelas : Informatika - 1 <br>

Laporan praktikum ke - 04 <br>
Topik : Konsistensi dan Replikasi pada Sistem Terdistribusi <br>

# TUJUAN
1. Memahami konsep konsistensi dan replikasi data pada sistem terdistribusi.
2. Mempraktikkan konfigurasi streaming replication menggunakan PostgreSQL dengan Docker.
3. Memahami perbedaan fungsi server primary dan replica pada PostgreSQL.
4. Memahami konsep High Availability (HA) dengan mempromosikan server replica menjadi primary.
5. Mempraktikkan konfigurasi replikasi master-master menggunakan Apache Ignite.
6. Menguji proses replikasi data antarnode melalui eksekusi perintah SQL.

# DASAR TEORI
Sistem terdistribusi merupakan sistem yang terdiri dari beberapa komputer atau server yang saling bekerja sama untuk mengelola dan bertukar data. Konsistensi dan replikasi merupakan konsep penting untuk menjaga kesesuaian data serta meningkatkan ketersediaan layanan.

1. Replikasi Data

Replikasi data adalah proses menyalin dan menyinkronkan data dari satu server ke server lain. Replikasi bertujuan menjaga ketersediaan data dan memungkinkan data yang sama diakses melalui beberapa server.

2. Streaming Replication PostgreSQL

Streaming replication merupakan mekanisme replikasi pada PostgreSQL yang menyalin perubahan data dari server primary ke server replica. Server primary menangani operasi baca dan tulis, sedangkan replica menyinkronkan data dan menyediakan akses baca.

3. High Availability (HA)

High Availability merupakan konsep untuk menjaga layanan tetap tersedia ketika terjadi gangguan pada server. Dalam praktikum ini, server replica dapat dipromosikan menjadi primary apabila server utama mengalami gangguan.

4. Replikasi Master-Master Apache Ignite

Replikasi master-master merupakan model replikasi yang memungkinkan node dalam cluster memiliki kemampuan sebagai primary untuk melakukan operasi baca dan tulis. Pada Apache Ignite, data yang dikelola dalam cluster dapat diakses melalui beberapa node.

5. Docker dan Docker Compose

Docker merupakan platform untuk menjalankan aplikasi dalam container, sedangkan Docker Compose digunakan untuk mengatur dan menjalankan beberapa container melalui satu file konfigurasi. Dalam praktikum ini, keduanya digunakan untuk menjalankan PostgreSQL dan Apache Ignite beserta node-node yang diperlukan.

## 4.1 Streaming Replication Menggunakan PostgreSQL
Membuat dua server database yang saling terhubung, yaitu server utama (primary) dan server cadangan (replica). Ketika data ditambahkan atau diubah di primary, perubahan tersebut akan direplikasi ke replica.<br>

Install Docker<br>

<img src="images/01_install_docker.png" width="700"> <br>

Pembahasan : <br>

Pada bagian ini, dilakukan persiapan lingkungan kerja (environment) berupa instalasi dan verifikasi Docker beserta Docker Compose sebagai prasyarat utama sebelum membangun arsitektur streaming replication PostgreSQL. Docker digunakan untuk mendistribusikan node primary dan node replica secara terisolasi di dalam kontainer terpisah pada satu mesin lokal.   Proses diawali dengan melakukan instalasi Docker Engine serta Docker Desktop pada sistem operasi yang digunakan. Setelah proses instalasi selesai, daemon Docker (dockerd) diaktifkan agar layanan kontainerisasi dapat berjalan dan siap menerima perintah. Untuk memastikan bahwa Docker telah terpasang dengan benar dan mesin kontainer sudah beroperasi dengan status Engine running, dilakukan pengujian koneksi dan pengecekan status sistem menggunakan perintah docker info. Verifikasi ini penting dilakukan untuk menjamin seluruh komponen runtime Docker siap digunakan dalam menjalankan layanan cluster PostgreSQL melalui Docker Compose. <br>

## 4.1.1 Prasyarat
Memastikan Docker dan Docker Compose sudah terinstal serta layanan Docker aktif. <br>

<img src="images/02_install_docker.png" width="700"> <br>

Pembahasan : <br>

Pada bagian 4.1.1 Prasyarat ini, dilakukan pengecekan lingkungan sistem untuk memastikan perangkat lunak pendukung utama, yaitu Docker Engine dan Docker Compose, telah terpasang dengan benar serta siap digunakan sebelum mengonfigurasi streaming replication pada PostgreSQL. Pengujian dilakukan dengan menjalankan perintah docker --version yang menghasilkan versi Docker 29.9.2 (build a82e528), serta perintah docker compose version yang menampilkan versi Docker Compose v5.6.1. Terverifikasinya kedua komponen ini menjamin bahwa sistem lokal telah memenuhi seluruh kebutuhan prasyarat untuk mengelola kontainer secara multi-container serta mengaktifkan daemon Docker (dockerd) dengan stabil selama proses praktikum berlangsung.<br>

## 4.1.2 Struktur Direktori dan FIle
Membuat 3 file :<br>

<img src="images/03_install_docker.png" width="700"> <br>

Pembahasan : <br>

Pada bagian 4.1.2 Struktur Direktori dan File, dilakukan penyiapan struktur direktori dan berkas konfigurasi utama di dalam folder proyek streaming-replication. Terdapat tiga berkas utama yang dibuat untuk mendukung jalannya arsitektur streaming replication PostgreSQL. Berkas pertama adalah 00_init.sql yang berisi perintah SQL untuk membuat user replikasi (replicator) serta physical replication slot (replication_slot) saat server primary diinisialisasi. Berkas kedua adalah docker-compose.yaml yang mendefinisikan service untuk node primary dan node replica, pemetaan port, environment variables, konfigurasi WAL (Write-Ahead Logging), hingga perintah otomatisasi sinkronisasi base backup. Terakhir, berkas env.sh disiapkan sebagai skrip shell yang berisi kumpulan alias perintah Docker untuk mempermudah eksekusi instruksi selama praktikum. Penyiapan ketiga berkas ini secara terstruktur menjamin seluruh proses kontainerisasi dan replikasi basis data berjalan konsisten serta terisolasi. <br>

## 4.1.3 Menjalankan docker-compose 

<img src="images/04_install_docker.png" width="700"><br>

Kemudian periksa kontainernya:<br>

<img src="images/05_install_docker.png" width="700"><br>

<img src="images/06_install_docker.png" width="700"><br>

Pembahasan : <br>

Pada praktikum ini, Docker Compose digunakan untuk menjalankan container PostgreSQL primary dan replica. Berdasarkan hasil perintah docker ps, kedua container berstatus healthy. Selain itu, pemeriksaan pg_stat_replication menunjukkan status streaming dengan mode replikasi async. Hal ini menunjukkan bahwa kedua container berjalan dengan baik dan proses streaming replication telah berhasil dilakukan.<br>

## 4.1.4 Pengujian 







