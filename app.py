
# Nama file: app.py
# Tujuan: Membuat server API Flask untuk layanan kategorisasi.

import os
from flask import Flask, request, jsonify
import Kategorisasi # <--- PERBAIKAN DI SINI

app = Flask(__name__)

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
        # Panggil fungsi dari modul Kategorisasi
        hasil_kategori = Kategorisasi.kategorisasi_otomatis(data_input)
        return jsonify(hasil_kategori)
    except (KeyError, TypeError, ValueError) as e:
        # Menangkap error validasi dari modul Kategorisasi
        return jsonify({"error": f"Input data tidak valid: {str(e)}"}), 400
    except Exception as e:
        # Menangkap error lain yang mungkin terjadi
        print(f"Error di /categorize/transaction: {str(e)}")
        return jsonify({"error": "Terjadi kesalahan internal saat melakukan kategorisasi."}), 500
    
if __name__ == '__main__':
    # Port diambil dari environment variable, default ke 5000 jika tidak ada
    port = int(os.environ.get("PORT", 5000))
    # Host harus 0.0.0.0 agar bisa diakses dari luar container/server
    app.run(host="0.0.0.0", port=port)
