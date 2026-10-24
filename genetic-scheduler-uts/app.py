import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scheduler_logic import GeneticScheduler

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="OptimaSchedule - AG Penjadwalan Kuliah",
    page_icon="📅",
    layout="wide"
)

st.title("📅 OptimaSchedule: Penjadwalan Kuliah Berbasis Algoritma Genetika")
st.markdown("Unggah data mata kuliah kustommu (format CSV atau Excel) atau gunakan data bawaan sistem.")

# --- SIDEBAR: PENGATURAN PARAMETER & DATA ---
st.sidebar.header("⚙️ Konfigurasi & Parameter")

# Pilihan Sumber Data
data_source = st.sidebar.radio("Sumber Data Mata Kuliah:", ["Gunakan Data Bawaan (Demo)", "Unggah File Kustom (CSV/Excel)"])

courses_data = []

if data_source == "Unggah File Kustom (CSV/Excel)":
    uploaded_file = st.sidebar.file_uploader("Unggah file data matkul", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)
            
            # Validasi kolom wajib
            required_cols = ["id", "nama", "sks", "dosen", "rombel"]
            if all(col in df_upload.columns for col in required_cols):
                courses_data = df_upload.to_dict(orient="records")
                st.sidebar.success(f"Berhasil memuat {len(courses_data)} mata kuliah dari file!")
            else:
                st.sidebar.error(f"Format file salah! Kolom harus mencakup: {required_cols}")
        except Exception as e:
            st.sidebar.error(f"Gagal membaca file: {e}")
    else:
        st.sidebar.info("Silakan unggah file CSV/Excel terlebih dahulu.")
else:
    # Data Bawaan Default
    courses_data = [
        {"id": "MK01", "nama": "Algoritma Genetika", "sks": 3, "dosen": "Dr. Budi", "rombel": "TI-A"},
        {"id": "MK02", "nama": "Basis Data II", "sks": 3, "dosen": "Bu Ani", "rombel": "TI-A"},
        {"id": "MK03", "nama": "Pemrograman Web", "sks": 3, "dosen": "Pak Eko", "rombel": "TI-A"},
        {"id": "MK04", "nama": "Grafika Komputer", "sks": 3, "dosen": "Pak Citra", "rombel": "TI-A"},
        {"id": "MK05", "nama": "Statistika", "sks": 2, "dosen": "Bu Dewi", "rombel": "TI-A"},
        {"id": "MK06", "nama": "Komputasi Paralel", "sks": 3, "dosen": "Dr. Budi", "rombel": "TI-B"},
        {"id": "MK07", "nama": "Teori Bahasa Otomata", "sks": 3, "dosen": "Pak Citra", "rombel": "TI-B"},
        {"id": "MK08", "nama": "Manajemen Proyek", "sks": 2, "dosen": "Bu Ani", "rombel": "TI-B"},
    ]

# Parameter AG di Sidebar
pop_size = st.sidebar.slider("Ukuran Populasi (Population Size)", 20, 200, 50, 10)
max_gen = st.sidebar.slider("Maksimal Generasi", 50, 500, 100, 25)
cx_prob = st.sidebar.slider("Probabilitas Crossover", 0.1, 1.0, 0.8, 0.05)
mut_prob = st.sidebar.slider("Probabilitas Mutasi", 0.01, 0.3, 0.1, 0.01)

# Daftar Ruangan & Slot Waktu Statis
DEFAULT_ROOMS = ["Lab Komputer 1", "Ruang Teori A1", "Ruang Teori A2"]
DEFAULT_SLOTS = [
    "Senin 08:00", "Senin 10:30", "Senin 13:30",
    "Selasa 08:00", "Selasa 10:30", "Selasa 13:30",
    "Rabu 08:00", "Rabu 10:30", "Rabu 13:30",
    "Kamis 08:00", "Kamis 10:30", "Kamis 13:30",
    "Jumat 08:00", "Jumat 10:30", "Jumat 13:30"
]

