"""
Bot UMKM Warung Jajanan - All in One
Telegram bot untuk UMKM makanan dengan fitur pemesanan dan pembayaran
"""

import logging
import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# ============================================================================
# CONFIGURATION
# ============================================================================

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_TELEGRAM_IDS = [int(id.strip()) for id in os.getenv('ADMIN_TELEGRAM_IDS', '').split(',') if id.strip()]
WARUNG_NAME = os.getenv('WARUNG_NAME', 'Warung Jajanan Kita')
WARUNG_ADDRESS = os.getenv('WARUNG_ADDRESS', 'Jl. Contoh No. 123, Jakarta')
WARUNG_DESCRIPTION = os.getenv('WARUNG_DESCRIPTION', 'Warung makanan dengan berbagai pilihan menu.')
BANK_NAME = os.getenv('BANK_NAME', 'BCA')
BANK_ACCOUNT = os.getenv('BANK_ACCOUNT', '1234567890')
BANK_ACCOUNT_NAME = os.getenv('BANK_ACCOUNT_NAME', 'Warung Jajanan Kita')
ONGKIR = int(os.getenv('ONGKIR', '10000'))

DATABASE_FILE = 'umkm_bot.db'

# Conversation states
ASKING_QUANTITY, ASKING_ADDRESS, ASKING_PAYMENT_PROOF, ADMIN_LOGIN_PASSWORD = range(4)

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """Initialize database with tables"""
    with get_db_connection() as conn:
        cur = conn.cursor()
        
        # Table menu
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
        
        # Table orders
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
        
        conn.commit()
        logger.info("Database initialized successfully")

def get_all_menu():
    """Get all menu items"""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM menu WHERE status = 'tersedia' ORDER BY id")
        return [dict(row) for row in cur.fetchall()]

def get_menu_by_id(menu_id):
    """Get menu item by ID"""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM menu WHERE id = ?", (menu_id,))
        row = cur.fetchone()
        return dict(row) if row else None

def create_order(nama_customer, telegram_id, menu_id, jumlah, total, metode_pengambilan, alamat_pengiriman, ongkir):
    """Create new order"""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO orders (nama_customer, telegram_id, menu_id, jumlah, total, 
                              metode_pengambilan, alamat_pengiriman, ongkir, status_pesanan, status_pembayaran)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'menunggu', 'menunggu')
        """, (nama_customer, telegram_id, menu_id, jumlah, total, metode_pengambilan, alamat_pengiriman, ongkir))
        conn.commit()
        return cur.lastrowid

def get_order_by_id(order_id):
    """Get order by ID"""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT o.*, m.nama as menu_nama, m.harga as menu_harga
            FROM orders o
            JOIN menu m ON o.menu_id = m.id
            WHERE o.id = ?
        """, (order_id,))
        row = cur.fetchone()
        return dict(row) if row else None

def update_order_payment_proof(order_id, file_id):
    """Update order with payment proof"""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE orders 
            SET bukti_transfer = ?, status_pembayaran = 'menunggu_konfirmasi'
            WHERE id = ?
        """, (file_id, order_id))
        conn.commit()

def get_pending_orders():
    """Get orders waiting for payment confirmation"""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT o.*, m.nama as menu_nama
            FROM orders o
            JOIN menu m ON o.menu_id = m.id
            WHERE o.status_pembayaran = 'menunggu_konfirmasi'
            ORDER BY o.tanggal DESC
        """)
        return [dict(row) for row in cur.fetchall()]

def confirm_payment(order_id, approved):
    """Confirm or reject payment"""
    status = 'lunas' if approved else 'ditolak'
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE orders 
            SET status_pembayaran = ?, status_pesanan = ?
            WHERE id = ?
        """, (status, 'diproses' if approved else 'ditolak', order_id))
        conn.commit()

def update_order_status(order_id, status):
    """Update order status"""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE orders 
            SET status_pesanan = ?
            WHERE id = ?
        """, (status, order_id))
        conn.commit()

def get_user_orders(telegram_id, limit=10):
    """Get user's recent orders"""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT o.*, m.nama as menu_nama
            FROM orders o
            JOIN menu m ON o.menu_id = m.id
            WHERE o.telegram_id = ?
            ORDER BY o.tanggal DESC
            LIMIT ?
        """, (telegram_id, limit))
        return [dict(row) for row in cur.fetchall()]

def get_daily_orders(date_str):
    """Get orders for specific date"""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT o.*, m.nama as menu_nama, m.harga as menu_harga
            FROM orders o
            JOIN menu m ON o.menu_id = m.id
            WHERE DATE(o.tanggal) = ?
            ORDER BY o.tanggal DESC
        """, (date_str,))
        return [dict(row) for row in cur.fetchall()]

# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_daily_report(date_str):
    """Generate PDF report for specific date"""
    orders = get_daily_orders(date_str)
    
    if not orders:
        return None
    
    filename = f"laporan_{date_str.replace('-', '')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1  # Center
    )
    title = Paragraph(f"LAPORAN HARIAN<br/>{date_str}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.5*cm))
    
    # Summary
    total_orders = len(orders)
    total_revenue = sum(o['total'] for o in orders if o['status_pembayaran'] == 'lunas')
    
    summary_data = [
        ['Total Pesanan', str(total_orders)],
        ['Total Omzet', f"Rp {total_revenue:,}"]
    ]
    summary_table = Table(summary_data, colWidths=[8*cm, 8*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 1*cm))
    
    # Orders detail
    detail_title = Paragraph("DETAIL PESANAN", styles['Heading2'])
    elements.append(detail_title)
    elements.append(Spacer(1, 0.3*cm))
    
    # Table header
    data = [['ID', 'Customer', 'Menu', 'Qty', 'Total', 'Metode', 'Status Bayar', 'Status Pesanan']]
    
    # Table rows
    for order in orders:
        data.append([
            str(order['id']),
            order['nama_customer'][:15],
            order['menu_nama'][:20],
            str(order['jumlah']),
            f"Rp {order['total']:,}",
            order['metode_pengambilan'][:8],
            order['status_pembayaran'][:10],
            order['status_pesanan'][:10]
        ])
    
    # Create table
    table = Table(data, colWidths=[1*cm, 3*cm, 3.5*cm, 1*cm, 2.5*cm, 2*cm, 2.5*cm, 2*cm])
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Body
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    return filename

# ============================================================================
# BOT HANDLERS - CUSTOMER
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.message.from_user
    keyboard = [
        [InlineKeyboardButton("🛒 Lihat Produk", callback_data='show_menu')],
        [InlineKeyboardButton("📦 Pesanan Saya", callback_data='my_orders')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Replace \n with actual line breaks
    description = WARUNG_DESCRIPTION.replace('\\n', '\n')
    
    welcome_text = (
        f"👋 Halo {user.first_name}! Selamat datang di {WARUNG_NAME} 🏪\n\n"
        f"📍 Alamat: {WARUNG_ADDRESS}\n\n"
        f"ℹ️ Tentang Kami:\n{description}\n\n"
        "Silakan pilih menu di bawah untuk mulai berbelanja:"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show menu - display product list for toko kelontong"""
    query = update.callback_query
    await query.answer()

    # Get all menu items
    menu_items = get_all_menu()

    if not menu_items:
        await query.edit_message_text("Maaf, menu belum tersedia.")
        return

    # Group products by category (simple grouping based on price range and name)
    categories = {
        '🍚 Sembako': [],
        '🥫 Makanan & Minuman': [],
        '🧼 Kebutuhan Rumah Tangga': [],
        '🍪 Snack & Jajanan': [],
        '🧴 Perlengkapan Mandi': []
    }
    
    # Simple categorization based on product names
    for item in menu_items:
        nama = item['nama'].lower()
        if any(x in nama for x in ['beras', 'minyak', 'gula', 'tepung']):
            categories['🍚 Sembako'].append(item)
        elif any(x in nama for x in ['indomie', 'mie', 'teh', 'susu', 'kopi', 'minuman']):
            categories['🥫 Makanan & Minuman'].append(item)
        elif any(x in nama for x in ['sabun cuci', 'detergen', 'tissue', 'pel', 'sapu']):
            categories['🧼 Kebutuhan Rumah Tangga'].append(item)
        elif any(x in nama for x in ['chitato', 'biskuit', 'snack', 'keripik', 'wafer']):
            categories['🍪 Snack & Jajanan'].append(item)
        elif any(x in nama for x in ['sabun mandi', 'shampoo', 'pasta gigi', 'sikat']):
            categories['🧴 Perlengkapan Mandi'].append(item)
        else:
            categories['🥫 Makanan & Minuman'].append(item)  # default category
    
    # Build menu text
    menu_text = f"🏪 DAFTAR PRODUK {WARUNG_NAME.upper()}\n\n"
    menu_text += "Pilih produk yang ingin dipesan:\n\n"
    
    # Create buttons grouped by category
    buttons = []
    
    for category, items in categories.items():
        if items:  # Only show category if it has items
            menu_text += f"{category}\n"
            for item in items:
                menu_text += f"  • {item['nama']} - Rp {item['harga']:,}\n"
                buttons.append([InlineKeyboardButton(
                    f"🛒 {item['nama']} - Rp {item['harga']:,}",
                    callback_data=f"pesan_{item['id']}"
                )])
            menu_text += "\n"
    
    # Add back button
    buttons.append([InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main')])
    reply_markup = InlineKeyboardMarkup(buttons)

    # Send menu text with buttons
    await query.edit_message_text(
        text=menu_text,
        reply_markup=reply_markup
    )

async def pesanan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pesanan command"""
    user_id = update.message.from_user.id
    orders = get_user_orders(user_id)
    
    if not orders:
        keyboard = [[InlineKeyboardButton("🍽️ Lihat Menu", callback_data='show_menu')]]
        await update.message.reply_text(
            "📦 Belum ada pesanan.\n\nSilakan pesan produk terlebih dahulu!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    # Status icons
    status_icons = {
        'menunggu': '⏸️',
        'menunggu_konfirmasi': '⏳',
        'lunas': '✅',
        'ditolak': '❌',
        'diproses': '🔄',
        'selesai': '✅'
    }
    
    text = "📦 PESANAN SAYA\n\n"
    for order in orders:
        payment_icon = status_icons.get(order['status_pembayaran'], '❓')
        order_icon = status_icons.get(order['status_pesanan'], '❓')
        
        text += (
            f"🆔 #{order['id']}\n"
            f"🍴 {order['menu_nama']} x{order['jumlah']}\n"
            f"💰 Rp {order['total']:,}\n"
            f"📍 {order['metode_pengambilan']}\n"
            f"{payment_icon} Pembayaran: {order['status_pembayaran']}\n"
            f"{order_icon} Pesanan: {order['status_pesanan']}\n"
            f"━━━━━━━━━━━━━━━━\n\n"
        )
    
    keyboard = [[InlineKeyboardButton("🔙 Menu Utama", callback_data='back_to_main')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's orders"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    orders = get_user_orders(user_id)
    
    if not orders:
        await query.edit_message_text(
            "📦 Belum ada pesanan.\n\nSilakan pesan produk terlebih dahulu!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main')
            ]])
        )
        return
    
    # Status icons
    status_icons = {
        'menunggu': '⏸️',
        'menunggu_konfirmasi': '⏳',
        'lunas': '✅',
        'ditolak': '❌',
        'diproses': '🔄',
        'selesai': '✅'
    }
    
    text = "📦 PESANAN SAYA\n\n"
    for order in orders:
        payment_icon = status_icons.get(order['status_pembayaran'], '❓')
        order_icon = status_icons.get(order['status_pesanan'], '❓')
        
        text += (
            f"🆔 #{order['id']}\n"
            f"🍴 {order['menu_nama']} x{order['jumlah']}\n"
            f"💰 Rp {order['total']:,}\n"
            f"📍 {order['metode_pengambilan']}\n"
            f"{payment_icon} Pembayaran: {order['status_pembayaran']}\n"
            f"{order_icon} Pesanan: {order['status_pesanan']}\n"
            f"━━━━━━━━━━━━━━━━\n\n"
        )
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main')
        ]])
    )
