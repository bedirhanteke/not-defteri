# GNOME Notes App (Fedora / GNOME)

Fedora Linux ve GNOME masaüstü ortamı için tasarlanmış; **Python (PyGObject)**, **GTK 4** ve **libadwaita** ile geliştirilmiş sade, hızlı ve tamamen yerel bir not defteri uygulamasıdır. 

Tüm verileriniz internet bağlantısına ihtiyaç duymadan, tamamen çevrimdışı olarak yerel diskteki SQLite veritabanında saklanır.

---

## 🌟 Özellikler

* **Yerel ve Çevrimdışı Depolama:** Notlarınız `~/.local/share/com.example.Notes/notes.db` konumunda SQLite olarak güvenle saklanır.
* **Klasör & Sabitleme (Pin) Yapısı:** Notları klasörlere ayırabilir, önemli notlarınızı en üste sabitleyebilirsiniz.
* **Sade ve Hızlı Metin Editörü:** Kolay ve hızlı not alma odaklı modern editör paneli.
* **GNOME Human Interface Guidelines (HIG) Uyumlu:** `Adw.OverlaySplitView`, `Adw.HeaderBar` ve `Adw.Breakpoint` mimarisi sayesinde pencere boyutu daraldığında otomatik olarak mobil/dar ekrana uyum sağlar (Responsive).
* **Anlık Arama:** Başlık veya içerik bazlı, gecikmesiz (debounced) canlı arama.

---

## 📸 Ekran Görüntüsü

*(Ekran görüntüsü eklenecek)*

```
+-------------------+--------------------+----------------------------------+
| Klasörler         | Not Listesi        | Editör                           |
|-------------------|--------------------|----------------------------------|
| [ ] Tüm Notlar    | 📌 Önemli Not      | Not Başlığı...                   |
| [ ] İş            |   Son güncellem... | -------------------------------- |
| [ ] Kişisel       |                    | Not içeriği buraya yazılır...    |
+-------------------+--------------------+----------------------------------+
```

---

## 🛠️ Bağımlılıklar ve Kurulum

### Sistem Bağımlılıkları (Fedora Linux)

Uygulama yerel GNOME kütüphanelerini kullandığı için temel bağımlılıklar Fedora paket yöneticisi `dnf` üzerinden kurulur:

```bash
sudo dnf install python3-gobject gtk4 libadwaita
```

---

## 🚀 Çalıştırma Talimatları

### Yöntem 1: Doğrudan Çalıştırma (Geliştirme Modu)

Depoyu klonladıktan sonra proje dizininde aşağıdaki komutu çalıştırmanız yeterlidir:

```bash
python3 run.py
```

### Yöntem 2: Flatpak İle Derleme ve Kurulum

`flatpak-builder` ile izole bir biçimde paketleyip çalıştırmak için:

```bash
flatpak-builder --user --install --force-clean build-dir com.example.Notes.json
flatpak run com.example.Notes
```

### Yöntem 3: RPM Paketi Derleme (Fedora)

Proje kökündeki `notes.spec` dosyasını kullanarak kendi RPM paketinizi oluşturabilirsiniz:

```bash
# RPM derleme dizin yapısını hazırlayın
rpmdev-setuptree

# Projeyi tar.gz olarak paketleyip SOURCES dizinine kopyalayın
tar -czvf notes-1.0.0.tar.gz app/ data/ run.py notes.spec
cp notes-1.0.0.tar.gz ~/rpmbuild/SOURCES/

# RPM paketini derleyin
rpmbuild -ba notes.spec

# Oluşan paketi kurun
sudo dnf install ~/rpmbuild/RPMS/noarch/notes-1.0.0-1.fc*.noarch.rpm
```

---

## 📂 Proje Yapısı

```
.
├── app/
│   ├── db.py          # SQLite veritabanı mantığı ve sorgular
│   ├── main.py        # Adw.Application giriş noktası
│   └── ui/
│       ├── editor.py  # Not düzenleme paneli ve başlık çubuğu
│       ├── note_list.py # Not listesi ve arama çubuğu
│       ├── sidebar.py # Klasör listesi paneli
│       └── window.py  # Adw.ApplicationWindow ve split view yerleşimi
├── data/              # Desktop ve ikon dosyaları
├── tests/             # Veritabanı ve birim testleri
├── run.py             # Uygulama başlatıcı betik
├── notes.spec         # Fedora RPM paket spesifikasyonu
├── com.example.Notes.json # Flatpak derleme bildirimi
├── LICENSE            # GPLv3 Lisans Metni
└── README.md
```

---

## 📜 Lisans

Bu proje **GNU General Public License v3.0 (GPLv3)** ile lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakabilirsiniz.
