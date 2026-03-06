# 🎯 START HERE - Panduan Lengkap Deploy Bot ke Railway

## 📋 Ringkasan

Bot Telegram UMKM Seblak Anda sudah siap untuk di-deploy ke Railway! 
Semua file konfigurasi sudah disiapkan. Tinggal ikuti langkah-langkah di bawah.

## ⏱️ Estimasi Waktu

- Setup Git: 5 menit
- Push ke GitHub: 2 menit
- Deploy ke Railway: 5 menit
- **Total: ~15 menit**

## 🚀 Langkah-Langkah

### Step 1: Setup Git Repository (5 menit)

Jika repository belum di-initialize:

```bash
# Initialize Git
git init

# Add remote
git remote add origin https://github.com/renisayangkuu/seblak1.git

# Add all files
git add .

# Commit
git commit -m "Initial commit: Ready for Railway deployment"

# Set branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

📖 **Panduan lengkap:** [SETUP_GIT.md](SETUP_GIT.md)

### Step 2: Verifikasi (1 menit)

Buka GitHub dan pastikan semua file sudah ada:
```
https://github.com/renisayangkuu/seblak1
```

File penting yang harus ada:
- ✅ bot.py
- ✅ requirements.txt
- ✅ railway.json
- ✅ Procfile
- ✅ gambar/ folder dengan 3 gambar

### Step 3: Deploy ke Railway (5 menit)

1. **Buka Railway**
   - https://railway.app
   - Login dengan GitHub

2. **Create Project**
   - Klik "New Project"
   - Pilih "Deploy from GitHub repo"
   - Pilih: `renisayangkuu/seblak1`

3. **Set Environment Variables**
   
   Klik tab "Variables" dan tambahkan:
   
   **WAJIB:**
   ```
   TELEGRAM_BOT_TOKEN=<token dari @BotFather>
   ADMIN_TELEGRAM_IDS=<ID dari @userinfobot>
   ```
   
   **Optional (bisa pakai default):**
   ```
   ADMIN_PASSWORD=admin123
   WARUNG_NAME=Seblak Sami
   BANK_NAME=BCA
   BANK_ACCOUNT=1234567890
   BANK_ACCOUNT_NAME=Seblak Sami
   ONGKIR=10000
   ```

4. **Deploy**
   - Railway akan otomatis deploy
   - Tunggu hingga status "Success" (2-3 menit)

5. **Test Bot**
   - Buka Telegram
   - Cari bot Anda
   - Kirim `/start`
   - Bot harus merespon dengan menu!

📖 **Panduan lengkap:** [RAILWAY_QUICK_START.md](RAILWAY_QUICK_START.md)

## ✅ Checklist

### Persiapan
- [ ] Bot sudah ditest di lokal
- [ ] Folder `gambar/` berisi 3 gambar
- [ ] File `.env.example` sudah ada

### Git & GitHub
- [ ] Git repository sudah di-initialize
- [ ] Remote GitHub sudah ditambahkan
- [ ] Semua file sudah di-push ke GitHub
- [ ] File terlihat di https://github.com/renisayangkuu/seblak1

### Railway
- [ ] Project Railway sudah dibuat
- [ ] Repository GitHub sudah di-connect
- [ ] Environment variables sudah diset
- [ ] Deploy status "Success"

### Testing
- [ ] Bot merespon `/start`
- [ ] Menu muncul dengan gambar
- [ ] Bisa order menu
- [ ] Admin bisa login
- [ ] Konfirmasi pembayaran berfungsi

## 📚 Dokumentasi Lengkap

### Quick Start (Recommended)
- **[RAILWAY_QUICK_START.md](RAILWAY_QUICK_START.md)** - Deploy dalam 5 menit

### Setup & Configuration
- **[SETUP_GIT.md](SETUP_GIT.md)** - Setup Git repository
- **[GIT_COMMANDS.md](GIT_COMMANDS.md)** - Git commands reference

### Deployment
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Panduan deploy lengkap
- **[CHECKLIST_DEPLOY.md](CHECKLIST_DEPLOY.md)** - Checklist detail

### Reference
- **[FILES_CREATED.md](FILES_CREATED.md)** - Daftar file yang dibuat
- **[README.md](README.md)** - Dokumentasi bot

## 🔧 Tools & Scripts

### Validasi Kesiapan Deploy
```bash
python validate_deploy.py
```

Output yang diharapkan:
```
✅ VALIDATION PASSED!
🎉 All files ready for Railway deployment!
```

## 🆘 Troubleshooting

### Git Issues
- Repository not found → Check remote URL
- Permission denied → Use Personal Access Token
- Branch doesn't exist → Run `git branch -M main`

📖 Lihat: [SETUP_GIT.md](SETUP_GIT.md)

### Railway Issues
- Bot tidak merespon → Check logs & TELEGRAM_BOT_TOKEN
- Gambar tidak muncul → Check folder gambar/ di repository
- Database error → Redeploy

📖 Lihat: [RAILWAY_QUICK_START.md](RAILWAY_QUICK_START.md)

### Bot Issues
- Menu tidak muncul → Check database initialization
- Payment tidak berfungsi → Check BANK_* variables
- Admin tidak bisa login → Check ADMIN_PASSWORD

📖 Lihat: [DEPLOYMENT.md](DEPLOYMENT.md)

## 💡 Tips

1. **Validasi sebelum push:**
   ```bash
   python validate_deploy.py
   ```

2. **Check status Git:**
   ```bash
   git status
   ```

3. **Monitor Railway logs:**
   - Railway dashboard → Deployments → View Logs

4. **Update bot:**
   ```bash
   git add .
   git commit -m "Update: <deskripsi>"
   git push origin main
   ```
   Railway akan auto-redeploy!

## 🎉 Selesai!

Setelah semua langkah selesai, bot Anda akan berjalan 24/7 di Railway!

**Next Steps:**
- Monitor logs di Railway dashboard
- Test semua fitur bot
- Promosikan bot ke customer
- Generate laporan harian

## 📞 Need Help?

- Railway Docs: https://docs.railway.app
- Telegram Bot API: https://core.telegram.org/bots/api
- GitHub Docs: https://docs.github.com

---

**Repository:** https://github.com/renisayangkuu/seblak1

**Dibuat dengan ❤️ untuk UMKM Seblak Sami**
