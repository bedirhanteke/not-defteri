# Not Defteri (GNOME Notes)

Fedora Linux ve GNOME masaüstü ortamı için modern GTK 4 ve libadwaita teknolojileriyle geliştirilmiş, yerel SQLite veritabanı tabanlı, gizlilik odaklı ve hafif bir not alma uygulamasıdır.

Tüm notlarınız internet bağlantısına ihtiyaç duymadan, üçüncü taraf sunuculara bağımlı kalmaksızın tamamen bilgisayarınızda yerel olarak saklanır.

---

## 📸 Ekran Görüntüsü

![Not Defteri Ekran Görüntüsü](data/screenshot.png)

> *Görsel yer tutucudur. Uygulama arayüzünün ekran görüntüsü buraya eklenecektir.*

---

## ✨ Özellikler

* **Klasörlerle Not Organizasyonu:** Notlarınızı özel klasörler altında gruplayın veya tüm notlarınızı tek bir listede ("Tüm Notlar") görüntüleyin.
* **Gelişmiş Klasör Yönetimi:** Yeni klasör oluşturma, var olan klasörü yeniden adlandırma ve silme desteği. Bir klasör silindiğinde içerisindeki notlar kaybolmaz, güvenle "Tüm Notlar" görünümüne aktarılır.
* **Zengin Sağ Tık (Bağlam) Menüsü:** Not listesindeki herhangi bir nota sağ tıklayarak:
  * **Yeniden Adlandır:** Not başlığını doğrudan diyalog üzerinden güncelleyin.
  * **Klasör Değiştir:** Yan açılan alt menüden (sub-popover) notu dilediğiniz klasöre taşıyın veya "Klasörsüz (Tüm Notlar)" seçeneği ile klasörden çıkarın.
  * **Sabitle / Sabitlemeyi Kaldır:** Önemli notları listenin en üstüne sabitleyin.
  * **Notu Sil:** Onay penceresi ile notu güvenle silin.
* **Akıllı Otomatik Kaydetme:** Not başlığı veya gövdesinde değişiklik yapıldığı anda yazma akışını bölmeden 500 ms içinde arka planda otomatik kaydedilir.
* **Anlık ve Canlı Arama:** Arama kutusuna yazıldığı anda hem başlıklar hem de not içerikleri taranarak sonuçlar anında listelenir (300 ms debounced).
* **GNOME HIG (Human Interface Guidelines) Uyumu:** Modern Adwaita tasarım dili, `Adw.OverlaySplitView` ile 3 sütunlu düzen (Klasörler | Not Listesi | Editör), `Adw.ToastOverlay` ile işlem bildirimleri ve boş klasör durumlarında `Adw.StatusPage` yönlendirmesi.
* **Tam Duyarlı (Responsive) Tasarım:** `Adw.Breakpoint` mimarisi sayesinde pencere boyutu küçüldüğünde (800px ve 600px sınırlarında) kenar çubukları otomatik daralır, küçük ekranlarda ve mobil görünümde kusursuz gezinme sunar.
* **Sistem Temasıyla Uyumlu (Karanlık / Aydınlık Mod):** GNOME sistem teması tercihini otomatik algılar; açık ve koyu temayı yerel libadwaita renk paletiyle kusursuz destekler.
* **Hızlı Klavye Kısayolları:** Hızlıca yeni not eklemek için `Ctrl+N` kısayol desteği.
* **Tamamen Yerel ve Güvenli Depolama:** Verileriniz `~/.local/share/com.example.Notes/notes.db` konumunda yerel SQLite veritabanında tutulur.

---

## 🛠️ Teknoloji Yığını

* **Programlama Dili:** Python 3
* **Kullanıcı Arayüzü Araç Seti:** GTK 4 (`gi.repository.Gtk`)
* **Tasarım Kütüphanesi:** libadwaita 1 (`gi.repository.Adw`)
* **Python Bağlayıcıları:** PyGObject (`python3-gobject`)
* **Veritabanı Katmanı:** SQLite 3 (Python yerel `sqlite3` modülü)
* **Paketleme Formatları:** Flatpak (`com.example.Notes.json`), RPM (`notes.spec`)

---

## 🚀 Kurulum ve Çalıştırma

Uygulamayı ihtiyacınıza göre doğrudan kaynak kodundan çalıştırabilir veya paketleyerek sisteminize entegre edebilirsiniz.

### Yöntem 1: Doğrudan Çalıştırma (Tavsiye Edilen Geliştirici Yolu)

Fedora üzerinde gerekli sistem paketlerini yükleyin ve uygulamayı başlatın:

```bash
# Gerekli sistem kütüphanelerini kurun
sudo dnf install python3 python3-gobject gtk4 libadwaita

# Depo dizinine gidin ve çalıştırın
python3 run.py
```

### Yöntem 2: Flatpak ile Kurulum ve Çalıştırma

Uygulamayı izole sandbox ortamında derlemek ve çalıştırmak için `flatpak-builder` kullanabilirsiniz:

