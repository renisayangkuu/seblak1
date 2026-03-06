# 📝 Git Commands untuk Deploy

## 🔍 Check Status

Lihat file apa saja yang berubah:
```bash
git status
```

## ➕ Add Files

Add semua file yang berubah:
```bash
git add .
```

Add file tertentu:
```bash
git add bot.py
git add requirements.txt
```

## 💾 Commit

Commit dengan message:
```bash
git commit -m "Ready for Railway deployment"
```

Commit dengan message lebih detail:
```bash
git commit -m "Add Railway deployment files

- Add railway.json, Procfile, nixpacks.toml
- Add init_railway.py for auto-initialization
- Update README with deployment guide"
```

## 🚀 Push ke GitHub

Push ke branch main:
```bash
git push origin main
```

Jika error "branch tidak ada", buat branch main dulu:
```bash
git branch -M main
git push -u origin main
```

## 🔄 Update Setelah Deploy

Setiap kali ada perubahan:
```bash
# 1. Check apa yang berubah
git status

# 2. Add semua perubahan
git add .

# 3. Commit dengan message
git commit -m "Update: <deskripsi perubahan>"

# 4. Push ke GitHub
git push origin main
```

Railway akan otomatis redeploy!

## 🌿 Branch Management

Lihat branch yang ada:
```bash
git branch
```

Buat branch baru:
```bash
git checkout -b development
```

Pindah ke branch lain:
```bash
git checkout main
```

## 📜 History

Lihat commit history:
```bash
git log
```

Lihat commit history singkat:
```bash
git log --oneline
```

## ↩️ Undo Changes

Undo perubahan file yang belum di-commit:
```bash
git checkout -- bot.py
```

Undo semua perubahan:
```bash
git checkout -- .
```

Undo commit terakhir (tapi keep changes):
```bash
git reset --soft HEAD~1
```

## 🔗 Remote Repository

Lihat remote repository:
```bash
git remote -v
```

Tambah remote (jika belum ada):
```bash
git remote add origin https://github.com/renisayangkuu/seblak1.git
```

Ganti remote URL:
```bash
git remote set-url origin https://github.com/renisayangkuu/seblak1.git
```

## 🆕 First Time Setup

Jika ini pertama kali setup Git di komputer:

```bash
# Set username
git config --global user.name "Your Name"

# Set email
git config --global user.email "your.email@example.com"

# Check config
git config --list
```

## 📦 Clone Repository

Clone repository ke komputer lain:
```bash
git clone https://github.com/renisayangkuu/seblak1.git
cd seblak1
```

## 🔄 Pull Latest Changes

Ambil perubahan terbaru dari GitHub:
```bash
git pull origin main
```

## 🚫 .gitignore

File yang di-ignore (tidak akan di-push):
- `.env` - Environment variables (rahasia!)
- `*.db` - Database lokal
- `*.pdf` - Laporan yang di-generate
- `__pycache__/` - Python cache
- `venv/` - Virtual environment

Lihat file yang di-ignore:
```bash
git status --ignored
```

## 💡 Tips

1. **Selalu check status sebelum commit:**
   ```bash
   git status
   ```

2. **Commit message yang baik:**
   - Singkat dan jelas
   - Gunakan present tense: "Add feature" bukan "Added feature"
   - Contoh: "Fix payment confirmation bug"

3. **Jangan push file sensitif:**
   - `.env` file (sudah di .gitignore)
   - Database dengan data real
   - API keys atau passwords

4. **Commit sering:**
   - Lebih baik commit kecil-kecil
   - Lebih mudah track perubahan
   - Lebih mudah undo jika ada masalah

## 🆘 Common Issues

### "Permission denied"
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add SSH key ke GitHub
# Copy public key
cat ~/.ssh/id_ed25519.pub

# Paste ke GitHub Settings → SSH Keys
```

### "Repository not found"
```bash
# Check remote URL
git remote -v

# Update remote URL
git remote set-url origin https://github.com/renisayangkuu/seblak1.git
```

### "Merge conflict"
```bash
# Pull latest changes
git pull origin main

# Resolve conflicts manually in files
# Then commit
git add .
git commit -m "Resolve merge conflicts"
git push origin main
```

## 📚 Resources

- Git Documentation: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com
- Git Cheat Sheet: https://education.github.com/git-cheat-sheet-education.pdf
