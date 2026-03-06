# ✅ Checklist Deploy ke Railway

## Persiapan Lokal

- [ ] Pastikan bot berjalan dengan baik di lokal
- [ ] Test semua fitur (order, payment, admin)
- [ ] Pastikan folder `gambar/` berisi 3 gambar produk
- [ ] File `.env` sudah dikonfigurasi dengan benar (tapi JANGAN di-push ke GitHub)

## File yang Harus Ada di Repository

- [ ] `bot.py` - Main bot file
- [ ] `requirements.txt` - Python dependencies
- [ ] `runtime.txt` - Python version untuk Railway
- [ ] `Procfile` - Process type untuk Railway
- [ ] `railway.json` - Railway configuration
- [ ] `nixpacks.toml` - Build configuration
- [ ] `.railwayignore` - Files to ignore saat deploy
- [ ] `init_railway.py` - Auto-initialize database
- [ ] `seed_menu.py` - Menu seeding script
- [ ] `.env.example` - Template environment variables
- [ ] `.gitignore` - Files to ignore di Git
- [ ] `README.md` - Dokumentasi
- [ ] `DEPLOYMENT.md` - Panduan deploy
- [ ] `gambar/` folder dengan 3 gambar produk

## Push ke GitHub

```bash
# Check status
git status

# Add semua file (kecuali yang di .gitignore)
git add .

# Commit
git commit -m "Prepare for Railway deployment"

# Push ke repository
git push origin main
```

## Setup di Railway

### 1. Buat Project
- [ ] Login ke Railway.app
- [ ] Klik "New Project"
- [ ] Pilih "Deploy from GitHub repo"
- [ ] Pilih repository: `renisayangkuu/seblak1`

### 2. Environment Variables
Tambahkan di Railway dashboard (tab "Variables"):

```
TELEGRAM_BOT_TOKEN=<dapatkan dari @BotFather>
ADMIN_TELEGRAM_IDS=<ID Telegram Anda, dapatkan dari @userinfobot>
ADMIN_PASSWORD=<password admin Anda>
WARUNG_NAME=Seblak Sami
WARUNG_ADDRESS=Jl. Contoh No. 123, Jakarta
WARUNG_DESCRIPTION=Seblak pedas dengan berbagai pilihan ukuran.\nHarga terjangkau, rasa mantap!
BANK_NAME=BCA
BANK_ACCOUNT=1234567890
BANK_ACCOUNT_NAME=Seblak Sami
ONGKIR=10000
```

**PENTING:**
- [ ] `TELEGRAM_BOT_TOKEN` sudah diisi dengan token dari @BotFather
- [ ] `ADMIN_TELEGRAM_IDS` sudah diisi dengan ID Telegram Anda
- [ ] Semua value sudah disesuaikan dengan bisnis Anda

### 3. Deploy
- [ ] Railway akan otomatis build dan deploy
- [ ] Tunggu hingga status "Success" (2-3 menit)
- [ ] Cek logs untuk memastikan tidak ada error

### 4. Test Bot
- [ ] Buka Telegram dan cari bot Anda
- [ ] Kirim `/start` - bot harus merespon
- [ ] Test order flow lengkap
- [ ] Test login admin dengan `/loginadmin`
- [ ] Test konfirmasi pembayaran
- [ ] Test generate laporan

## Troubleshooting

### Bot tidak merespon
- [ ] Cek logs di Railway dashboard
- [ ] Pastikan `TELEGRAM_BOT_TOKEN` benar
- [ ] Pastikan tidak ada error di logs

### Gambar tidak muncul
- [ ] Pastikan folder `gambar/` ada di repository
- [ ] Pastikan ada 3 gambar di folder tersebut
- [ ] Cek logs untuk error terkait file path

### Database error
- [ ] Railway akan auto-create database
- [ ] Jika error, coba redeploy (klik "Redeploy" di Railway)

### Environment variables tidak terbaca
- [ ] Pastikan semua variables sudah diset di Railway dashboard
- [ ] Restart deployment setelah menambah variables

## Monitoring

- [ ] Bookmark Railway dashboard untuk monitoring
- [ ] Setup notifikasi di Railway (optional)
- [ ] Cek logs secara berkala

## Update Bot

Setiap kali ada perubahan:

```bash
git add .
git commit -m "Update: <deskripsi perubahan>"
git push origin main
```

Railway akan otomatis redeploy (jika auto-deploy enabled).

## Catatan Penting

⚠️ **Database SQLite di Railway bersifat ephemeral**
- Data akan hilang saat redeploy
- Untuk production, pertimbangkan Railway PostgreSQL atau external database

⚠️ **File uploads (bukti transfer)**
- File_id Telegram akan tetap tersimpan (sudah implemented)
- File fisik akan hilang saat redeploy
- Pertimbangkan cloud storage untuk production

✅ **Railway Free Tier**
- Cukup untuk bot kecil-menengah
- $5 credit gratis per bulan
- Bot akan sleep setelah tidak ada aktivitas (auto-wake saat ada request)

## Selesai!

Jika semua checklist sudah ✅, bot Anda siap berjalan 24/7 di Railway! 🎉