async def pesanan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pesanan command"""
    user_id = update.message.from_user.id
    orders = get_user_orders(user_id)

    if not orders:
        keyboard = [[InlineKeyboardButton("🍽️ Lihat Menu", callback_data='show_menu')]]
        await update.message.reply_text(
            "📦 Belum ada pesanan.\n\nSilakan pesan produk terlebih dahulu!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Status icons
    status_icons = {
        'menunggu': '⏸️',
        'menunggu_konfirmasi': '⏳',
        'lunas': '✅',
        'ditolak': '❌',
        'diproses': '🔄',
        'selesai': '✅'
    }

    text = "📦 PESANAN SAYA\n\n"
    for order in orders:
        payment_icon = status_icons.get(order['status_pembayaran'], '❓')
        order_icon = status_icons.get(order['status_pesanan'], '❓')

        text += (
            f"🆔 #{order['id']}\n"
            f"🍴 {order['menu_nama']} x{order['jumlah']}\n"
            f"💰 Rp {order['total']:,}\n"
            f"📍 {order['metode_pengambilan']}\n"
            f"{payment_icon} Pembayaran: {order['status_pembayaran']}\n"
            f"{order_icon} Pesanan: {order['status_pesanan']}\n"
            f"━━━━━━━━━━━━━━━━\n\n"
        )

    keyboard = [[InlineKeyboardButton("🔙 Menu Utama", callback_data='back_to_main')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Back to main menu"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🛒 Lihat Produk", callback_data='show_menu')],
        [InlineKeyboardButton("📦 Pesanan Saya", callback_data='my_orders')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🏠 Menu Utama\n\nSilakan pilih:",
        reply_markup=reply_markup
    )

# ============================================================================
# BOT HANDLERS - ORDERING FLOW
# ============================================================================

async def order_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle menu order button"""
    query = update.callback_query
    await query.answer()
    
    # Extract menu_id from callback_data (format: pesan_<menu_id>)
    menu_id = int(query.data.split('_')[1])
    menu_item = get_menu_by_id(menu_id)
    
    if not menu_item:
        await query.edit_message_text("Maaf, menu tidak ditemukan.")
        return
    
    # Store menu_id in context
    context.user_data['menu_id'] = menu_id
    context.user_data['menu_item'] = menu_item
    
    await query.edit_message_text(
        f"🍴 {menu_item['nama']}\n"
        f"💰 Rp {menu_item['harga']:,}\n\n"
        f"Berapa porsi yang ingin dipesan?\n"
        f"(Ketik angka, contoh: 2)"
    )
    
    return ASKING_QUANTITY