# --- TAMPILAN UTAMA (TABS) ---
tab1, tab2, tab3 = st.tabs(["🚀 Jalankan Optimasi", "📊 Lihat Data Mata Kuliah", "ℹ️ Panduan Format File"])

with tab1:
    st.subheader("Eksekusi Algoritma Penjadwalan")
    
    if len(courses_data) == 0:
        st.warning("⚠️ Belum ada data mata kuliah yang dimuat. Silakan pilih data bawaan atau unggah file di sidebar.")
    else:
        st.write(f"Total mata kuliah yang akan dijadwalkan: **{len(courses_data)} sesi**")
        
        if st.button("Mulai Jalankan AG", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Panggil kelas logika dari file terpisah
            scheduler = GeneticScheduler(
                courses=courses_data,
                rooms=DEFAULT_ROOMS,
                slots=DEFAULT_SLOTS,
                pop_size=pop_size,
                max_gen=max_gen,
                cx_prob=cx_prob,
                mut_prob=mut_prob
            )
            
            best_ind, best_fit, h_best, h_avg, sol_gen = scheduler.run(progress_bar, status_text)
            
            st.success("Optimasi Selesai!")
            
            # Metrik Hasil
            col1, col2, col3 = st.columns(3)
            col1.metric("Fitness Terbaik", f"{best_fit:.4f}")
            col2.metric("Status Jadwal", "Valid (Bebas Bentrok)" if best_fit == 1.0 else "Ada Pelanggaran Minor")
            col3.metric("Solusi Ditemukan pada Gen", sol_gen if sol_gen is not None else "> Max Gen")
            
            # Tabel Hasil Jadwal
            st.subheader("📋 Jadwal Kuliah Optimal Terpilih")
            schedule_data = []
            loop_length = min(len(courses_data), len(best_ind))
            
            for idx in range(loop_length):
                course = courses_data[idx]
                schedule_data.append({
                    "Kode": course["id"],
                    "Mata Kuliah": course["nama"],
                    "SKS": course["sks"],
                    "Dosen": course["dosen"],
                    "Rombel": course["rombel"],
                    "Hari & Slot Waktu": best_ind[idx]["slot"],
                    "Ruangan": best_ind[idx]["room"]
                })
            
            df_schedule = pd.DataFrame(schedule_data)
            st.dataframe(df_schedule, use_container_width=True)
            
            # Tombol Ekspor CSV
            csv = df_schedule.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Unduh Jadwal ke CSV",
                data=csv,
                file_name="jadwal_kuliah_optimal.csv",
                mime="text/csv",
            )
            
            # Grafik Konvergensi Fitness
            st.subheader("📈 Grafik Konvergensi Fitness per Generasi")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(h_best, label="Fitness Terbaik", color="blue", linewidth=2)
            ax.plot(h_avg, label="Fitness Rata-rata", color="orange", linestyle="--")
            ax.set_xlabel("Generasi")
            ax.set_ylabel("Nilai Fitness")
            ax.set_title("Grafik Peningkatan Kualitas Solusi Algoritma Genetika")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

with tab2:
    st.subheader("Pratinjau Data Mata Kuliah Aktif")
    if len(courses_data) > 0:
        st.dataframe(pd.DataFrame(courses_data), use_container_width=True)
    else:
        st.info("Belum ada data.")

with tab3:
    st.subheader("📄 Panduan Format File Unggahan (.csv / .xlsx)")
    st.markdown("""
    Jika kamu ingin mengunggah data sendiri, pastikan file memiliki kolom dengan nama header berikut:
    * `id`: Kode unik mata kuliah (contoh: `MK01`)
    * `nama`: Nama mata kuliah (contoh: `Pemrograman Web`)
    * `sks`: Jumlah SKS dalam bentuk angka (contoh: `3`)
    * `dosen`: Nama dosen pengampu (contoh: `Dr. Budi`)
    * `rombel`: Kelas atau rombongan mahasiswa (contoh: `TI-A`)
    """)