```bash
# Flatpak derleyicisini kurun (kurulu değilse)
sudo dnf install flatpak flatpak-builder

# GNOME Platform ve SDK çalışma zamanlarını ekleyin
flatpak install flathub org.gnome.Platform//46 org.gnome.Sdk//46

# Uygulamayı derleyin ve kullanıcınıza kurun
flatpak-builder --user --install --force-clean build-dir com.example.Notes.json

# Uygulamayı başlatın
flatpak run com.example.Notes
```

### Yöntem 3: RPM Paketi Derleme (Fedora / RHEL)

Sisteminiz için standart bir `.rpm` paketi oluşturup kurmak için:

```bash
# RPM geliştirme araçlarını kurun
sudo dnf install rpmdevtools rpm-build

# RPM derleme dizin ağacını oluşturun (~/rpmbuild)
rpmdev-setuptree

# Kaynak kod arşivini hazırlayıp SOURCES dizinine kopyalayın
tar --exclude='.git' -czvf notes-1.0.0.tar.gz app/ data/ run.py notes.spec
cp notes-1.0.0.tar.gz ~/rpmbuild/SOURCES/

# RPM paketini derleyin
rpmbuild -ba notes.spec

# Üretilen RPM paketini sisteme kurun
sudo dnf install ~/rpmbuild/RPMS/noarch/notes-1.0.0-1.fc*.noarch.rpm

# Uygulamayı sistem komutuyla veya uygulama menüsünden başlatın
notes
```

---

## 📖 Kullanım

1. **Yeni Not Oluşturma:** Üst çubukta bulunan `+` butonuna tıklayın veya klavyeden `Ctrl+N` tuşlarına basın.
2. **Klasör Yönetimi:** Sol kenar çubuğunun üstündeki `+` butonuna basarak yeni bir klasör oluşturun. Klasör seçeneklerine (yeniden adlandırma veya silme) klasörün yanındaki üç nokta butonundan veya sağ tıklayarak erişebilirsiniz.
3. **Not Taşıma:** Not listesinde bir nota sağ tıklayıp **"Klasör Değiştir ›"** menüsünü açın ve taşımak istediğiniz klasörü seçin.
4. **Arama Yapma:** Not listesinin üst kısmındaki arama alanına bir kelime yazarak notlarınız arasında anında filtreleme yapın.
5. **Düzenleme ve Kaydetme:** Başlık veya gövde metnini değiştirdiğinizde kaydetme işlemi otomatik olarak gerçekleşir, manuel kaydetmeye gerek yoktur.

---

## 📂 Proje Yapısı

```text
.
├── app/                           # Uygulama kaynak kodları
│   ├── __init__.py                # Paket başlatıcı
│   ├── db.py                      # SQLite veritabanı şeması, CRUD ve arama sorguları
│   ├── main.py                    # Adw.Application uygulaması ve yaşam döngüsü
│   └── ui/                        # Kullanıcı arayüzü bileşenleri
│       ├── editor.py              # Not başlığı, metin düzenleyici, sabitleme ve silme paneli
│       ├── note_list.py           # Not listesi, arama kutusu ve sağ tık bağlam menüleri
│       ├── sidebar.py             # Klasör listesi ve klasör yönetim paneli
│       └── window.py              # Adw.ApplicationWindow, responsive split-view ve kısayollar
├── data/                          # Masaüstü entegrasyonu ve grafik dosyaları
│   ├── com.example.Notes.desktop  # GNOME masaüstü başlatıcı dosyası
│   └── com.example.Notes.svg      # Uygulama vektör ikonu
├── icons/                         # Çeşitli boyutlarda hicolor uygulama ikonları
├── tests/                         # Otomatik birim ve entegrasyon testleri
│   ├── test_db.py                 # Veritabanı işlemleri birim testleri
│   └── test_folder_note_flow.py   # Klasör-not taşıma ve otomatik kaydetme akış testleri
├── com.example.Notes.json         # Flatpak manifest dosyası
├── notes.spec                     # Fedora/RPM paketleme tanımlama dosyası
├── requirements.txt               # Bağımlılık dokümantasyonu
├── run.py                         # Uygulama giriş noktası ve başlatıcı betik
├── LICENSE                        # GNU General Public License v3.0 lisans metni
└── README.md                      # Proje dokümantasyonu
```

---

## 🧪 Testleri Çalıştırma

Projeye ait birim ve entegrasyon testlerini çalıştırmak için:

```bash
python3 -m unittest discover tests
```

---

## 🤝 Katkıda Bulunma

1. Bu depoyu çatallayın (Fork).
2. Özelliğiniz için yeni bir dal (branch) açın (`git checkout -b feature/yeni-ozellik`).
3. Değişikliklerinizi commit edin (`git commit -m 'Feat: Yeni özellik eklendi'`).
4. Dalınızı uzak depoya gönderin (`git push origin feature/yeni-ozellik`).
5. Bir Çekme İsteği (Pull Request) oluşturun.

---

## 📜 Lisans

Bu proje **GNU General Public License v3.0 (GPLv3)** ile lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasını inceleyebilirsiniz.
