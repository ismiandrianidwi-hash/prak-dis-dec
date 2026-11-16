# PRAKTIKUM MINGGU 06

Nama : Dwi Ismi Andriani <br>
Nim : 255410012 <br>
Kelas : Informatika - 1 <br>

Laporan praktikum ke - 06 <br>
Topik : Distributed File System - HDFS <br>

# TUJUAN
1. Memahami konsep dasar sistem berkas terdistribusi (Distributed File System) menggunakan Apache Hadoop Distributed File System (HDFS).   
2. Mampu melakukan instalasi dan konfigurasi lingkungan Apache Hadoop 3.5.0 dalam mode pseudo-distributed (single-node) beserta dependensinya (JDK, SSH passwordless, dan pdsh).

3. Mampu mengelola daemon HDFS (NameNode, DataNode, dan Secondary NameNode) serta memantau status klaster melalui antarmuka web (Web UI).

4. Mampu mengoperasikan perintah dasar sistem berkas HDFS (hdfs dfs) untuk manajemen direktori dan pengiriman data dari penyimpanan lokal ke HDFS.

# DASAR TEORI

#### 1. Sistem Berkas Terdistribusi dan Apache Hadoop
Sistem berkas terdistribusi (Distributed File System) memungkinkan penyimpanan dan pengelolaan data berukuran besar secara tersebar di berbagai mesin (node), namun tetap dapat diakses oleh pengguna seolah-olah berada pada satu sistem berkas lokal. Apache Hadoop merupakan kerangka kerja (framework) sumber terbuka yang dirancang untuk komputasi terdistribusi dan penyimpanan data skala besar, dengan komponen utama penyimpanan berupa HDFS (Hadoop Distributed File System) dan komponen manajemen sumber daya berupa YARN (Yet Another Resource Negotiator).  

#### 2. Arsitektur dan Komponen HDFS
HDFS bekerja menggunakan arsitektur master-slave yang terdiri dari beberapa layanan latar belakang (daemon) utama:

- NameNode (Master): Bertugas mengelola metadata sistem berkas, seperti struktur direktori, nama berkas, izin akses, serta pemetaan blok data ke masing-masing DataNode

- DataNode (Worker): Bertugas menyimpan blok-blok data fisik secara aktual dan melayani permintaan pembacaan maupun penulisan data dari klien.

- Secondary NameNode: Membantu NameNode dalam melakukan checkpointing (penggabungan fsimage dan edit logs) agar ukuran log transaksi tidak membengkak.

Pada konfigurasi pseudo-distributed (single-node), seluruh daemon tersebut dijalankan pada satu komputer lokal (localhost) dengan faktor replikasi blok (dfs.replication) diatur ke nilai 1 karena hanya terdapat satu node penyimpanan.

#### 3. Infrastruktur Pendukung Konfigurasi Hadoop
Agar klaster Hadoop dapat beroperasi dengan baik pada lingkungan Linux, diperlukan beberapa komponen pendukung:

- Java Development Kit (JDK): Hadoop dibangun di atas bahasa pemrograman Java sehingga membutuhkan JDK (seperti JDK 17 atau 21) yang didefinisikan melalui variabel lingkungan JAVA_HOME.

- SSH (Secure Shell) & pdsh (Parallel Distributed Shell): Skrip manajemen Hadoop (seperti start-dfs.sh dan stop-dfs.sh) menggunakan koneksi SSH tanpa kata sandi (passwordless SSH berbasis pasangan kunci RSA) serta pdsh untuk mengontrol dan mengeksekusi perintah pada node secara paralel, termasuk pada localhost. 

#### 4. Berkas Konfigurasi Utama Hadoop
Pengaturan perilaku klaster Hadoop ditentukan melalui berkas konfigurasi XML di dalam direktori $HADOOP_HOME/etc/hadoop/: 

- core-site.xml: Mendefinisikan alamat URI utama sistem berkas HDFS (misalnya hdfs://localhost:9000) serta pengaturan izin proxy user.
- hdfs-site.xml: Mengatur parameter spesifik HDFS, seperti jumlah replikasi blok data (dfs.replication).
- mapred-site.xml & yarn-site.xml: Mengatur kerangka eksekusi pemrosesan paralel menggunakan YARN beserta alokasi memori kontainer (resource memory dan minimum allocation).

#### 5. Manajemen dan Antarmuka HDFS
Sebelum digunakan pertama kali, direktori penyimpanan metadata NameNode harus diinisialisasi menggunakan perintah hdfs namenode -format. Setelah layanan HDFS aktif, pemantauan kondisi klaster (kapasitas penyimpanan, status node, dan jumlah blok) dapat dilakukan melalui antarmuka web pada port 9870, sedangkan manipulasi berkas dilakukan melalui antarmuka baris perintah menggunakan utilitas hdfs dfs (seperti -mkdir untuk membuat direktori, -put untuk menyalin berkas lokal ke HDFS, dan -ls untuk melihat isi direktori).<br>

Silakan tinjau bagian Tujuan dan Dasar Teori di atas. Jika sudah sesuai dengan format laporan di kampus Anda (atau jika ada penyesuaian gaya bahasa), beri tahu saya kapan saja Anda siap untuk melanjutkan ke bagian Langkah-Langkah Pengerjaan Laporan dan analisis hasil praktikumnya.

# PRAKTIK
## 1. Unduh Apache Hadoop

<img src="images/01_Pert 6.png" width="700"> <br>

Pembahasan : <br>

## 2. Instalasi Apache Hadoop 
