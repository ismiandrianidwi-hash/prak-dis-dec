# PRAKTIKUM MINGGU 06

Nama : Dwi Ismi Andriani <br>
Nim : 255410012 <br>
Kelas : Informatika - 1 <br>

Laporan praktikum ke - 06 <br>
Topik : Distributed File System - HDFS <br>

# TUJUAN
1. Mahasiswa mampu menyiapkan prasyarat lingkungan perangkat lunak (software requirements) yang dibutuhkan untuk menjalankan sistem berkas terdistribusi, meliputi Java Development Kit (JDK 17/21), SSH (passwordless SSH), dan pdsh (Parallel Distributed Shell).

2. Mahasiswa mampu melakukan proses unduhan, instalasi, serta konfigurasi variabel lingkungan (environment variables) Apache Hadoop (versi 3.5.0) pada sistem operasi Linux.

3. Mahasiswa mampu mengonfigurasi komponen inti Hadoop dan HDFS melalui berkas konfigurasi XML (core-site.xml, hdfs-site.xml, mapred-site.xml, dan yarn-site.xml) serta hadoop-env.sh.

4. Mahasiswa mampu melakukan inisialisasi (format) NameNode serta menjalankan, memantau melalui antarmuka Web UI, dan menghentikan layanan daemon HDFS.

5. Mahasiswa mampu mengoperasikan perintah dasar manajemen file dan direktori pada HDFS menggunakan antarmuka command-line (hdfs dfs).

# DASAR TEORI

1. Hadoop Distributed File System (HDFS)<br>
HDFS adalah sistem berkas terdistribusi yang dirancang untuk menyimpan data berukuran besar secara andal dan mengalirkannya (streaming) dengan throughput tinggi ke aplikasi pengguna. Dalam arsitekturnya, HDFS memiliki dua komponen daemon utama yang dikelola dalam praktikum ini, yaitu NameNode (bertugas mengelola metadata sistem berkas, struktur direktori, dan pemetaan blok data) serta DataNode (bertugas menyimpan dan mengambil blok data fisik secara aktual). Selain itu, terdapat Secondary NameNode yang membantu proses checkpointing metadata NameNode. Pada pengaturan klaster tunggal (pseudo-distributed mode), nilai replikasi blok (dfs.replication) umumnya diatur ke 1.   

2. Ekosistem Inti Apache Hadoop<br>
Apache Hadoop menyediakan kerangka kerja pemrosesan dan penyimpanan terdistribusi yang saling terintegrasi melalui empat berkas konfigurasi utama:

- Hadoop Common (core-site.xml): Mengatur konfigurasi dasar sistem, seperti alamat URI sistem berkas default (fs.defaultFS, misalnya hdfs://localhost:9000) dan pengaturan proxy user.

- HDFS (hdfs-site.xml): Mengatur parameter spesifik penyimpanan terdistribusi seperti faktor replikasi data (dfs.replication).

- YARN (yarn-site.xml): Yet Another Resource Negotiator yang bertugas mengelola alokasi sumber daya komputasi (seperti memori kontainer pada NodeManager) dan penjadwalan tugas di dalam klaster.

- MapReduce (mapred-site.xml): Kerangka kerja pemrosesan data paralel yang dijalankan di atas YARN (mapreduce.framework.name).   

3. Komunikasi Antar-Node (SSH dan pdsh)<br>
Dalam sistem terdistribusi, node master harus dapat berkomunikasi dan menjalankan skrip pengendali daemon (seperti start-dfs.sh dan stop-dfs.sh) pada node pekerja maupun localhost tanpa hambatan autentikasi manual. Hal ini dicapai dengan:

- Passwordless SSH: Menggunakan pasangan kunci kriptografi RSA (ssh-keygen) yang didaftarkan ke dalam berkas authorized_keys agar koneksi SSH antar-node berjalan otomatis tanpa meminta kata sandi.

- pdsh (Parallel Distributed Shell): Utilitas baris perintah yang memungkinkan eksekusi perintah secara paralel pada banyak node sekaligus melalui protokol ssh.   

4. Lingkungan Eksekusi Java (JDK) dan Environment Variables <br>
Apache Hadoop dibangun menggunakan bahasa pemrograman Java, sehingga membutuhkan Java Development Kit (JDK 17 untuk sisi server dan JDK 17/21 untuk client) agar proses JVM pada setiap daemon dapat berjalan. Pengaturan variabel lingkungan seperti JAVA_HOME (di dalam hadoop-env.sh) serta PATH (yang mengarah ke direktori bin dan sbin pada $HADOOP_HOME) diperlukan agar sistem operasi dapat mengenali lokasi pustaka Java dan mengeksekusi perintah administrasi Hadoop secara global.   

5. Inisialisasi, Pemantauan, dan Operasi Sistem Berkas HDFS

- Format NameNode (hdfs namenode -format): Proses inisialisasi awal untuk membuat struktur direktori penyimpanan metadata (FSImage) pada NameNode. Proses ini hanya dilakukan satu kali saat instalasi awal karena menjalankannya kembali akan menghapus seluruh data yang sudah tersimpan di HDFS.

- Pemantauan Web UI: Status kesehatan klaster, kapasitas penyimpanan, jumlah blok aktif, dan kondisi DataNode dapat dipantau secara visual melalui antarmuka web bawaan NameNode pada port 9870.

- HDFS FileSystem Shell (hdfs dfs): Antarmuka baris perintah yang menyerupai perintah sistem berkas POSIX/Linux (seperti -ls untuk melihat isi direktori, -mkdir untuk membuat direktori, dan perintah penyalinan berkas dari sistem lokal ke HDFS) untuk mengelola data pengguna di dalam lingkungan HDFS.   