async def receive_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive quantity input"""
    try:
        quantity = int(update.message.text)
        if quantity <= 0:
            await update.message.reply_text("Jumlah harus lebih dari 0. Silakan coba lagi:")
            return ASKING_QUANTITY
        
        menu_item = context.user_data['menu_item']
        subtotal = menu_item['harga'] * quantity
        
        # Store quantity
        context.user_data['quantity'] = quantity
        context.user_data['subtotal'] = subtotal
        
        # Ask for delivery method
        keyboard = [
            [InlineKeyboardButton("🏪 Ambil Sendiri (Pickup)", callback_data='pickup')],
            [InlineKeyboardButton(f"🚚 Dikirim (+Rp {ONGKIR:,})", callback_data='delivery')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🍴 {menu_item['nama']} x{quantity}\n"
            f"💰 Subtotal: Rp {subtotal:,}\n\n"
            f"Bagaimana pesanan Anda ingin diterima?",
            reply_markup=reply_markup
        )
        
        # End conversation, delivery method will be handled by separate callback
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text("Mohon masukkan angka yang valid:")
        return ASKING_QUANTITY

async def choose_delivery_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle delivery method selection"""
    query = update.callback_query
    await query.answer()
    
    method = query.data  # 'pickup' or 'delivery'
    context.user_data['metode_pengambilan'] = method
    
    # If delivery, ask for address first
    if method == 'delivery':
        await query.edit_message_text(
            "📍 Silakan kirim alamat lengkap pengiriman Anda:\n\n"
            "Contoh:\n"
            "Jl. Merdeka No. 123, RT 01/RW 02\n"
            "Kelurahan Menteng, Kecamatan Menteng\n"
            "Jakarta Pusat 10310\n"
            "Patokan: Dekat Indomaret"
        )
        return ASKING_ADDRESS
    else:
        # If pickup, proceed directly to create order
        await finalize_order_pickup(query, context)
        return ConversationHandler.END

