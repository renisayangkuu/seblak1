"""
Script untuk inisialisasi database dan menu saat pertama kali deploy di Railway
"""
import sqlite3
import os

def init_railway_db():
    """Initialize database and seed menu for Railway deployment"""
    
    # Check if database already exists
    db_exists = os.path.exists('umkm_bot.db')
    
    conn = sqlite3.connect('umkm_bot.db')
    cur = conn.cursor()
    
    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama VARCHAR(100) NOT NULL,
            harga INTEGER NOT NULL,
            deskripsi TEXT,
            stok INTEGER DEFAULT 0,
            foto TEXT,
            status VARCHAR(20) DEFAULT 'tersedia'
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_customer VARCHAR(100) NOT NULL,
            telegram_id BIGINT NOT NULL,
            menu_id INTEGER NOT NULL,
            jumlah INTEGER NOT NULL,
            total INTEGER NOT NULL,
            metode_pengambilan VARCHAR(20),
            alamat_pengiriman TEXT,
            ongkir INTEGER DEFAULT 0,
            status_pesanan VARCHAR(20) DEFAULT 'menunggu',
            status_pembayaran VARCHAR(20) DEFAULT 'menunggu',
            bukti_transfer TEXT,
            tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (menu_id) REFERENCES menu(id)
        )
    """)
    
    # Check if menu is empty
    cur.execute("SELECT COUNT(*) FROM menu")
    menu_count = cur.fetchone()[0]
    
    if menu_count == 0:
        print("📝 Seeding menu data...")
        
        # Get image paths
        gambar_folder = 'gambar'
        images = []
        
        if os.path.exists(gambar_folder):
            images = sorted([f for f in os.listdir(gambar_folder) 
                           if f.endswith(('.png', '.jpg', '.jpeg', '.avif', '.webp')) 
                           and not f.startswith('menu_collage')])
        
        # Seed menu - Produk toko kelontong
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
        ]
        
        for item in sample_menu:
            cur.execute("""
                INSERT INTO menu (nama, harga, deskripsi, stok, foto, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, item)
        
        print("✅ Menu berhasil ditambahkan!")
        print(f"   Total: {len(sample_menu)} produk toko kelontong")
    else:
        print(f"✅ Database sudah ada dengan {menu_count} menu items")
    
    conn.commit()
    conn.close()
    print("✅ Database initialization complete!")

if __name__ == "__main__":
    init_railway_db()
