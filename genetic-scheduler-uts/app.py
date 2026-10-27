import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scheduler_logic import GeneticScheduler

st.set_page_config(page_title="OptimaSchedule - AG Penjadwalan Kuliah", page_icon="📅", layout="wide")

st.title("📅 OptimaSchedule: Penjadwalan Kuliah Berbasis Algoritma Genetika")
st.markdown("Sistem Penjadwalan Otomatis dengan Kendala Kapasitas Ruangan & Berbagai Operator Genetika.")

# --- SIDEBAR: PENGATURAN PARAMETER & OPERATOR ---
st.sidebar.header("⚙️ Konfigurasi & Operator AG")

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
            
            required_cols = ["id", "nama", "sks", "dosen", "rombel", "kuota"]
            if all(col in df_upload.columns for col in required_cols):
                courses_data = df_upload.to_dict(orient="records")
                st.sidebar.success(f"Berhasil memuat {len(courses_data)} mata kuliah!")
            else:
                st.sidebar.error(f"Kolom wajib di file: {required_cols}")
        except Exception as e:
            st.sidebar.error(f"Gagal membaca file: {e}")
else:
    # Data Bawaan dengan atribut kuota kelas
    courses_data = [
        {"id": "MK01", "nama": "Metodologi Penelitian A", "sks": 3, "dosen": "Felicia Sylviana", "rombel": "TI-5A", "kuota": 35},
        {"id": "MK02", "nama": "Metodologi Penelitian B", "sks": 3, "dosen": "Devi Karolita", "rombel": "TI-5B", "kuota": 30},
        {"id": "MK03", "nama": "Analisis & Desain PL A", "sks": 3, "dosen": "Ressa Priskila", "rombel": "TI-5A", "kuota": 35},
        {"id": "MK04", "nama": "Analisis & Desain PL B", "sks": 3, "dosen": "Deddy Ronaldo", "rombel": "TI-5B", "kuota": 30},
        {"id": "MK05", "nama": "Keamanan Data A", "sks": 3, "dosen": "Agus Sehatman", "rombel": "TI-5A", "kuota": 35},
        {"id": "MK06", "nama": "Keamanan Data B", "sks": 3, "dosen": "Septian Geges", "rombel": "TI-5B", "kuota": 30},
        {"id": "MK07", "nama": "Pengolahan Citra A", "sks": 3, "dosen": "Deddy Ronaldo", "rombel": "TI-5A", "kuota": 35},
        {"id": "MK08", "nama": "Pengolahan Citra B", "sks": 3, "dosen": "Nahumi Nugraha", "rombel": "TI-5B", "kuota": 30},
        {"id": "MK09", "nama": "Penjaminan Mutu PL", "sks": 3, "dosen": "Deddy Ronaldo", "rombel": "TI-7", "kuota": 40},
        {"id": "MK10", "nama": "Kompleksitas Algoritma A", "sks": 3, "dosen": "Agus Sehatman", "rombel": "TI-5A", "kuota": 35},
    ]

# Pilihan Operator Tambahan Sesuai Panduan UTS
st.sidebar.markdown("---")
st.sidebar.subheader("🧬 Pilihan Operator AG")
selection_method = st.sidebar.selectbox("Metode Seleksi", ["Tournament", "Roulette Wheel"])
crossover_method = st.sidebar.selectbox("Metode Crossover", ["Single-Point", "Uniform"])

# Parameter AG
pop_size = st.sidebar.slider("Ukuran Populasi", 20, 200, 50, 10)
max_gen = st.sidebar.slider("Maksimal Generasi", 50, 500, 100, 25)
cx_prob = st.sidebar.slider("Probabilitas Crossover", 0.1, 1.0, 0.8, 0.05)
mut_prob = st.sidebar.slider("Probabilitas Mutasi", 0.01, 0.3, 0.1, 0.01)

# Data Ruangan beserta Kapasitasnya (untuk validasi kendala kapasitas)
DEFAULT_ROOMS = [
    {"nama": "FT6", "kapasitas": 50},
    {"nama": "FT7", "kapasitas": 50},
    {"nama": "FT8", "kapasitas": 50},
    {"nama": "FT9", "kapasitas": 90},
    {"nama": "audit", "kapasitas": 120},
]

