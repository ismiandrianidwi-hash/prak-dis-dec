#  PRAKTIKUM MINGGU 04

Nama : Dwi Ismi Andriani <br>
Nim : 255410012 <br>
Kelas : Informatika - 1 <br>

Laporan praktikum ke - 04 <br>
Topik : Sinkronisasi Pada Sistem Terdistribusi <br>

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