async def finalize_order_pickup(query, context):
    """Finalize order for pickup (no address needed)"""
    menu_item = context.user_data['menu_item']
    quantity = context.user_data['quantity']
    subtotal = context.user_data['subtotal']
    
    method = 'pickup'
    ongkir = 0
    total = subtotal
    
    user = query.from_user
    chat_id = query.message.chat_id
    
    order_id = create_order(
        nama_customer=user.first_name,
        telegram_id=user.id,
        menu_id=menu_item['id'],
        jumlah=quantity,
        total=total,
        metode_pengambilan=method,
        alamat_pengiriman=None,
        ongkir=ongkir
    )
    
    # Store order_id
    context.user_data['order_id'] = order_id
    
    # Payment instruction
    payment_text = (
        f"🧾 DETAIL PESANAN #{order_id}\n\n"
        f"🍴 Menu: {menu_item['nama']} x{quantity}\n"
        f"💰 Subtotal: Rp {subtotal:,}\n"
        f"📍 Metode: Ambil Sendiri\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"💵 TOTAL: Rp {total:,}\n\n"
        f"💳 Silakan transfer ke:\n"
        f"{BANK_NAME} {BANK_ACCOUNT}\n"
        f"a.n {BANK_ACCOUNT_NAME}\n\n"
        f"Setelah transfer, klik tombol di bawah:"
    )
    
    keyboard = [[InlineKeyboardButton("📸 Saya Sudah Bayar", callback_data=f'paid_{order_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=payment_text,
        reply_markup=reply_markup
    )

async def receive_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive delivery address"""
    alamat = update.message.text
    context.user_data['alamat_pengiriman'] = alamat
    
    method = context.user_data['metode_pengambilan']
    return await finalize_order(update, context, method, alamat)

async def finalize_order(update, context, method, alamat_pengiriman):
    """Finalize order and show payment instruction"""
    menu_item = context.user_data['menu_item']
    quantity = context.user_data['quantity']
    subtotal = context.user_data['subtotal']
    
    ongkir = ONGKIR if method == 'delivery' else 0
    total = subtotal + ongkir
    
    # Get user and chat_id from update (could be message or callback_query)
    if hasattr(update, 'callback_query') and update.callback_query:
        user = update.callback_query.from_user
        chat_id = update.callback_query.message.chat_id
    elif hasattr(update, 'message') and update.message:
        user = update.message.from_user
        chat_id = update.message.chat_id
    else:
        # Fallback
        user = update.effective_user
        chat_id = update.effective_chat.id
    
    order_id = create_order(
        nama_customer=user.first_name,
        telegram_id=user.id,
        menu_id=menu_item['id'],
        jumlah=quantity,
        total=total,
        metode_pengambilan=method,
        alamat_pengiriman=alamat_pengiriman,
        ongkir=ongkir
    )
    
    # Store order_id
    context.user_data['order_id'] = order_id
    
    # Payment instruction
    payment_text = (
        f"🧾 DETAIL PESANAN #{order_id}\n\n"
        f"🍴 Menu: {menu_item['nama']} x{quantity}\n"
        f"💰 Subtotal: Rp {subtotal:,}\n"
        f"📍 Metode: {'Dikirim' if method == 'delivery' else 'Ambil Sendiri'}\n"
    )
    
    if method == 'delivery':
        payment_text += f"📮 Alamat: {alamat_pengiriman}\n"
        payment_text += f"� Ongkir: Rp {ongkir:,}\n"
    
    payment_text += (
        f"━━━━━━━━━━━━━━━━\n"
        f"�💵 TOTAL: Rp {total:,}\n\n"
        f"💳 Silakan transfer ke:\n"
        f"{BANK_NAME} {BANK_ACCOUNT}\n"
        f"a.n {BANK_ACCOUNT_NAME}\n\n"
        f"Setelah transfer, klik tombol di bawah:"
    )
    
    keyboard = [[InlineKeyboardButton("📸 Saya Sudah Bayar", callback_data=f'paid_{order_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=payment_text,
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END

async def payment_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for payment proof"""
    query = update.callback_query
    await query.answer()
    
    # Extract order_id from callback_data
    order_id = int(query.data.split('_')[1])
    context.user_data['order_id'] = order_id
    
    await query.edit_message_text(
        "📸 Silakan upload foto bukti transfer Anda:"
    )
    
    return ASKING_PAYMENT_PROOF

async def receive_payment_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive payment proof photo"""
    if not update.message.photo:
        await update.message.reply_text("Mohon kirim foto bukti transfer:")
        return ASKING_PAYMENT_PROOF
    
    # Get largest photo
    photo = update.message.photo[-1]
    order_id = context.user_data.get('order_id')
    
    if not order_id:
        await update.message.reply_text("Terjadi kesalahan. Silakan mulai dari awal dengan /start")
        return ConversationHandler.END
    
    # Update order with payment proof
    update_order_payment_proof(order_id, photo.file_id)
    
    # Notify admins
    order = get_order_by_id(order_id)
    for admin_id in ADMIN_TELEGRAM_IDS:
        try:
            keyboard = [
                [InlineKeyboardButton("📸 Lihat Bukti", callback_data=f'view_proof_{order_id}')],
                [
                    InlineKeyboardButton("✅ Konfirmasi", callback_data=f'approve_{order_id}'),
                    InlineKeyboardButton("❌ Tolak", callback_data=f'reject_{order_id}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=admin_id,
                text=(
                    f"🔔 PESANAN BARU #{order_id}\n\n"
                    f"👤 Customer: {order['nama_customer']}\n"
                    f"🍴 Menu: {order['menu_nama']} x{order['jumlah']}\n"
                    f"💰 Total: Rp {order['total']:,}\n"
                    f"📍 {order['metode_pengambilan']}\n\n"
                    f"Bukti transfer telah diupload."
                ),
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.error(f"Failed to notify admin {admin_id}: {e}")
    
    await update.message.reply_text(
        f"✅ Bukti transfer berhasil dikirim!\n\n"
        f"Pesanan #{order_id} sedang menunggu konfirmasi admin.\n"
        f"Anda akan mendapat notifikasi setelah pembayaran dikonfirmasi.\n\n"
        f"Gunakan /pesanan untuk cek status pesanan."
    )
    
    return ConversationHandler.END

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel order conversation"""
    await update.message.reply_text(
        "❌ Pesanan dibatalkan.\n\nGunakan /start untuk memulai lagi."
    )
    return ConversationHandler.END

# ============================================================================
# BOT HANDLERS - ADMIN
# ============================================================================

async def login_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin login with password"""
    await update.message.reply_text(
        "🔐 LOGIN ADMIN\n\n"
        "Masukkan password admin:"
    )
    return ADMIN_LOGIN_PASSWORD

async def receive_admin_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive admin password"""
    password = update.message.text
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    if password == admin_password:
        user_id = update.message.from_user.id
        if user_id not in ADMIN_TELEGRAM_IDS:
            ADMIN_TELEGRAM_IDS.append(user_id)
        
        await update.message.reply_text(
            "✅ Login berhasil!\n\n"
            "Gunakan /admin untuk mengakses menu admin."
        )
    else:
        await update.message.reply_text(
            "❌ Password salah!\n\n"
            "Silakan coba lagi dengan /loginadmin"
        )
    
    return ConversationHandler.END

async def show_admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin menu - accessible via /admin command"""
    user_id = update.message.from_user.id
    
    if user_id not in ADMIN_TELEGRAM_IDS:
        await update.message.reply_text("❌ Anda tidak memiliki akses admin!\n\nSilakan login terlebih dahulu dengan /loginadmin")
        return
    
    pending_count = len(get_pending_orders())
    keyboard = [
        [InlineKeyboardButton(f"📋 Pesanan Menunggu ({pending_count})", callback_data='admin_pending')],
        [InlineKeyboardButton("📊 Generate Laporan", callback_data='admin_laporan')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🔐 MENU ADMIN\n\n📊 Status:\n• Pesanan menunggu: {pending_count}\n\nPilih menu:",
        reply_markup=reply_markup)

async def show_admin_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin menu from callback query"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if user_id not in ADMIN_TELEGRAM_IDS:
        await query.answer("❌ Anda tidak memiliki akses admin!", show_alert=True)
        return
    
    await query.answer()
    pending_count = len(get_pending_orders())
    keyboard = [
        [InlineKeyboardButton(f"📋 Pesanan Menunggu ({pending_count})", callback_data='admin_pending')],
        [InlineKeyboardButton("📊 Generate Laporan", callback_data='admin_laporan')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"🔐 MENU ADMIN\n\n📊 Status:\n• Pesanan menunggu: {pending_count}\n\nPilih menu:",
        reply_markup=reply_markup)

async def show_pending_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show pending orders to admin"""
    query = update.callback_query
    await query.answer()
    
    orders = get_pending_orders()
    
    if not orders:
        try:
            await query.edit_message_text(
                "✅ Tidak ada pesanan yang menunggu konfirmasi.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Kembali", callback_data='admin_menu')
                ]])
            )
        except:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="✅ Tidak ada pesanan yang menunggu konfirmasi.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Kembali", callback_data='admin_menu')
                ]])
            )
        return
    
    text = "📋 PESANAN MENUNGGU KONFIRMASI\n\n"
    buttons = []
    
    for order in orders:
        text += (
            f"🆔 #{order['id']}\n"
            f"👤 {order['nama_customer']}\n"
            f"🍴 {order['menu_nama']} x{order['jumlah']}\n"
            f"💰 Rp {order['total']:,}\n"
            f"━━━━━━━━━━━━━━━━\n\n"
        )
        buttons.append([
            InlineKeyboardButton(f"� Lihat #{order['id']}", callback_data=f"view_proof_{order['id']}"),
            InlineKeyboardButton(f"✅ #{order['id']}", callback_data=f"approve_{order['id']}"),
            InlineKeyboardButton(f"❌ #{order['id']}", callback_data=f"reject_{order['id']}")
        ])
    
    buttons.append([InlineKeyboardButton("🔙 Kembali", callback_data='admin_menu')])
    reply_markup = InlineKeyboardMarkup(buttons)
    
    try:
        await query.edit_message_text(text, reply_markup=reply_markup)
    except:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=text,
            reply_markup=reply_markup
        )

