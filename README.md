# 📅 OptimaSchedule - Sistem Penjadwalan Kuliah Berbasis Algoritma Genetika (UTS)

Sistem penjadwalan kuliah otomatis berbasis **Algoritma Genetika (AG)** dari nol (tanpa library AG instan seperti DEAP/PyGAD). Dibuat untuk memenuhi Tugas Proyek Kelompok Mata Kuliah Algoritma Genetika (Tahap 1 UTS), Program Studi S-1 Teknik Informatika, Universitas Palangka Raya.

---

## 👥 Anggota Kelompok & Pembagian Peran

* **Hadi Setiawan** (2430205030016) - *Programmer Inti AG*
* **[Nama Anggota 2]** ([NIM]) - *Ketua / Analis Masalah*
* **[Nama Anggota 3]** ([NIM]) - *Programmer Fitness & Validasi*
* **[Nama Anggota 4]** ([NIM]) - *Analis Eksperimen*
* **[Nama Anggota 5]** ([NIM]) - *Penulis & Presenter*

**Dosen Pengampu / Kolaborator Repositori:** Novera Kristianti, S.T., M.T. (`noverara@gmail.com`)

---

## 🚀 Fitur Utama Application (Tahap UTS)

1. **Implementasi AG Murni (Custom):** Operator seleksi (*tournament selection*), *single-point crossover*, mutasi acak, dan mekanisme elitisme ditulis secara independen dari nol.
2. **Unggah Data Kustom:** Mendukung *upload* data mata kuliah berbasis format CSV maupun Excel (.xlsx).
3. **Pemeriksaan Kendala Keras (*Hard Constraints*):** Penalti otomatis untuk mencegah bentrok dosen, bentrok ruangan, dan bentrok rombongan belajar (rombel) mahasiswa.
4. **Visualisasi Interaktif:** Menampilkan grafik konvergensi fitness per generasi dan antarmuka web berbasis Streamlit.
5. **Ekspor Hasil:** Hasil jadwal kuliah optimal dapat langsung diunduh dalam format file CSV.

---

## 📂 Struktur Repositori

```text
├── app.py                   # Interface utama aplikasi (Streamlit UI)
├── scheduler_logic.py       # Kelas & logika inti Algoritma Genetika
├── data_matkul_sem5_7.csv   # Sample dataset mata kuliah (Semester 5 & 7 S-1 TI UPR)
├── requirements.txt         # Daftar dependensi library Python
└── README.md                # Dokumentasi proyek


## 🛠️ Prasyarat & Instalasi
1. **Clone Repositori:** Salin link yang ada pada tombol "Code", kemudian lakukan clone dengan cara buka terminal dan masukkan link yang tadi dalam format berikut "git clone [https://github.com/USERNAME/NAMA-REPOSITORI.git](https://github.com/USERNAME/NAMA-REPOSITORI.git)"
cd NAMA-REPOSITORI
2. **Instalasi Dependensi:** Lakukan instalasi library-library yang dibutuhkan jika belum ada "pip install streamlit pandas numpy matplotlib openpyxl".
3. **Jalankan Program:** Buka terminal lalu masukan perintah "streamlit run app.py", dengan perintah tersebut browser akan otomatis terbuka dan menampilkan antarmuka aplikasi pada alamat.

## 📖 Panduan Penggunaan Aplikasi
1. Pilih Sumber Data:
   - Di panel sebelah kiri (sidebar), pilih opsi "Unggah File Kustom (CSV/Excel)" untuk mengunggah file data_matkul_sem5_7.csv atau pilih "Gunakan Data Bawaan (Demo)".
2. Atur Parameter Algoritma:
   - entukan Ukuran Populasi, Maksimal Generasi, Probabilitas Crossover, dan Probabilitas Mutasi sesuai skenario pengujian.
3. Jalankan Optimasi:
   - Buka tab "🚀 Jalankan Optimasi" dan klik tombol "Mulai Jalankan AG".
   - Tunggu proses evolusi selesai hingga progress bar mencapai 100%.
4. Analisis Hasil & Unduh:
   - Periksa nilai Fitness Terbaik (nilai 1.0 menandakan jadwal bebas bentrok 100%).
   - Lihat tabel jadwal hasil optimasi dan unduh file hasil jadwal melalui tombol "📥 Unduh Jadwal ke CSV".
   - Amati Grafik Konvergensi Fitness untuk menganalisis kecepatan konvergensi algoritma.
