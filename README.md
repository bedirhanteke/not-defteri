# Not Defteri

Fedora ve GNOME masaüstü ortamı için Python, GTK 4 ve libadwaita ile geliştirilmiş yerel bir not defteri uygulamasıdır. Notlar yerel SQLite veritabanında saklanır.

---

<img width="1192" height="788" alt="image" src="https://github.com/user-attachments/assets/f548d689-bc78-4296-ad80-63229cb36cbe" />


---

## Özellikler

- **Klasör yönetimi:** Notlar klasörlere ayrılabilir; klasör oluşturulabilir, yeniden adlandırılabilir ve silinebilir (silinen klasördeki notlar "Tüm Notlar" listesine aktarılır).
- **Klasör değiştirme:** Not listesindeki sağ tık menüsünden notlar başka bir klasöre taşınabilir veya "Klasörsüz" yapılabilir.
- **Not işlemleri:** Notlar sağ tık menüsünden yeniden adlandırılabilir, silinebilir ve listenin en üstüne sabitlenebilir.
- **Otomatik kaydetme:** Başlık ve içerik değişiklikleri 500 ms sonra arka planda kaydedilir.
- **Canlı arama:** Arama çubuğu üzerinden başlık ve içerikte 300 ms gecikmeyle anlık filtreleme yapılır.
- **Duyarlı (responsive) arayüz:** `Adw.OverlaySplitView` ve `Adw.Breakpoint` ile pencere daraldığında mobil/dar ekran görünümüne geçer (800px ve 600px sınırları).
- **Tema desteği:** GNOME sisteminin açık ve koyu tema tercihlerine otomatik uyum sağlar.
- **Klavye kısayolu:** `Ctrl+N` ile yeni not oluşturulabilir.
- **Yerel depolama:** Veriler `~/.local/share/com.example.Notes/notes.db` konumundaki SQLite veritabanında tutulur.

---

## Teknoloji Yığını

- **Dil:** Python 3
- **Arayüz:** GTK 4 (`gi.repository.Gtk`), libadwaita 1 (`gi.repository.Adw`)
- **Bağlayıcı:** PyGObject (`python3-gobject`)
- **Veritabanı:** SQLite 3 (Python standart kütüphanesi)
- **Paketleme:** Flatpak (`com.example.Notes.json`), RPM (`notes.spec`)

---

## Kurulum ve Çalıştırma

### 1. Doğrudan Çalıştırma

Fedora üzerinde bağımlılıkları kurup uygulamayı çalıştırın:

```bash
sudo dnf install python3 python3-gobject gtk4 libadwaita
python3 run.py
```

### 2. Flatpak ile Kurulum

`flatpak-builder` ile derleyip çalıştırmak için:

```bash
sudo dnf install flatpak flatpak-builder
flatpak install flathub org.gnome.Platform//46 org.gnome.Sdk//46
flatpak-builder --user --install --force-clean build-dir com.example.Notes.json
flatpak run com.example.Notes
```

### 3. RPM Paketi Oluşturma

Fedora üzerinde `.rpm` paketi derleyip kurmak için:

```bash
sudo dnf install rpmdevtools rpm-build
rpmdev-setuptree
tar --exclude='.git' -czvf notes-1.0.0.tar.gz app/ data/ run.py notes.spec
cp notes-1.0.0.tar.gz ~/rpmbuild/SOURCES/
rpmbuild -ba notes.spec
sudo dnf install ~/rpmbuild/RPMS/noarch/notes-1.0.0-1.fc*.noarch.rpm
notes
```

---

## Kullanım

- **Yeni not:** Üst çubuktaki `+` butonuna tıklayın veya `Ctrl+N` kısayolunu kullanın.
- **Klasör işlemleri:** Sol paneldeki `+` butonu ile yeni klasör oluşturabilir, klasör seçeneklerinden yeniden adlandırma veya silme yapabilirsiniz.
- **Not taşıma:** Nota sağ tıklayıp "Klasör Değiştir" alt menüsünden hedef klasörü seçin.
- **Arama:** Not listesinin üzerindeki arama alanına metin girerek filtreleme yapın.
- **Kaydetme:** Metin düzenlendikten sonra otomatik kaydedilir; ayrı bir kaydet butonu bulunmaz.

---

## Proje Yapısı

```text
.
├── app/                           # Uygulama kaynak kodları
│   ├── __init__.py                # Paket başlatıcı
│   ├── db.py                      # SQLite veritabanı şeması ve CRUD sorguları
│   ├── main.py                    # Adw.Application giriş noktası ve yaşam döngüsü
│   └── ui/                        # Kullanıcı arayüzü bileşenleri
│       ├── editor.py              # Not başlığı, metin düzenleyici ve butonlar
│       ├── note_list.py           # Not listesi, arama ve sağ tık bağlam menüsü
│       ├── sidebar.py             # Klasör listesi ve klasör yönetimi
│       └── window.py              # Adw.ApplicationWindow ve 3 panelli split-view düzeni
├── data/                          # Masaüstü entegrasyonu dosyaları
│   ├── com.example.Notes.desktop  # Masaüstü başlatıcı dosyası
│   └── com.example.Notes.svg      # Uygulama vektör ikonu
├── icons/                         # Hicolor uygulama ikonları
├── tests/                         # Birim ve entegrasyon testleri
│   ├── test_db.py                 # Veritabanı testleri
│   └── test_folder_note_flow.py   # Klasör ve otomatik kaydetme akış testleri
├── com.example.Notes.json         # Flatpak manifest dosyası
├── notes.spec                     # Fedora RPM spec dosyası
├── requirements.txt               # Bağımlılık listesi
├── run.py                         # Uygulama başlatıcı betik
├── LICENSE                        # GPLv3 lisans metni
└── README.md                      # Proje dokümantasyonu
```

---

## Testler

Testleri çalıştırmak için:

```bash
python3 -m unittest discover tests
```

---

## Katkıda Bulunma

1. Depoyu forklayın.
2. Yeni bir dal açın (`git checkout -b feature/yeni-ozellik`).
3. Değişikliklerinizi commit edin (`git commit -m 'Feat: Yeni özellik'`).
4. Dalı uzak depoya gönderin (`git push origin feature/yeni-ozellik`).
5. Pull Request açın.

---

## Lisans

Bu proje GNU General Public License v3.0 (GPLv3) ile lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakabilirsiniz.
