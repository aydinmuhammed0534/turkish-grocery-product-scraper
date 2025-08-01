# Web Scraper Koleksiyonu

Bu proje, çeşitli Türk gıda şirketlerinin web sitelerinden ürün görsellerini otomatik olarak indiren Python script'lerini içerir.

## Toplam İstatistikler
- **5 aktif scraper**
- **626+ görsel** başarıyla indirildi
- **Kategorili organizasyon**
- **Selenium & BeautifulSoup teknolojileri**

## Mevcut Scraperlar

### 1. Teksüt Ürün Görselleri Scraper
Teksüt'ün ürünler sayfasından (https://teksut.com.tr/urunler/) tüm ürün görsellerini otomatik olarak indirir.

### 2. Kahve Dünyası Scraper  
Kahve Dünyası'nın web sitesinden (https://www.kahvedunyasi.com/) ürün görsellerini kategorilere ayırarak indirir.

### 3. TAT Ürün Görselleri Scraper **386 görsel indirildi**
TAT'ın web sitesinden (https://www.tat.com.tr/) tüm ürün kategorilerindeki görselleri indirir.

### 4. Mutlu Makarna Scraper **48 görsel indirildi**
Mutlu Makarna'nın web sitesinden (https://www.mutlumakarna.com.tr/) tüm makarna ürün görsellerini indirir.

### 5. Kinder Scraper **63 görsel indirildi**
Kinder'ın web sitesinden (https://www.kinder.com/tr/tr/) tüm çikolata ürün görsellerini indirir.

## Özellikler

- Tüm ürün görsellerini otomatik indirir
- Görselleri kategorilere göre organize eder
- Dosya adlarını korur ve duplikasyon önler
- User-Agent ile güvenli web scraping
- Hata yönetimi ve ilerleme takibi
- Selenium desteği ile dinamik içerik scraping

## İndirilen Görsel Kategorileri

### Teksüt Ürünleri (129 adet)
- **Süzme Peynirler** - 6 çeşit
- **Kültürlü Peynirler** - 10 çeşit  
- **Klasik Peynirler** - 5 çeşit
- **Tost Peynirler** - 9 çeşit
- **Kaşar Peynirler** - 7 çeşit
- **Sürülebilir Peynirler** - 18 çeşit
- **Yöresel Peynirler** - 12 çeşit
- **Kaymak & Tereyağı & Krema** - 10 çeşit
- **UHT Sütler** - 5 çeşit
- **UHT Küçük Sütler** - 10 çeşit
- **Bag in Box Sütler** - 5 çeşit
- **Ayranlar** - 8 çeşit
- **Yoğurtlar** - 11 çeşit
- **Açık Şarküteri Ürünleri** - 8 çeşit
- **Endüstriyel Ürünler** - 6 çeşit

### Mutlu Makarna Ürünleri (48 adet)
- **Klasik Ürünler** - 26 adet
- **Kısa Kesmeler** - 7 adet (Penne, Burgu, Kelebek, Midye, Boncuk, Fiyonk, Yüksük)
- **Uzun Kesmeler** - 4 adet (Spagetti, İnce Uzun, Orta Uzun)
- **Çorbalık** - 3 adet (Tel Şehriye, Arpa Şehriye, Yıldız Şehriye)
- **Sebzeli** - 2 adet
- **Tam Buğday** - 2 adet
- **Couscous** - 2 adet
- **İrmik** - 1 adet
- **Mac & Cheese** - 1 adet

### Kinder Ürünleri (63 adet)
- **Kinder Joy** - 10 adet (En popüler)
- **Genel** - 27 adet (Ana sayfa ve ortak görseller)
- **Kinder Pingui** - 6 adet
- **Kinder Surprise** - 5 adet
- **Kinder Chocolate** - 4 adet
- **Kinder Bueno** - 3 adet
- **Kinder Bueno White** - 3 adet
- **Kinder Delice** - 3 adet
- **Kinder Süt Dilimi** - 2 adet

---

## TAT Ürün Görselleri Scraper

TAT'ın resmi web sitesinden tüm ürün kategorilerindeki görselleri otomatik olarak indirir.

### Özellikler
- **Dinamik Menü Desteği** - Selenium ile hover menüleri handle eder
- **Kategori Organizasyonu** - Ürünleri kategorilere göre düzenler
- **Akıllı Görsel Filtreleme** - Logo, ikon gibi gereksiz görselleri filtreler
- **Fallback Mekanizması** - Selenium çalışmazsa manuel URL'lerle devam eder

### TAT Ürün Kategorileri (386 adet)
- **Salça** - 66 adet görsel
- **Domates Ürünleri** - 63 adet görsel
- **Soslar** - 63 adet görsel (Ketçap, Mayonez, Barbekü)
- **Çorba** - 66 adet görsel
- **Sebze Konservesi** - 63 adet görsel (Fasulye, Bezelye, Bamya)
- **Hazır Yemek** - 65 adet görsel (Pilav, Fasulye)

