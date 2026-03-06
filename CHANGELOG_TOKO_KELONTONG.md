# 🔄 Perubahan: Seblak → Toko Kelontong

## ✅ Perubahan yang Sudah Dilakukan

### 1. Branding & Konfigurasi

**File: `.env.example`**
- ✅ `WARUNG_NAME`: "Seblak Sami" → "Toko Kelontong Berkah"
- ✅ `WARUNG_DESCRIPTION`: Deskripsi seblak → Deskripsi toko kelontong
- ✅ `BANK_ACCOUNT_NAME`: "Seblak Sami" → "Toko Kelontong Berkah"

### 2. Produk Menu

**File: `seed_menu.py`**
- ✅ Hapus: 3 ukuran seblak
- ✅ Tambah: 14 produk toko kelontong
  - 🍚 Sembako (3 item): Beras, Minyak Goreng, Gula
  - 🥫 Makanan & Minuman (3 item): Indomie, Teh Botol, Susu UHT
  - 🧼 Kebutuhan Rumah Tangga (3 item): Sabun Cuci Piring, Detergen, Tissue
  - 🍪 Snack & Jajanan (2 item): Chitato, Biskuit Marie
  - 🧴 Perlengkapan Mandi (3 item): Sabun Mandi, Shampoo, Pasta Gigi

**File: `init_railway.py`**
- ✅ Update auto-seed dengan produk toko kelontong (9 item utama)

### 3. Tampilan Bot

**File: `bot.py`**
- ✅ Welcome message: Emoji 🍜 → 🏪
- ✅ Button: "🍽️ Lihat Menu" → "🛒 Lihat Produk"
- ✅ Menu display: Dari gambar produk → List produk dengan kategori
- ✅ Kategorisasi otomatis berdasarkan nama produk
- ✅ Pesan error: "pesan menu" → "pesan produk"

## 📦 Produk yang Tersedia

### 🍚 Sembako
1. Beras Premium 5kg - Rp 65,000
2. Minyak Goreng 2L - Rp 32,000
3. Gula Pasir 1kg - Rp 15,000

### 🥫 Makanan & Minuman
4. Indomie Goreng (1 dus) - Rp 85,000
5. Teh Botol Sosro (1 dus) - Rp 48,000
6. Susu UHT 1L - Rp 18,000

### 🧼 Kebutuhan Rumah Tangga
7. Sabun Cuci Piring 800ml - Rp 12,000
8. Detergen 1kg - Rp 15,000
9. Tissue Gulung (12 roll) - Rp 35,000

### 🍪 Snack & Jajanan
10. Chitato (1 dus) - Rp 95,000
11. Biskuit Marie (1 dus) - Rp 42,000

### 🧴 Perlengkapan Mandi
12. Sabun Mandi Batang (6 pcs) - Rp 18,000
13. Shampoo Sachet (1 dus) - Rp 48,000
14. Pasta Gigi 150g - Rp 12,000

## 🚀 Deployment

Perubahan sudah di-push ke GitHub dan Railway akan otomatis redeploy.

**Status:** ✅ Pushed to GitHub

**Repository:** https://github.com/renisayangkuu/seblak1

## 📝 Yang Perlu Diupdate di Railway

### Environment Variables

Update di Railway dashboard → Variables:

```
WARUNG_NAME=Toko Kelontong Berkah
WARUNG_DESCRIPTION=🏪 TOKO KELONTONG BERKAH – Lengkap, Murah, Terpercaya! 🛒\n\nToko Kelontong Berkah menyediakan berbagai kebutuhan sehari-hari dengan harga terjangkau dan kualitas terjamin!\n\n📦 Produk yang tersedia:\n🍚 Sembako (beras, minyak, gula, dll)\n🥫 Makanan & Minuman\n🧼 Kebutuhan rumah tangga\n🍪 Snack & Jajanan\n🧴 Perlengkapan mandi\n\n✨ Keunggulan Toko Kami:\n✅ Harga bersaing & terjangkau\n✅ Produk lengkap & berkualitas\n✅ Tersedia layanan antar\n✅ Bisa pesan via Telegram\n✅ Pembayaran mudah & aman\n\nBelanja kebutuhan sehari-hari jadi lebih praktis! Pesan sekarang, barang langsung diantar ke rumah!
BANK_ACCOUNT_NAME=Toko Kelontong Berkah
```

**Note:** Variables lain (TELEGRAM_BOT_TOKEN, ADMIN_TELEGRAM_IDS, dll) tetap sama.

## 🔄 Reset Database (Optional)

Jika ingin reset database di Railway:

1. Stop service di Railway
2. Redeploy
3. Database akan otomatis dibuat ulang dengan produk toko kelontong

Atau bisa manual via Railway CLI:
```bash
railway run python seed_menu.py
```

## ✅ Testing Checklist

Setelah redeploy, test:

- [ ] Bot merespon `/start` dengan branding toko kelontong
- [ ] Button "🛒 Lihat Produk" berfungsi
- [ ] Menu menampilkan 14 produk dengan kategori
- [ ] Bisa pesan produk (pilih, input jumlah, dll)
- [ ] Proses checkout berfungsi normal
- [ ] Admin panel masih berfungsi

## 📸 Gambar Produk (Optional)

Folder `gambar/` masih berisi gambar seblak. Untuk update:

1. Ganti dengan gambar produk toko kelontong
2. Nama file diurutkan alfabetis
3. 3 gambar pertama akan digunakan untuk Beras, Minyak, Gula

Atau bisa hapus gambar dan produk akan tampil tanpa foto (text only).

## 🎉 Selesai!

Bot sudah berubah dari jualan seblak menjadi toko kelontong!

Railway akan otomatis redeploy dalam beberapa menit.