async def view_payment_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View payment proof"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[2])
    order = get_order_by_id(order_id)
    
    if not order or not order['bukti_transfer']:
        await query.answer("Bukti transfer tidak ditemukan!", show_alert=True)
        return
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Konfirmasi", callback_data=f'approve_{order_id}'),
            InlineKeyboardButton("❌ Tolak", callback_data=f'reject_{order_id}')
        ],
        [InlineKeyboardButton("🔙 Kembali", callback_data='admin_pending')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    caption = (
        f"🧾 PESANAN #{order_id}\n\n"
        f"👤 Customer: {order['nama_customer']}\n"
        f"🍴 Menu: {order['menu_nama']} x{order['jumlah']}\n"
        f"💰 Total: Rp {order['total']:,}\n"
        f"📍 {order['metode_pengambilan']}"
    )
    
    await context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=order['bukti_transfer'],
        caption=caption,
        reply_markup=reply_markup
    )

async def approve_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Approve payment"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[1])
    order = get_order_by_id(order_id)
    
    if not order:
        await query.answer("Pesanan tidak ditemukan!", show_alert=True)
        return
    
    confirm_payment(order_id, approved=True)
    
    # Notify customer with status update buttons
    try:
        keyboard = [[InlineKeyboardButton("📦 Cek Status Pesanan", callback_data=f'check_status_{order_id}')]]
        await context.bot.send_message(
            chat_id=order['telegram_id'],
            text=(
                f"✅ PEMBAYARAN DIKONFIRMASI\n\n"
                f"Pesanan #{order_id} telah dikonfirmasi!\n"
                f"Status: Sedang diproses\n\n"
                f"Terima kasih telah berbelanja! 🙏"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.error(f"Failed to notify customer: {e}")
    
    # Show admin options to update order status
    keyboard = [
        [InlineKeyboardButton("👨‍🍳 Sedang Dibuat", callback_data=f'status_sedang_dibuat_{order_id}')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='admin_menu')]
    ]
    
    await query.edit_message_text(
        f"✅ Pembayaran pesanan #{order_id} telah dikonfirmasi.\n\nUpdate status pesanan:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def reject_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reject payment"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[1])
    order = get_order_by_id(order_id)
    
    if not order:
        await query.answer("Pesanan tidak ditemukan!", show_alert=True)
        return
    
    confirm_payment(order_id, approved=False)
    
    # Notify customer
    try:
        await context.bot.send_message(
            chat_id=order['telegram_id'],
            text=(
                f"❌ PEMBAYARAN DITOLAK\n\n"
                f"Pesanan #{order_id} ditolak.\n"
                f"Silakan hubungi admin untuk informasi lebih lanjut."
            )
        )
    except Exception as e:
        logger.error(f"Failed to notify customer: {e}")
    
    await query.edit_message_text(
        f"❌ Pembayaran pesanan #{order_id} telah ditolak.",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Kembali", callback_data='admin_menu')
        ]])
    )