Diğer kategoriler (Organik, Haşlanmış, Meze, Turşu, Reçel) için de klasörler oluşturuldu ve gelecek güncellemeler için hazır.

---

## Mutlu Makarna Scraper

Mutlu Makarna'nın resmi web sitesinden tüm makarna ürün görsellerini kategorilere göre indirir.

### Özellikler
- **Makarna Kategorileri Tanıma** - Ürünleri şekil ve tipine göre otomatik kategorize eder
- **Hibrit Scraping** - Selenium ve BeautifulSoup teknolojilerini birlikte kullanır
- **Görsel Kalite Kontrolü** - Sadece ürün görsellerini filtreler
- **Hata Toleransı** - 404 hataları ve eksik görselleri atlayarak devam eder

### Mutlu Makarna Kategorileri (48 adet)
- **Klasik Ürünler** - 26 adet (Mantı, Eriştə, Charleston vb.)
- **Kısa Kesmeler** - 7 adet (Penne, Burgu, Kelebek, Midye, Boncuk)
- **Uzun Kesmeler** - 4 adet (Spagetti, İnce Uzun, Orta Uzun)
- **Çorbalık** - 3 adet (Tel Şehriye, Arpa Şehriye, Yıldız Şehriye)
- **Sebzeli Makarnalar** - 2 adet
- **Tam Buğday** - 2 adet
- **Couscous** - 2 adet
- **İrmik** - 1 adet
- **Mac & Cheese** - 1 adet

### Kurulum

```bash
# Gerekli kütüphaneleri yükle
pip install -r requirements.txt

# ChromeDriver'ı yükle (macOS için)
brew install chromedriver

# ChromeDriver'ı yükle (Ubuntu/Debian için)
sudo apt-get install chromium-chromedriver

# ChromeDriver'ı yükle (Windows için)
# https://chromedriver.chromium.org/ adresinden indirip PATH'e ekleyin
```

### Kullanım

```bash
python tat_scraper.py
```

Script çalıştırıldığında:
1. TAT ana sayfasına gider
2. "tat Ürünleri" menüsüne hover yapar
3. Tüm kategori linklerini toplar
4. Her kategorideki ürün görsellerini bulur
5. Görselleri `tat_images/` klasörüne kategorilere ayırarak indirir
6. İlerleme durumunu gösterir

---

## Genel Kurulum

```bash
pip install -r requirements.txt
```

## Genel Kullanım

### Teksüt Scraper
```bash
python teksut_image_scraper.py
```

### Kahve Dünyası Scraper
```bash
python kahvedunyasi_scraper.py
```

### TAT Scraper
```bash
python tat_scraper.py
```

### Mutlu Makarna Scraper
```bash
python mutlu_makarna_scraper.py
```

### Kinder Scraper
```bash
python kinder_scraper.py
```

## Gereksinimler

- Python 3.6+
- requests
- beautifulsoup4
- lxml
- selenium (TAT ve Mutlu Makarna scraper'ları için)
- ChromeDriver (TAT ve Mutlu Makarna scraper'ları için)

## Dosya Yapısı

```
scra-teksüt/
├── teksut_image_scraper.py    # Teksüt scraper script'i (129 görsel)
├── kahvedunyasi_scraper.py    # Kahve Dünyası scraper script'i
├── tat_scraper.py             # TAT scraper script'i (386 görsel)
├── mutlu_makarna_scraper.py   # Mutlu Makarna scraper script'i (48 görsel)
├── kinder_scraper.py          # Kinder scraper script'i (63 görsel)
├── requirements.txt           # Python bağımlılıkları
├── teksut_images/            # Teksüt görselleri (129 adet)
├── kahvedunyasi_images/      # Kahve Dünyası görselleri (kategorili)
├── tat_images/               # TAT görselleri (386 adet, kategorili)
├── mutlu_makarna_images/     # Mutlu Makarna görselleri (48 adet, kategorili)
├── kinder_images/            # Kinder görselleri (63 adet, kategorili)
├── .gitignore                # Git ignore dosyası
└── README.md                 # Bu dosya
```

## Önemli Notlar

- Script etik web scraping prensiplerine uyar
- İstekler arası 0.5 saniye bekleme süresi
- User-Agent header'ı kullanır
- Hata durumlarında güvenli şekilde devam eder
- Mevcut dosyaları kontrol eder ve duplikasyon önler

## Lisans

Bu proje eğitim amaçlıdır. Tüm şirketlerin (Teksüt, Kahve Dünyası, TAT, Mutlu Makarna, Kinder) telif haklarına saygı gösterilmelidir.

## Katkıda Bulunma

Yeni scraper eklemek veya mevcut scraperları geliştirmek için pull request açabilirsiniz.