DEFAULT_SLOTS = [
    # Senin
    "Senin 07:00", "Senin 09:30", "Senin 12:00", "Senin 14:30", "Senin 16:30",
    # Selasa
    "Selasa 07:00", "Selasa 09:30", "Selasa 12:00", "Selasa 14:30", "Selasa 16:30",
    # Rabu
    "Rabu 07:00", "Rabu 09:30", "Rabu 12:00", "Rabu 14:30", "Rabu 16:30",
    # Kamis
    "Kamis 07:00", "Kamis 09:30", "Kamis 12:00", "Kamis 14:30", "Kamis 16:30",
    # Jumat
    "Jumat 07:00", "Jumat 09:30", "Jumat 12:00", "Jumat 14:30", "Jumat 16:30"
]

# --- TAMPILAN UTAMA ---
tab1, tab2, tab3 = st.tabs(["🚀 Jalankan Optimasi", "📊 Data Mata Kuliah & Ruangan", "ℹ️ Informasi Kendala"])

with tab1:
    st.subheader("Eksekusi Algoritma Penjadwalan")
    if len(courses_data) == 0:
        st.warning("⚠️ Data mata kuliah kosong.")
    else:
        if st.button("Mulai Jalankan AG", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            scheduler = GeneticScheduler(
                courses=courses_data,
                rooms=DEFAULT_ROOMS,
                slots=DEFAULT_SLOTS,
                pop_size=pop_size,
                max_gen=max_gen,
                cx_prob=cx_prob,
                mut_prob=mut_prob,
                selection_method=selection_method,
                crossover_method=crossover_method
            )
            
            best_ind, best_fit, h_best, h_avg, sol_gen = scheduler.run(progress_bar, status_text)
            
            st.success("Optimasi Selesai!")
            
            # --- TAMPILAN METRIK HASIL (TERMASUK FITNESS RATA-RATA POPULASI AKHIR) ---
            final_avg_fitness = h_avg[-1]  # Nilai fitness rata-rata dari generasi terakhir
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Fitness Terbaik Akhir", f"{best_fit:.4f}")
            col2.metric("Fitness Rata-Rata Akhir", f"{final_avg_fitness:.4f}")
            col3.metric("Status Jadwal", "Valid (Bebas Bentrok)" if best_fit == 1.0 else "Ada Pelanggaran")
            col4.metric("Solusi Ditemukan Gen Ke-", sol_gen if sol_gen is not None else "> Max Gen")
            
            # Tabel Ringkasan Hasil Evaluasi
            st.info(f"📌 **Ringkasan Hasil Evaluasi:** Dari populasi sebanyak **{pop_size}** individu pada generasi terakhir, rata-rata tingkat fitness populasi mencapai **{final_avg_fitness:.4f}**, dengan nilai individu terbaik mencapai **{best_fit:.4f}**.")
            
            # Tabel Hasil Jadwal Kuliah
            st.subheader("📋 Jadwal Kuliah Optimal Terpilih")
            schedule_data = []
            for idx in range(min(len(courses_data), len(best_ind))):
                course = courses_data[idx]
                schedule_data.append({
                    "Kode": course["id"],
                    "Mata Kuliah": course["nama"],
                    "SKS": course["sks"],
                    "Dosen": course["dosen"],
                    "Rombel": course["rombel"],
                    "Kuota": course["kuota"],
                    "Hari & Slot": best_ind[idx]["slot"],
                    "Ruangan": best_ind[idx]["room"]
                })
            
            df_schedule = pd.DataFrame(schedule_data)
            st.dataframe(df_schedule, use_container_width=True)
            
            # Ekspor CSV
            csv = df_schedule.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Unduh Jadwal ke CSV", data=csv, file_name="jadwal_optimal_uts.csv", mime="text/csv")
            
            # Grafik Konvergensi Fitness
            st.subheader("📈 Grafik Konvergensi Fitness per Generasi")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(h_best, label="Fitness Terbaik (Best Fitness)", color="blue", linewidth=2)
            ax.plot(h_avg, label="Fitness Rata-rata (Avg Fitness)", color="orange", linestyle="--")
            ax.set_xlabel("Generasi")
            ax.set_ylabel("Nilai Fitness")
            ax.set_title("Perkembangan Kualitas Populasi Selama Proses Evolusi")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

with tab2:
    st.subheader("Data Referensi Ruangan & Kapasitas")
    st.dataframe(pd.DataFrame(DEFAULT_ROOMS), use_container_width=True)
    st.subheader("Data Mata Kuliah Aktif")
    st.dataframe(pd.DataFrame(courses_data), use_container_width=True)

with tab3:
    st.markdown("""
    ### Penambahan Indikator Layar:
    * **Fitness Terbaik Akhir:** Menampilkan nilai fitness dari individu terbaik di generasi terakhir.
    * **Fitness Rata-Rata Akhir:** Menampilkan rata-rata kualitas seluruh kromosom dalam populasi pada generasi terakhir.
    """)
