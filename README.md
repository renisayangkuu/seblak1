# 🏪 Bot Telegram Toko Kelontong

Bot Telegram untuk toko kelontong dengan fitur pemesanan dan pembayaran lengkap.

## ✨ Fitur

### Customer
- 🛒 Lihat produk dengan kategori
- 📦 Pesan produk (sembako, makanan, snack, dll)
- 📍 Pilih metode pengambilan (pickup/delivery)
- 💳 Upload bukti transfer
- 📦 Cek status pesanan real-time

### Admin
- 📋 Kelola pesanan masuk
- ✅ Konfirmasi pembayaran
- 🔄 Update status pesanan
- 📊 Generate laporan harian PDF

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment
Copy `.env.example` ke `.env` dan isi:
```env
TELEGRAM_BOT_TOKEN=your_bot_token
ADMIN_TELEGRAM_IDS=your_telegram_id
ADMIN_PASSWORD=admin123
WARUNG_NAME=Toko Kelontong Berkah
BANK_NAME=BCA
BANK_ACCOUNT=1234567890
BANK_ACCOUNT_NAME=Toko Kelontong Berkah
ONGKIR=10000
```

### 3. Inisialisasi Database
```bash
python seed_menu.py
```

### 4. Jalankan Bot
```bash
python bot.py
```

## 📦 Produk Default

Bot sudah include 14 produk toko kelontong:
- 🍚 Sembako: Beras, Minyak, Gula
- 🥫 Makanan & Minuman: Indomie, Teh, Susu
- 🧼 Kebutuhan Rumah Tangga: Sabun, Detergen, Tissue
- 🍪 Snack: Chitato, Biskuit
- 🧴 Perlengkapan Mandi: Sabun Mandi, Shampoo, Pasta Gigi

Edit `seed_menu.py` untuk menambah/mengubah produk.

## 🌐 Deploy ke Railway

### Quick Deploy:
1. Push ke GitHub
2. Buat project di [Railway.app](https://railway.app)
3. Connect repository
4. Set environment variables
5. Deploy!

Lihat [RAILWAY_QUICK_START.md](RAILWAY_QUICK_START.md) untuk panduan lengkap.

## 📝 Command Bot

### Customer:
- `/start` - Mulai bot dan lihat produk
- `/pesanan` - Cek status pesanan

### Admin:
- `/loginadmin` - Login admin
- `/admin` - Menu admin

## 🛠️ Tech Stack

- Python 3.11
- python-telegram-bot
- SQLite
- ReportLab (PDF generation)

## 📖 Dokumentasi

- [RAILWAY_QUICK_START.md](RAILWAY_QUICK_START.md) - Deploy ke Railway
- [CHANGELOG_TOKO_KELONTONG.md](CHANGELOG_TOKO_KELONTONG.md) - Perubahan dari versi sebelumnya

## 📄 License

MIT License
