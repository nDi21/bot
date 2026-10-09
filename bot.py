import telebot
import pandas as pd

TOKEN = '8929131903:AAFo-p8cP7DpBbAE3HiIwIENvdPRsIayPs0'
bot = telebot.TeleBot(TOKEN)

# Membaca file Excel Anda
# Sesuaikan nama file jika berbeda
df = pd.read_excel('data_site.xlsx')

# Menghapus spasi berlebih pada nama kolom (jika ada)
df.columns = df.columns.str.strip()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Silakan kirimkan Site ID untuk mengecek detail informasi site.")

@bot.message_handler(func=lambda message: True)
def cari_site(message):
    site_id_input = message.text.strip()
    
    # Mencari data berdasarkan kolom 'Site ID' di Excel Anda
    hasil = df[df['Site ID'].astype(str).str.upper() == site_id_input.upper()]
    
    if not hasil.empty:
        data = hasil.iloc[0]
        
        # Ambil nilai Latitude dan Longitude dari kolom P dan Q
        lat = data.get('Latitude', '')
        long = data.get('Longitude', '')

        # Susun format balasan berdasarkan kolom Excel Anda
        balasan = f"""*DETAIL INFORMASI SITE*
============================================
*INFORMASI UTAMA*
• Site ID: {data.get('Site ID', '-')}
• Old Site ID: {data.get('Old Site ID', '-')}
• Site Name: {data.get('Site Name', '-')}
• Region: {data.get('Region', '-')}
• Area CL: {data.get('Area CL', '-')}
• Alamat: {data.get('Alamat', '-')}
• Cluster: {data.get('Cluster', '-')}
• ROH: {data.get('ROH', '-')}
• VIP / VVIP: {data.get('VIP / VVIP', '-')}
• Coordinate: {lat}, {long}

*INFRASTRUKTUR & TOWER*
• PLN ID: {data.get('PLN ID', '-')}
• Field Type: {data.get('Field Type', '-')}
• Hub Type: {data.get('Hub Type', '-')}
• TOCO: {data.get('TOCO', '-')}
• ID ToCo: {data.get('ID ToCo', '-')}
• OWS TE: {data.get('OWS TE', '-')}
• DWS CME: {data.get('DWS CME', '-')}

Link Gmaps:
https://maps.google.com/?q={lat},{long}"""

        bot.reply_to(message, balasan, parse_mode='Markdown')
    else:
        bot.reply_to(message, f"❌ Site ID *{site_id_input}* tidak ditemukan.", parse_mode='Markdown')

print("Bot sedang berjalan...")
bot.polling()