async def generate_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate daily report"""
    query = update.callback_query
    await query.answer("Generating report...")
    
    today = datetime.now().strftime('%Y-%m-%d')
    filename = generate_daily_report(today)
    
    if not filename:
        await query.edit_message_text(
            "❌ Tidak ada data untuk laporan hari ini.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Kembali", callback_data='admin_menu')
            ]])
        )
        return
    
    # Send PDF
    with open(filename, 'rb') as pdf_file:
        await context.bot.send_document(
            chat_id=query.message.chat_id,
            document=pdf_file,
            filename=filename,
            caption=f"📊 Laporan Harian {today}"
        )
    
    await query.edit_message_text(
        "✅ Laporan berhasil digenerate!",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Kembali", callback_data='admin_menu')
        ]])
    )

async def update_status_sedang_dibuat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Update status to sedang dibuat"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[3])
    order = get_order_by_id(order_id)
    
    if not order:
        await query.answer("Pesanan tidak ditemukan!", show_alert=True)
        return
    
    update_order_status(order_id, 'sedang_dibuat')
    
    # Notify customer
    try:
        await context.bot.send_message(
            chat_id=order['telegram_id'],
            text=(
                f"👨‍🍳 PESANAN SEDANG DIBUAT\n\n"
                f"Pesanan #{order_id} sedang dibuat oleh chef kami!\n"
                f"Mohon tunggu sebentar ya 😊"
            )
        )
    except Exception as e:
        logger.error(f"Failed to notify customer: {e}")
    
    # Show next status options
    if order['metode_pengambilan'] == 'delivery':
        keyboard = [
            [InlineKeyboardButton("🚚 Sedang Diantar", callback_data=f'status_sedang_diantar_{order_id}')],
            [InlineKeyboardButton("🔙 Kembali", callback_data='admin_menu')]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("✅ Siap Diambil", callback_data=f'status_siap_diambil_{order_id}')],
            [InlineKeyboardButton("🔙 Kembali", callback_data='admin_menu')]
        ]
    
    await query.edit_message_text(
        f"✅ Status pesanan #{order_id} diupdate: Sedang Dibuat\n\nUpdate status selanjutnya:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def update_status_sedang_diantar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Update status to sedang diantar (delivery)"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[3])
    order = get_order_by_id(order_id)
    
    if not order:
        await query.answer("Pesanan tidak ditemukan!", show_alert=True)
        return
    
    update_order_status(order_id, 'sedang_diantar')
    
    # Notify customer with confirmation button
    try:
        keyboard = [[InlineKeyboardButton("✅ Konfirmasi Sudah Diterima", callback_data=f'confirm_received_{order_id}')]]
        await context.bot.send_message(
            chat_id=order['telegram_id'],
            text=(
                f"🚚 PESANAN SEDANG DIANTAR\n\n"
                f"Pesanan #{order_id} sedang dalam perjalanan ke alamat Anda!\n"
                f"Mohon tunggu kurir kami ya 😊\n\n"
                f"Setelah pesanan diterima, klik tombol di bawah:"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.error(f"Failed to notify customer: {e}")
    
    await query.edit_message_text(
        f"✅ Status pesanan #{order_id} diupdate: Sedang Diantar",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Kembali", callback_data='admin_menu')
        ]])
    )

async def update_status_siap_diambil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Update status to siap diambil (pickup)"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[3])
    order = get_order_by_id(order_id)
    
    if not order:
        await query.answer("Pesanan tidak ditemukan!", show_alert=True)
        return
    
    update_order_status(order_id, 'siap_diambil')
    
    # Notify customer with confirmation button
    try:
        keyboard = [[InlineKeyboardButton("✅ Konfirmasi Sudah Diambil", callback_data=f'confirm_received_{order_id}')]]
        await context.bot.send_message(
            chat_id=order['telegram_id'],
            text=(
                f"✅ PESANAN SIAP DIAMBIL\n\n"
                f"Pesanan #{order_id} sudah siap!\n"
                f"Silakan datang ke {WARUNG_NAME} untuk mengambil pesanan Anda 😊\n\n"
                f"Setelah pesanan diambil, klik tombol di bawah:"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.error(f"Failed to notify customer: {e}")
    
    await query.edit_message_text(
        f"✅ Status pesanan #{order_id} diupdate: Siap Diambil",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Kembali", callback_data='admin_menu')
        ]])
    )

async def confirm_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Customer confirms order received"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[2])
    order = get_order_by_id(order_id)
    
    if not order:
        await query.answer("Pesanan tidak ditemukan!", show_alert=True)
        return
    
    update_order_status(order_id, 'selesai')
    
    await query.edit_message_text(
        f"✅ PESANAN SELESAI\n\n"
        f"Terima kasih telah mengkonfirmasi penerimaan pesanan #{order_id}!\n\n"
        f"Kami harap Anda menikmati {order['menu_nama']} kami 😊\n\n"
        f"Sampai jumpa lagi! 🙏"
    )
    
    # Notify admin
    for admin_id in ADMIN_TELEGRAM_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"✅ Pesanan #{order_id} telah dikonfirmasi diterima oleh customer."
            )
        except Exception as e:
            logger.error(f"Failed to notify admin: {e}")

async def check_order_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check order status"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[2])
    order = get_order_by_id(order_id)
    
    if not order:
        await query.answer("Pesanan tidak ditemukan!", show_alert=True)
        return
    
    # Status icons
    status_icons = {
        'menunggu': '⏸️',
        'diproses': '🔄',
        'sedang_dibuat': '👨‍🍳',
        'sedang_diantar': '🚚',
        'siap_diambil': '✅',
        'selesai': '✅',
        'ditolak': '❌'
    }
    
    status_text = {
        'menunggu': 'Menunggu Pembayaran',
        'diproses': 'Sedang Diproses',
        'sedang_dibuat': 'Sedang Dibuat',
        'sedang_diantar': 'Sedang Diantar',
        'siap_diambil': 'Siap Diambil',
        'selesai': 'Selesai',
        'ditolak': 'Ditolak'
    }
    
    icon = status_icons.get(order['status_pesanan'], '❓')
    status = status_text.get(order['status_pesanan'], order['status_pesanan'])
    
    text = (
        f"📦 STATUS PESANAN #{order_id}\n\n"
        f"🍴 Menu: {order['menu_nama']} x{order['jumlah']}\n"
        f"💰 Total: Rp {order['total']:,}\n"
        f"📍 Metode: {order['metode_pengambilan']}\n\n"
        f"{icon} Status: {status}"
    )
    
    await query.edit_message_text(text)

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Start the bot"""
    # Initialize database
    init_database()
    
    # Auto-seed menu if empty (for Railway deployment)
    try:
        menu_items = get_all_menu()
        if not menu_items:
            logger.info("No menu found, running auto-seed...")
            from init_railway import init_railway_db
            init_railway_db()
    except Exception as e:
        logger.warning(f"Auto-seed skipped: {e}")
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Conversation handler for ordering (complete flow)
    order_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(order_menu, pattern='^pesan_')],
        states={
            ASKING_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_quantity)],
        },
        fallbacks=[CommandHandler('cancel', cancel_order)],
        per_message=False,
    )
    
    # Conversation handler for delivery address
    delivery_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(choose_delivery_method, pattern='^delivery$')],
        states={
            ASKING_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_address)],
        },
        fallbacks=[CommandHandler('cancel', cancel_order)],
        per_message=False,
    )
    
    # Conversation handler for payment proof
    payment_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(payment_confirmation, pattern='^paid_')],
        states={
            ASKING_PAYMENT_PROOF: [MessageHandler(filters.PHOTO, receive_payment_proof)],
        },
        fallbacks=[CommandHandler('cancel', cancel_order)],
        per_message=False,
    )
    
    # Conversation handler for admin login
    admin_login_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('loginadmin', login_admin)],
        states={
            ADMIN_LOGIN_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_admin_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel_order)],
    )
    
    # Command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('admin', show_admin_menu))
    application.add_handler(CommandHandler('pesanan', pesanan_command))
    
    # Conversation handlers
    application.add_handler(order_conv_handler)
    application.add_handler(delivery_conv_handler)
    application.add_handler(payment_conv_handler)
    application.add_handler(admin_login_conv_handler)
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(show_menu, pattern='^show_menu$'))
    application.add_handler(CallbackQueryHandler(my_orders, pattern='^my_orders$'))
    application.add_handler(CallbackQueryHandler(back_to_main, pattern='^back_to_main$'))
    application.add_handler(CallbackQueryHandler(choose_delivery_method, pattern='^pickup$'))
    
    # Admin callbacks
    application.add_handler(CallbackQueryHandler(show_admin_menu_callback, pattern='^admin_menu$'))
    application.add_handler(CallbackQueryHandler(show_pending_orders, pattern='^admin_pending$'))
    application.add_handler(CallbackQueryHandler(view_payment_proof, pattern='^view_proof_'))
    application.add_handler(CallbackQueryHandler(approve_payment, pattern='^approve_'))
    application.add_handler(CallbackQueryHandler(reject_payment, pattern='^reject_'))
    application.add_handler(CallbackQueryHandler(generate_report, pattern='^admin_laporan$'))
    
    # Status update callbacks (admin)
    application.add_handler(CallbackQueryHandler(update_status_sedang_dibuat, pattern='^status_sedang_dibuat_'))
    application.add_handler(CallbackQueryHandler(update_status_sedang_diantar, pattern='^status_sedang_diantar_'))
    application.add_handler(CallbackQueryHandler(update_status_siap_diambil, pattern='^status_siap_diambil_'))
    
    # Customer callbacks
    application.add_handler(CallbackQueryHandler(confirm_received, pattern='^confirm_received_'))
    application.add_handler(CallbackQueryHandler(check_order_status, pattern='^check_status_'))
    
    # Start bot
    logger.info("Bot started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
