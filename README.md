# Toko Bola ⚽

Proyek ini dibuat untuk memenuhi tugas-individu mata kuliah **PBP**

---

## 🌍 Link Aplikasi

🔗 [klik link ini untuk menuju ke website](https://izzudin-abdul-tokobola.pbp.cs.ui.ac.id/)  

---
#  📝Tugas 2
## ✅ Step by Step Implementasi
1. **Inisialisasi Proyek Django**
   - Membuat virtual environment: `python -m venv env`
   - Mengaktifkan env: `env\Scripts\activate` 
   - Install Django: `pip install django`
   - Membuat project: `django-admin startproject tokobola .`
   - Membuat app: `py manage.py main`

2. **Mendaftarkan App**
   - Menambahkan `main` ke dalam `INSTALLED_APPS` di `settings.py`.

3. **Routing**
   - Menambahkan `path('', include('main.urls'))` di `urls.py` project utama.
   - Membuat file `urls.py` di `main`
     
4. **Views**
   - Membuat fungsi `show_main` di `views.py` untuk merender template HTML.

5. **Template**
   - Buat folder `templates/` di dalam `main`.
   - Menambahkan `main.html` yang berisi konten yang akan ditampilkan di website.

6. **Deployment**
   - Setup repository GitHub.
   - Deploy ke Pacil Web Service

---
## 📊 Alur Request & Response Django
  ```mermaid
flowchart TD
    A[Request via Browser] -->|Browser mengirim request ke server Django| B[urls.py]
    B -->|URL dicocokkan, lalu diarahkan ke view| C[views.py]
    C ---->|View meminta atau memodifikasi data di database| D[models.py]
    C ---->|View mengirim data untuk dirender di template| E[HTML Template]
    D -->|Data dari database dikembalikan ke view| C
    E -->|Template menghasilkan HTML jadi| C
    C -->|HTML dikirim kembali ke browser sebagai response| F[HTTP Response to Client]
```

---
## 🛠 Peran settings.py
settings.py adalah file konfigurasi utama Django yang berfungsi untuk:
 - Menyimpan konfigurasi database (SQLite/PostgreSQL)
 - Mendaftarkan aplikasi (INSTALLED_APPS)
 - Menentukan middleware
 - Mengatur jalur template dan static file
 - Menentukan konfigurasi keamanan (secret key, debug mode, allowed hosts)

---
## 🗄️ Cara Kerja Migrasi Database
  - Definisikan model di models.py
  - Jalankan `py manage.py makemigrations` → Django membuat blueprint migrasi
  - Jalankan `py manage.py migrate` → migrasi diterapkan ke database
  - Django menyimpan riwayat migrasi, sehingga setiap perubahan yang terjadi pada model bisa dilacak

---
## 🤔 Kenapa Django?
  - Batteries included: banyak fitur bawaan (auth, ORM, admin)
  - Struktur rapi: memisahkan concerns (urls, views, models, templates)
  - Cocok untuk pemula: dokumentasi lengkap, komunitas besar
  - Dipakai industri: banyak perusahaan masih menggunakan Django.
  - Memperkenalkan konsep dasar web dev seperti request-response, MVC/MVT, database, dan deployment.

---
## 💬 Feedback untuk ASDOS (Tutorial 1)
So far, kaka asdos sudah sangat baik dalam membantu dalam mengerjakan tutorial, baik saat sesi offline maupun saat sesi online. 
Mungkin pesanku untuk kaka asdos: semoga selalu sabar dan semangat dalam membimbing kami 😁

---
#  📝Tugas 3
## ✅ Step by Step Implementasi
   - Membuat view untuk menampilkan daftar produk (show_main), menambahkan produk (create_product), menampilkan detail (show_product).
   - Menambahkan template main.html dan create_product.html.
   - Membuat URL routing untuk semua view.
   - Menambahkan fitur delivery data (XML, JSON, JSON by id) dengan serializers di views.py.
   - Mengecek hasil di endpoint /xml/, /json/, /xml/<id>/, /json/<id>/.
   - Deploy ke Pacil Web Service.

---
## 📦 Mengapa Data Delivery Dibutuhkan?
Data delivery diperlukan agar data dari server dapat dikirim ke client atau aplikasi lain dalam format yang konsisten, dapat dipahami, dan mudah diproses. Tanpa data delivery, aplikasi hanya bisa menampilkan data statis, tidak bisa dinamis.

---
## ⚔️ JSON VS XML
   - XML: lebih verbose (bertele-tele), banyak tag, cocok untuk dokumen kompleks.
   - JSON: ringan, lebih mudah dibaca manusia, langsung dipetakan ke struktur data (dictionary, list).
   - Alasan JSON lebih populer: sintaks singkat, cepat diproses, langsung kompatibel dengan JavaScript.

---
## ✅ Fungsi `is_valid()` pada Form Django
- hal ini dibutuhkan untuk mencegah data-data yang tidak sesuai ketentuan masuk lewat form
- jika data yang dimasukkan `valid` atau sesuai ketentuan, maka return true dan data bisa diakses
- jika data yang dimasukkan `tidak valid` atau tidak sesuai ketentuan, maka return false dan akan menampilkan error

---
## 🤔 Kenapa Butuh csrf_token?
   - `csrf_token` mencegah serangan Cross Site Request Forgery, yaitu serangan yang membuat oknum akan membuat pengguna seolah-oleh meminta request tertentu pada website dan kemudian web akan  mengeksekusi permintaan tersebut.
   - Jika tidak ada token, penyerang bisa membuat form palsu di luar aplikasi kita yang mengeksekusi aksi berbahaya (misal: transfer uang, ganti password).
   - dengan csrf_token hanya request dari form asli yang diterima oleh server

## 📸 Screenshoot Postman
   - XML function
     <img width="1986" height="1291" alt="Screenshot 2025-09-17 082608" src="https://github.com/user-attachments/assets/34325ebb-323c-48c5-a150-3252b33ddd3d" />
   - XML by ID function
     <img width="2003" height="984" alt="Screenshot 2025-09-17 082632" src="https://github.com/user-attachments/assets/e4533df9-0b4d-4706-bd52-a98b103fbc0d" />
   - JSON function
     <img width="1983" height="1285" alt="Screenshot 2025-09-17 082901" src="https://github.com/user-attachments/assets/09fe13b6-393f-4ca1-a4ea-7493c1f4da6a" />
   - JSON by ID function
     <img width="1985" height="995" alt="Screenshot 2025-09-17 082816" src="https://github.com/user-attachments/assets/c881a647-e84f-4276-af4d-d8e85be1dbeb" />

---
## 💬 Feedback untuk ASDOS (Tutorial 2)
So far, kaka asdos sudah sangat baik dalam membantu dalam mengerjakan tutorial, baik saat sesi offline maupun saat sesi online. 
Mungkin pesanku untuk kaka asdos: semoga selalu sabar dan semangat dalam membimbing kami 😁

---
## ✨ Credit
Program ini dibuat oleh Izzudin Abdul Rasyid - 2406495786 - PBP D









  
