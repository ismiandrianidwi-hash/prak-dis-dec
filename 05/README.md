# PRAKTIKUM MINGGU 05

Nama : Dwi Ismi Andriani <br>
Nim : 255410012 <br>
Kelas : Informatika - 1 <br>

Laporan praktikum ke - 05 <br>
Topik : Fault Tolerance <br>

# TUJUAN

1. Memahami Konsep Fault Tolerance dan High Availability: Mahasiswa mampu memahami prinsip dasar toleransi kesalahan (fault tolerance) dan peningkatan ketersediaan layanan (high availability) pada sistem terdistribusi.   
2. Mengimplementasikan Load Balancing dengan Nginx dan Docker: Mahasiswa mampu melakukan scaling aplikasi web berbasis ASGI (Blacksheep) menjadi beberapa instance serta mengonfigurasikan Nginx sebagai reverse proxy load balancer.   
3. Memahami Mekanisme Failure Detection: Mahasiswa mampu mengidentifikasi status kegagalan komponen sistem terdistribusi menggunakan metode Heartbeat.   
4. Menerapkan Pola Penanganan Kegagalan (Retry & Circuit Breaker): Mahasiswa mampu menerapkan teknik retry menggunakan library tenacity dan memahami mekanisme kerja Circuit Breaker untuk mencegah kegagalan berantai (cascading failure) pada microservices.  

# DASAR TEORI

1. High Availability dan Load Balancing <br>

Dalam arsitektur sistem terdistribusi, High Availability (HA) bertujuan untuk memastikan bahwa sistem dapat terus beroperasi secara andal tanpa mengalami downtime yang signifikan. Salah satu pendekatan utama untuk mencapai HA adalah dengan menerapkan Load Balancing. <br> 

Load Balancing merupakan teknik mendistribusikan beban kerja (incoming traffic) secara merata ke beberapa unit server (instances). Dengan adanya Nginx sebagai reverse proxy, permintaan dari pengguna akan diarahkan ke upstream server yang tersedia secara bergantian (misalnya dengan metode Round-Robin), sehingga tidak ada satu server pun yang mengalami beban berlebih (overload).

2. Containerization dan Horizontal Scaling <br>

Horizontal Scaling adalah strategi menambahkan jumlah instance aplikasi untuk menangani peningkatan lalu lintas data. Penggunaan container seperti Docker dan alat pengelolanya (Docker Compose) mempermudah replikasi aplikasi secara konsisten. Melalui opsi perintah --scale, infrastruktur dapat menambah atau mengurangi jumlah container aplikasi secara dinamis tanpa mengubah konfigurasi kode utama.

3. Failure Detection dan Protokol Heartbeat <br>

Failure Detection merupakan proses penting dalam sistem terdistribusi untuk menentukan apakah suatu komponen atau layanan telah mengalami gangguan/gagal (crash). Salah satu pendekatan dasar yang digunakan adalah Protokol Heartbeat. Pemantau akan mengirimkan sinyal periodik ke server target; jika dalam tenggat waktu tertentu server tidak memberikan respons, maka server tersebut dianggap down atau tidak responsif.

4. Retry Mechanism (Mekanisme Pemulihan Koneksi) <br>

Kegagalan dalam sistem terdistribusi sering kali bersifat sementara (transient failures), seperti gangguan jaringan singkat. Retry Mechanism memfasilitasi aplikasi untuk mencoba kembali koneksi yang gagal beberapa kali sebelum melempar exception atau menganggap layanan tujuan benar-benar mati. Di Python, hal ini dapat dikelola secara efektif menggunakan library seperti tenacity

5. Pattern Circuit Breaker <br>

Circuit Breaker adalah pola desain (design pattern) pada arsitektur microservices yang berfungsi menghentikan pemanggilan ke layanan eksternal jika layanan tersebut terdeteksi mengalami kegagalan secara berulang. Tujuan utamanya adalah mencegah cascading failure (kegagalan berantai yang merambat ke layanan lain). <br>

Pola ini bekerja berdasarkan tiga status utama (State Machine): <br>

<!-- Menghasilkan: ○ --> Closed: Kondisi normal. Permintaan diizinkan lewat sambil terus dipantau. Jika rasio kegagalan melampaui batas ambang (threshold), status berubah menjadi Open.
<!-- Menghasilkan: ○ --> Open: Permintaan baru langsung ditolak secara instan (fast-fail) tanpa menghubungi layanan target untuk memberi waktu bagi layanan tersebut pulih.
<!-- Menghasilkan: ○ --> Half-Open: Setelah melewati batas waktu tunggu (timeout), sirkuit mencoba mengirimkan sejumlah kecil permintaan uji coba. Jika permintaan tersebut berhasil, status kembali ke Closed; namun jika gagal, status akan kembali ke Open.   

# PRAKTIK

# KESIMPULAN