import telebot
import pandas as pd
import os
from flask import Flask
from threading import Thread

# --- DUMMY WEB SERVER UNTUK MENGELUARKAN PORT DI RENDER (FREE TIER) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Telegram Aktif 24 Jam!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------------------------------------

TOKEN = '8929131903:AAFo-p8cP7DpBbAE3HiIwIENvdPRsIayPs0'
bot = telebot.TeleBot(TOKEN)

# Membaca data Excel
df = pd.read_excel('data_site.xlsx')
df.columns = df.columns.str.strip()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Silakan kirimkan Site ID untuk mengecek detail informasi site.")

@bot.message_handler(func=lambda message: True)
def cari_site(message):
    site_id_input = message.text.strip()
    hasil = df[df['Site ID'].astype(str).str.upper() == site_id_input.upper()]
    
    if not hasil.empty:
        data = hasil.iloc[0]
        lat = data.get('Latitude', '')
        long = data.get('Longitude', '')
        
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
• Coordinate: {lat}, {long}

*INFRASTRUKTUR & TOWER*
• PLN ID: {data.get('PLN ID', '-')}
• Field Type: {data.get('Field Type', '-')}
• Hub Type: {data.get('Hub Type', '-')}
• TOCO: {data.get('TOCO', '-')}
• ID ToCo: {data.get('ID ToCo', '-')}

Link Gmaps:
https://maps.google.com/?q={lat},{long}"""

        bot.reply_to(message, balasan, parse_mode='Markdown')
    else:
        bot.reply_to(message, f"❌ Site ID *{site_id_input}* tidak ditemukan.", parse_mode='Markdown')

if __name__ == '__main__':
    keep_alive()          # Menjalankan server Flask di latar belakang
    bot.remove_webhook()   # Memastikan tidak ada webhook tersisa
    print("Bot sedang berjalan di Render...")
    bot.polling(non_stop=True)
