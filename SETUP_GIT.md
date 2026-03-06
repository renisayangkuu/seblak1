# 🔧 Setup Git Repository

## 📝 Langkah-Langkah

### 1️⃣ Initialize Git Repository

Buka terminal di folder project ini, lalu jalankan:

```bash
git init
```

### 2️⃣ Add Remote Repository

Tambahkan remote repository GitHub:

```bash
git remote add origin https://github.com/renisayangkuu/seblak1.git
```

### 3️⃣ Check Remote

Pastikan remote sudah terhubung:

```bash
git remote -v
```

Output yang diharapkan:
```
origin  https://github.com/renisayangkuu/seblak1.git (fetch)
origin  https://github.com/renisayangkuu/seblak1.git (push)
```

### 4️⃣ Add All Files

Tambahkan semua file ke staging:

```bash
git add .
```

### 5️⃣ Check Status

Lihat file apa saja yang akan di-commit:

```bash
git status
```

### 6️⃣ Commit

Commit dengan message:

```bash
git commit -m "Initial commit: Ready for Railway deployment"
```

### 7️⃣ Set Branch to Main

Pastikan branch adalah main (bukan master):

```bash
git branch -M main
```

### 8️⃣ Push to GitHub

Push ke GitHub:

```bash
git push -u origin main
```

Jika diminta username/password:
- Username: username GitHub Anda
- Password: Gunakan Personal Access Token (bukan password biasa)

## 🔑 Cara Membuat Personal Access Token

Jika diminta password saat push:

1. Buka GitHub → Settings → Developer settings
2. Klik "Personal access tokens" → "Tokens (classic)"
3. Klik "Generate new token" → "Generate new token (classic)"
4. Beri nama: "Railway Deploy"
5. Pilih scope: `repo` (full control)
6. Klik "Generate token"
7. Copy token (simpan di tempat aman!)
8. Gunakan token sebagai password saat push

## ✅ Verifikasi

Setelah push berhasil, buka:
```
https://github.com/renisayangkuu/seblak1
```

Pastikan semua file sudah ada di GitHub!

## 🚀 Next: Deploy ke Railway

Setelah file ada di GitHub, lanjut ke:
→ [RAILWAY_QUICK_START.md](RAILWAY_QUICK_START.md)

## 🆘 Troubleshooting

### "Repository not found"
- Pastikan repository sudah dibuat di GitHub
- Pastikan URL remote benar
- Coba: `git remote set-url origin https://github.com/renisayangkuu/seblak1.git`

### "Permission denied"
- Gunakan Personal Access Token sebagai password
- Atau setup SSH key (lihat GIT_COMMANDS.md)

### "Branch main doesn't exist"
- Jalankan: `git branch -M main`
- Lalu: `git push -u origin main`

## 📚 Resources

- [GIT_COMMANDS.md](GIT_COMMANDS.md) - Git commands reference
- [GitHub Docs](https://docs.github.com) - Official documentation
