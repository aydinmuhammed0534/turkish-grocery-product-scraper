# Teksüt Ürün Görselleri Scraper

Bu proje, Teksüt'ün ürünler sayfasından (https://teksut.com.tr/urunler/) tüm ürün görsellerini otomatik olarak indiren bir Python script'idir.

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

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

```bash
python teksut_image_scraper.py
```

Script çalıştırıldığında:
1. Teksüt ürünler sayfasına bağlanır
2. Tüm görsel URL'lerini bulur
3. Görselleri `teksut_images/` klasörüne indirir
4. İlerleme durumunu gösterir

## Gereksinimler

- Python 3.6+
- requests
- beautifulsoup4
- lxml

## Dosya Yapısı

```
teksut-scraper/
├── teksut_image_scraper.py    # Ana scraper script'i
├── requirements.txt           # Python bağımlılıkları
├── teksut_images/            # İndirilen görseller (129 adet)
└── README.md                 # Bu dosya
```

## Önemli Notlar

- Script etik web scraping prensiplerine uyar
- İstekler arası 0.5 saniye bekleme süresi
- User-Agent header'ı kullanır
- Hata durumlarında güvenli şekilde devam eder
- Mevcut dosyaları kontrol eder ve duplikasyon önler

## Lisans

Bu proje eğitim amaçlıdır. Teksüt'ün telif haklarına saygı gösterilmelidir.