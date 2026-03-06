"""Script to seed sample menu data - 1 product with 3 sizes"""
import sqlite3
import os

def seed_menu():
    """Add sample menu items - 3 sizes of one product with separate images"""
    conn = sqlite3.connect('umkm_bot.db')
    cur = conn.cursor()
    
    # Clear existing menu
    cur.execute("DELETE FROM menu")
    
    # Get image paths
    gambar_folder = 'gambar'
    images = sorted([f for f in os.listdir(gambar_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.avif', '.webp')) and not f.startswith('menu_collage')])
    
    # 1 product with 3 sizes - each with its own image
    sample_menu = [
        ('Seblak - Ukuran Kecil', 10000, 'Seblak kerupuk pedas porsi kecil (200gr)', 100, 
         os.path.join(gambar_folder, images[0]) if len(images) > 0 else None, 'tersedia'),
        ('Seblak - Ukuran Sedang', 15000, 'Seblak kerupuk pedas porsi sedang (350gr)', 100, 
         os.path.join(gambar_folder, images[1]) if len(images) > 1 else None, 'tersedia'),
        ('Seblak - Ukuran Besar', 20000, 'Seblak kerupuk pedas porsi besar (500gr)', 100, 
         os.path.join(gambar_folder, images[2]) if len(images) > 2 else None, 'tersedia'),
    ]
    
    for item in sample_menu:
        cur.execute("""
            INSERT INTO menu (nama, harga, deskripsi, stok, foto, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, item)
    
    conn.commit()
    conn.close()
    print("✅ Menu dengan 3 ukuran dan gambar terpisah berhasil ditambahkan!")
    print("   - Seblak Ukuran Kecil: Rp 10,000")
    print("   - Seblak Ukuran Sedang: Rp 15,000")
    print("   - Seblak Ukuran Besar: Rp 20,000")
    print(f"\n📸 Gambar diambil dari folder: {gambar_folder}")
    for i, img in enumerate(images[:3]):
        print(f"   {i+1}. {img}")

if __name__ == "__main__":
    seed_menu()
