# Web Scraper Koleksiyonu 🕷️

Bu proje, çeşitli Türk gıda şirketlerinin web sitelerinden ürün görsellerini otomatik olarak indiren Python script'lerini içerir.

## 📊 **Toplam İstatistikler**
- ✅ **3 aktif scraper**
- 📸 **515+ görsel** başarıyla indirildi
- 🗂️ **Kategorili organizasyon**
- 🚀 **Selenium & BeautifulSoup teknolojileri**

## Mevcut Scraperlar

### 1. Teksüt Ürün Görselleri Scraper
Teksüt'ün ürünler sayfasından (https://teksut.com.tr/urunler/) tüm ürün görsellerini otomatik olarak indirir.

### 2. Kahve Dünyası Scraper  
Kahve Dünyası'nın web sitesinden (https://www.kahvedunyasi.com/) ürün görsellerini kategorilere ayırarak indirir.

### 3. TAT Ürün Görselleri Scraper ⭐ **386 görsel indirildi!**
TAT'ın web sitesinden (https://www.tat.com.tr/) tüm ürün kategorilerindeki görselleri indirir.

## Özellikler

- ✅ Teksüt ürünler sayfasındaki tüm görselleri otomatik indirir
- ✅ Görselleri kategorilere göre organize eder
- ✅ Dosya adlarını korur ve duplikasyon önler
- ✅ User-Agent ile güvenli web scraping
- ✅ Hata yönetimi ve ilerleme takibi

## İndirilen Görsel Kategorileri

- 🧀 **Süzme Peynirler** - 6 çeşit
- 🧀 **Kültürlü Peynirler** - 10 çeşit  
- 🧀 **Klasik Peynirler** - 5 çeşit
- 🧀 **Tost Peynirler** - 9 çeşit
- 🧀 **Kaşar Peynirler** - 7 çeşit
- 🧀 **Sürülebilir Peynirler** - 18 çeşit
- 🧀 **Yöresel Peynirler** - 12 çeşit
- 🧈 **Kaymak & Tereyağı & Krema** - 10 çeşit
- 🥛 **UHT Sütler** - 5 çeşit
- 🥛 **UHT Küçük Sütler** - 10 çeşit
- 🥛 **Bag in Box Sütler** - 5 çeşit
- 🥤 **Ayranlar** - 8 çeşit
- 🍶 **Yoğurtlar** - 11 çeşit
- 🧀 **Açık Şarküteri Ürünleri** - 8 çeşit
- 🏭 **Endüstriyel Ürünler** - 6 çeşit

**Toplam: 129 adet ürün görseli başarıyla indirildi**

---

## 🍅 TAT Ürün Görselleri Scraper

TAT'ın resmi web sitesinden tüm ürün kategorilerindeki görselleri otomatik olarak indirir.

### Özellikler
- 🎯 **Dinamik Menü Desteği** - Selenium ile hover menüleri handle eder
- 📁 **Kategori Organizasyonu** - Ürünleri kategorilere göre düzenler
- 🖼️ **Akıllı Görsel Filtreleme** - Logo, ikon gibi gereksiz görselleri filtreler
- 🔄 **Fallback Mekanizması** - Selenium çalışmazsa manuel URL'lerle devam eder

### TAT Ürün Kategorileri ✅ **İndirme Tamamlandı**
- 🥫 **Salça** - 66 adet görsel
- 🍅 **Domates Ürünleri** - 63 adet görsel
- 🥫 **Soslar** - 63 adet görsel (Ketçap, Mayonez, Barbekü)
- 🍲 **Çorba** - 66 adet görsel
- 🥒 **Sebze Konservesi** - 63 adet görsel (Fasulye, Bezelye, Bamya)
- 🍚 **Hazır Yemek** - 65 adet görsel (Pilav, Fasulye)

**Toplam: 386 adet TAT ürün görseli başarıyla indirildi!** 🎉

Diğer kategoriler (Organik, Haşlanmış, Meze, Turşu, Reçel) için de klasörler oluşturuldu ve gelecek güncellemeler için hazır.

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

## Gereksinimler

- Python 3.6+
- requests
- beautifulsoup4
- lxml
- selenium (TAT scraper için)
- ChromeDriver (TAT scraper için)

## Dosya Yapısı

```
scra-teksüt/
├── teksut_image_scraper.py    # Teksüt scraper script'i
├── kahvedunyasi_scraper.py    # Kahve Dünyası scraper script'i
├── tat_scraper.py             # TAT scraper script'i (YENİ)
├── requirements.txt           # Python bağımlılıkları
├── teksut_images/            # Teksüt görselleri (129 adet)
├── kahvedunyasi_images/      # Kahve Dünyası görselleri (kategorili)
├── tat_images/               # TAT görselleri (386 adet, kategorili) ✅
└── README.md                 # Bu dosya
```

## Önemli Notlar

- Script etik web scraping prensiplerine uyar
- İstekler arası 0.5 saniye bekleme süresi
- User-Agent header'ı kullanır
- Hata durumlarında güvenli şekilde devam eder
- Mevcut dosyaları kontrol eder ve duplikasyon önler

## Lisans

Bu proje eğitim amaçlıdır. Tüm şirketlerin (Teksüt, Kahve Dünyası, TAT) telif haklarına saygı gösterilmelidir.

## Katkıda Bulunma

Yeni scraper eklemek veya mevcut scraperları geliştirmek için pull request açabilirsiniz.