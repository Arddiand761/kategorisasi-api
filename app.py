# Nama file: app.py
import os
from flask import Flask, request, jsonify
import Kategorisasi

# --- SETUP LOGGING ---
import logging
from logging.handlers import RotatingFileHandler

# Pastikan aplikasi memiliki izin untuk menulis ke file ini
log_file = 'app_errors.log' 
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=3)
handler.setLevel(logging.ERROR) # Hanya catat error dan yang lebih parah
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)
handler.setFormatter(formatter)
# --- AKHIR SETUP LOGGING ---

app = Flask(__name__)
# Menambahkan handler ke logger aplikasi Flask
app.logger.addHandler(handler)

# Menambahkan endpoint untuk health check
@app.route('/')
def home():
    """Endpoint untuk health check."""
    status_model = Kategorisasi.dapatkan_status_model_kategorisasi()
    return jsonify({
        "message": "Selamat Datang di API Kategorisasi Transaksi",
        "status_model": status_model
    })

@app.route('/categorize/transaction', methods=['POST'])
def categorize_transaction_route():
    if not request.is_json:
        return jsonify({"error": "Request harus dalam format JSON"}), 400
    
    try:
        data_input = request.get_json()
        hasil_kategori = Kategorisasi.kategorisasi_otomatis(data_input)
        return jsonify(hasil_kategori)
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Input data tidak valid: {str(e)}"}), 400
    except Exception as e:
        # --- PERUBAHAN DI SINI ---
        # Mencatat traceback lengkap ke file log
        app.logger.error('Terjadi kesalahan internal tak terduga', exc_info=True)
        return jsonify({"error": "Terjadi kesalahan internal saat melakukan kategorisasi."}), 500
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
