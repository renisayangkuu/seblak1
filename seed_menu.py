"""Script to seed sample menu data - Toko Kelontong products"""
import sqlite3
import os

def seed_menu():
    """Add sample menu items - Produk toko kelontong"""
    conn = sqlite3.connect('umkm_bot.db')
    cur = conn.cursor()
    
    # Clear existing menu
    cur.execute("DELETE FROM menu")
    
    # Get image paths
    gambar_folder = 'gambar'
    images = []
    if os.path.exists(gambar_folder):
        images = sorted([f for f in os.listdir(gambar_folder) 
                        if f.endswith(('.png', '.jpg', '.jpeg', '.avif', '.webp')) 
                        and not f.startswith('menu_collage')])
    
    # Produk toko kelontong
    sample_menu = [
        # Sembako
        ('Beras Premium 5kg', 65000, 'Beras putih premium kualitas terbaik', 50, 
         os.path.join(gambar_folder, images[0]) if len(images) > 0 else None, 'tersedia'),
        ('Minyak Goreng 2L', 32000, 'Minyak goreng kemasan 2 liter', 30, 
         os.path.join(gambar_folder, images[1]) if len(images) > 1 else None, 'tersedia'),
        ('Gula Pasir 1kg', 15000, 'Gula pasir putih 1 kilogram', 40, 
         os.path.join(gambar_folder, images[2]) if len(images) > 2 else None, 'tersedia'),
        
        # Makanan & Minuman
        ('Indomie Goreng (1 dus)', 85000, 'Indomie goreng isi 40 bungkus', 20, 
         None, 'tersedia'),
        ('Teh Botol Sosro (1 dus)', 48000, 'Teh botol sosro isi 24 botol', 15, 
         None, 'tersedia'),
        ('Susu UHT 1L', 18000, 'Susu UHT plain 1 liter', 25, 
         None, 'tersedia'),
        
        # Kebutuhan Rumah Tangga
        ('Sabun Cuci Piring 800ml', 12000, 'Sabun cuci piring ekonomis', 30, 
         None, 'tersedia'),
        ('Detergen 1kg', 15000, 'Detergen bubuk 1 kilogram', 25, 
         None, 'tersedia'),
        ('Tissue Gulung (12 roll)', 35000, 'Tissue gulung isi 12 roll', 20, 
         None, 'tersedia'),
        
        # Snack & Jajanan
        ('Chitato (1 dus)', 95000, 'Chitato berbagai rasa isi 20 pcs', 10, 
         None, 'tersedia'),
        ('Biskuit Marie (1 dus)', 42000, 'Biskuit marie isi 24 bungkus', 15, 
         None, 'tersedia'),
        
        # Perlengkapan Mandi
        ('Sabun Mandi Batang (6 pcs)', 18000, 'Sabun mandi batang isi 6', 20, 
         None, 'tersedia'),
        ('Shampoo Sachet (1 dus)', 48000, 'Shampoo sachet isi 48 pcs', 15, 
         None, 'tersedia'),
        ('Pasta Gigi 150g', 12000, 'Pasta gigi keluarga 150 gram', 25, 
         None, 'tersedia'),
    ]
    
    for item in sample_menu:
        cur.execute("""
            INSERT INTO menu (nama, harga, deskripsi, stok, foto, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, item)
    
    conn.commit()
    conn.close()
    print("✅ Menu toko kelontong berhasil ditambahkan!")
    print(f"\n📦 Total produk: {len(sample_menu)}")
    print("\n📋 Kategori produk:")
    print("   - Sembako (3 item)")
    print("   - Makanan & Minuman (3 item)")
    print("   - Kebutuhan Rumah Tangga (3 item)")
    print("   - Snack & Jajanan (2 item)")
    print("   - Perlengkapan Mandi (3 item)")
    
    if images:
        print(f"\n📸 Gambar diambil dari folder: {gambar_folder}")
        for i, img in enumerate(images[:3]):
            print(f"   {i+1}. {img}")

if __name__ == "__main__":
    seed_menu()
