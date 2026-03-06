# Panduan Deploy ke Railway

## Persiapan

1. Pastikan semua file sudah di-push ke GitHub repository: https://github.com/renisayangkuu/seblak1

2. Buat akun di [Railway.app](https://railway.app) jika belum punya

## Langkah Deploy

### 1. Buat Project Baru di Railway

- Login ke Railway
- Klik "New Project"
- Pilih "Deploy from GitHub repo"
- Pilih repository: `renisayangkuu/seblak1`
- Railway akan otomatis detect dan build project

### 2. Setup Environment Variables

Di Railway dashboard, masuk ke tab "Variables" dan tambahkan:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
ADMIN_TELEGRAM_IDS=your_telegram_id_here
ADMIN_PASSWORD=your_admin_password
WARUNG_NAME=Warung Seblak Kita
WARUNG_ADDRESS=Jl. Contoh No. 123, Jakarta
WARUNG_DESCRIPTION=Seblak pedas dengan berbagai pilihan ukuran.\nHarga terjangkau, rasa mantap!
BANK_NAME=BCA
BANK_ACCOUNT=1234567890
BANK_ACCOUNT_NAME=Warung Seblak Kita
ONGKIR=10000
```

**Penting:**
- `TELEGRAM_BOT_TOKEN`: Dapatkan dari @BotFather di Telegram
- `ADMIN_TELEGRAM_IDS`: ID Telegram Anda (bisa dapat dari @userinfobot)
- Ganti semua value sesuai kebutuhan Anda

### 3. Deploy

- Railway akan otomatis deploy setelah environment variables diset
- Tunggu proses build selesai (biasanya 2-3 menit)
- Cek logs untuk memastikan bot berjalan dengan baik

### 4. Setup Database & Menu

Setelah bot berjalan, database SQLite akan otomatis dibuat. Untuk menambahkan menu:

**Opsi 1: Jalankan seed script via Railway CLI**
```bash
railway run python seed_menu.py
```

**Opsi 2: Manual via Python**
Buat temporary script untuk insert menu langsung dari bot.py

### 5. Upload Gambar Menu

Karena Railway menggunakan ephemeral filesystem, ada 2 opsi:

**Opsi A: Embed gambar di repository (Recommended)**
- Pastikan folder `gambar/` sudah ada di repository
- Push semua gambar ke GitHub
- Railway akan copy gambar saat deploy

**Opsi B: Gunakan external storage (untuk production)**
- Upload gambar ke cloud storage (Cloudinary, AWS S3, dll)
- Update path foto di database dengan URL

## Monitoring

- Cek logs di Railway dashboard untuk troubleshooting
- Bot akan auto-restart jika crash (max 10 retries)

## Catatan Penting

1. **Database**: SQLite di Railway bersifat ephemeral (data hilang saat redeploy). Untuk production, pertimbangkan:
   - Railway PostgreSQL (gratis tier available)
   - External database service

2. **File Upload**: Bukti transfer yang diupload customer akan hilang saat redeploy. Solusi:
   - Simpan file_id Telegram (sudah implemented)
   - Atau gunakan cloud storage

3. **Cost**: Railway free tier cukup untuk bot kecil-menengah

## Troubleshooting

**Bot tidak merespon:**
- Cek logs di Railway dashboard
- Pastikan TELEGRAM_BOT_TOKEN benar
- Pastikan bot sudah di-start dengan /start di Telegram

**Database error:**
- Railway akan auto-create database saat pertama kali run
- Jika error, coba redeploy

**Gambar tidak muncul:**
- Pastikan folder gambar/ ada di repository
- Cek path di seed_menu.py

## Update Bot

Setiap kali push ke GitHub, Railway akan otomatis redeploy (jika auto-deploy enabled).

```bash
git add .
git commit -m "Update bot"
git push origin main
```

Railway akan detect changes dan redeploy otomatis.
