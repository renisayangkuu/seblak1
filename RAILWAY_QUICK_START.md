# 🚀 Railway Quick Start Guide

## 📦 Yang Sudah Disiapkan

✅ Semua file deployment sudah siap!
✅ Database akan auto-initialize
✅ Menu akan auto-seed dengan 3 ukuran seblak
✅ Gambar produk sudah ada di folder `gambar/`

## 🎯 Langkah Deploy (5 Menit)

### 1️⃣ Push ke GitHub

```bash
# Check status
git status

# Add semua file
git add .

# Commit
git commit -m "Ready for Railway deployment"

# Push
git push origin main
```

### 2️⃣ Setup Railway

1. Buka https://railway.app
2. Login dengan GitHub
3. Klik **"New Project"**
4. Pilih **"Deploy from GitHub repo"**
5. Pilih repository: **renisayangkuu/seblak1**
6. Railway akan otomatis detect dan mulai build

### 3️⃣ Set Environment Variables

Di Railway dashboard, klik tab **"Variables"** dan tambahkan:

#### 🔑 Required (WAJIB):

```
TELEGRAM_BOT_TOKEN=<token dari @BotFather>
ADMIN_TELEGRAM_IDS=<ID Telegram Anda dari @userinfobot>
```

#### ⚙️ Optional (bisa pakai default):

```
ADMIN_PASSWORD=admin123
WARUNG_NAME=Seblak Sami
WARUNG_ADDRESS=Jl. Contoh No. 123, Jakarta
WARUNG_DESCRIPTION=Seblak pedas dengan berbagai pilihan ukuran.\nHarga terjangkau, rasa mantap!
BANK_NAME=BCA
BANK_ACCOUNT=1234567890
BANK_ACCOUNT_NAME=Seblak Sami
ONGKIR=10000
```

**Cara mendapatkan token & ID:**
- Token: Chat dengan @BotFather di Telegram → /newbot → ikuti instruksi
- ID: Chat dengan @userinfobot di Telegram → kirim pesan apa saja

### 4️⃣ Deploy & Test

1. Setelah set variables, Railway akan auto-redeploy
2. Tunggu hingga status **"Success"** (2-3 menit)
3. Buka Telegram, cari bot Anda
4. Kirim `/start` - bot harus merespon!

## ✅ Checklist Test

- [ ] Bot merespon `/start`
- [ ] Menu muncul dengan 3 gambar seblak
- [ ] Bisa pesan menu (pilih ukuran)
- [ ] Bisa pilih pickup/delivery
- [ ] Bisa upload bukti transfer
- [ ] Admin bisa login dengan `/loginadmin`
- [ ] Admin bisa konfirmasi pembayaran

## 🔧 Troubleshooting

### Bot tidak merespon?
1. Cek logs di Railway dashboard
2. Pastikan `TELEGRAM_BOT_TOKEN` benar
3. Pastikan bot sudah di-start dengan @BotFather

### Gambar tidak muncul?
1. Pastikan folder `gambar/` ada di repository
2. Pastikan ada 3 gambar di folder
3. Redeploy jika perlu

### Environment variables tidak terbaca?
1. Pastikan sudah save di Railway
2. Redeploy setelah menambah variables

## 📊 Monitoring

- **Logs**: Railway dashboard → tab "Deployments" → klik deployment → "View Logs"
- **Status**: Railway dashboard → lihat status service (running/stopped)
- **Usage**: Railway dashboard → tab "Metrics" → lihat CPU/Memory usage

## 💰 Biaya

Railway Free Tier:
- $5 credit gratis per bulan
- Cukup untuk bot kecil-menengah
- Bot akan sleep setelah tidak ada aktivitas
- Auto-wake saat ada request dari Telegram

## 📝 Update Bot

Setiap kali ada perubahan code:

```bash
git add .
git commit -m "Update: <deskripsi>"
git push origin main
```

Railway akan otomatis redeploy!

## 🎉 Selesai!

Bot Anda sekarang berjalan 24/7 di cloud!

**Dokumentasi Lengkap:**
- [DEPLOYMENT.md](DEPLOYMENT.md) - Panduan detail
- [CHECKLIST_DEPLOY.md](CHECKLIST_DEPLOY.md) - Checklist lengkap
- [README.md](README.md) - Dokumentasi bot

**Need Help?**
- Railway Docs: https://docs.railway.app
- Telegram Bot API: https://core.telegram.org/bots/api
