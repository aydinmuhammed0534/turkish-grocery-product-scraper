#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mutlu Makarna Ürün Görselleri Çekici
Bu script Mutlu Makarna'nın web sitesindeki tüm ürün görsellerini kategorilere göre indirir.
"""

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import time
from pathlib import Path
import mimetypes
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class MutluMakarnaScraper:
    def __init__(self, base_url="https://www.mutlumakarna.com.tr/tr"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        })
        
        # Çıktı dizini oluştur
        self.output_dir = Path("mutlu_makarna_images")
        self.output_dir.mkdir(exist_ok=True)
        
        # Mutlu Makarna ürün kategorileri
        self.categories = {
            'klasik_urunler': 'Klasik Ürünler',
            'sebzeli': 'Sebzeli Makarnalar',
            'tam_bugday': 'Tam Buğday',
            'couscous': 'Couscous',
            'irmik': 'İrmik',
            'mac_cheese': 'Mac & Cheese',
            'kisa_kesmeler': 'Kısa Kesmeler',
            'uzun_kesmeler': 'Uzun Kesmeler',
            'corbalik': 'Çorbalık',
            'genel': 'Genel'
        }
        
        # Kategori dizinleri oluştur
        for category_key in self.categories.keys():
            category_dir = self.output_dir / category_key
            category_dir.mkdir(exist_ok=True)
        
    def setup_driver(self):
        """Chrome WebDriver'ı kurar"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
        
        try:
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            print(f"Chrome WebDriver kurulamadı: {e}")
            print("Lütfen ChromeDriver'ın yüklü olduğundan emin olun.")
            return None
    
    def get_product_urls(self, driver):
        """Ürün sayfalarının URL'lerini toplar"""
        product_urls = {}
        
        try:
            print("Ana sayfa yükleniyor...")
            driver.get(self.base_url)
            time.sleep(3)
            
            # Ürün linklerini bul
            product_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/urun') or contains(@href, '/product')]")
            
            for link in product_links:
                try:
                    href = link.get_attribute('href')
                    text = link.text.strip()
                    
                    if href and text and len(text) > 2:
                        # Ürün adını normalleştir
                        product_key = self.normalize_product_name(text)
                        if product_key:
                            product_urls[product_key] = {
                                'url': href,
                                'name': text
                            }
                            print(f"Ürün bulundu: {text} -> {href}")
                except Exception as e:
                    continue
            
            # Ana sayfadaki ürün görsellerini de kontrol et
            print("Ana sayfa ürün görselleri aranıyor...")
            img_elements = driver.find_elements(By.TAG_NAME, "img")
            
            for img in img_elements:
                try:
                    src = img.get_attribute('src')
                    alt = img.get_attribute('alt') or ''
                    
                    if src and self.is_valid_product_image(src, alt):
                        product_key = self.categorize_product(src, alt)
                        if product_key not in product_urls:
                            product_urls[f"homepage_{len(product_urls)}"] = {
                                'url': self.base_url,
                                'name': f"Ana Sayfa Ürünü",
                                'image_url': src,
                                'category': product_key
                            }
                            print(f"Ana sayfa ürün görseli bulundu: {src}")
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Ürün URL'leri alınırken hata: {e}")
        
        return product_urls
    
    def normalize_product_name(self, product_name):
        """Ürün adını normalleştirir"""
        product_lower = product_name.lower()
        
        # Makarna türü eşleştirmeleri
        makarna_types = [
            'spagetti', 'spaghetti', 'firin', 'burgu', 'ince', 'fiyonk', 
            'yuksuk', 'yüksük', 'orta', 'penne', 'kelebek', 'midye', 
            'boncuk', 'manti', 'eriste', 'eriştə', 'carliston', 'charleston',
            'tel', 'arpa', 'sehriye', 'şehriye', 'kuskus', 'couscous',
            'yildiz', 'yıldız', 'makarna', 'pasta'
        ]
        
        if any(makarna_type in product_lower for makarna_type in makarna_types):
            return re.sub(r'[^a-zA-Z0-9_]', '_', product_lower.replace(' ', '_'))
        
        return None
    
    def categorize_product(self, url, alt=""):
        """Ürünü kategoriye göre sınıflandırır"""
        url_lower = url.lower()
        alt_lower = alt.lower()
        
        # Kategori eşleştirmeleri
        if any(word in url_lower or word in alt_lower for word in ['sebzeli', 'sebze']):
            return 'sebzeli'
        elif any(word in url_lower or word in alt_lower for word in ['tam', 'bugday', 'buğday', 'kepek']):
            return 'tam_bugday'
        elif any(word in url_lower or word in alt_lower for word in ['couscous', 'kuskus']):
            return 'couscous'
        elif any(word in url_lower or word in alt_lower for word in ['irmik']):
            return 'irmik'
        elif any(word in url_lower or word in alt_lower for word in ['mac', 'cheese']):
            return 'mac_cheese'
        elif any(word in url_lower or word in alt_lower for word in ['tel', 'arpa', 'yildiz', 'yıldız', 'sehriye', 'şehriye']):
            return 'corbalik'
        elif any(word in url_lower or word in alt_lower for word in ['spagetti', 'spaghetti', 'ince', 'uzun', 'orta']):
            return 'uzun_kesmeler'
        elif any(word in url_lower or word in alt_lower for word in ['penne', 'burgu', 'kelebek', 'midye', 'boncuk', 'fiyonk', 'yuksuk', 'yüksük']):
            return 'kisa_kesmeler'
        else:
            return 'klasik_urunler'
    
    def get_page_content(self, url):
        """Sayfanın HTML içeriğini alır"""
        try:
            print(f"Sayfa içeriği alınıyor: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            print(f"Sayfa alınırken hata oluştu: {e}")
            return None
    
    def extract_product_images(self, html_content, category_key):
        """HTML içeriğinden ürün görsellerini çıkarır"""
        soup = BeautifulSoup(html_content, 'html.parser')
        image_data = []
        
        # Ürün görsel konteynerlerini bul
        product_containers = soup.find_all(['div', 'article', 'section'], 
                                         class_=lambda x: x and any(word in x.lower() for word in 
                                         ['product', 'urun', 'item', 'card', 'makarna']))
        
        print(f"Ürün konteyneri bulundu: {len(product_containers)}")
        
        # Tüm img etiketlerini kontrol et
        all_images = soup.find_all('img')
        print(f"Toplam img etiketi: {len(all_images)}")
        
        for img in all_images:
            # src özelliğini kontrol et
            src = img.get('src')
            alt = img.get('alt', '')
            
            if src and self.is_valid_product_image(src, alt):
                full_url = urljoin(self.base_url, src)
                detected_category = self.categorize_product(full_url, alt)
                
                image_data.append({
                    'url': full_url,
                    'alt': alt,
                    'category': detected_category or category_key
                })
                print(f"Ürün görseli bulundu: {full_url}")
            
            # data-src özelliğini kontrol et (lazy loading)
            data_src = img.get('data-src')
            if data_src and self.is_valid_product_image(data_src, alt):
                full_url = urljoin(self.base_url, data_src)
                detected_category = self.categorize_product(full_url, alt)
                
                image_data.append({
                    'url': full_url,
                    'alt': alt,
                    'category': detected_category or category_key
                })
                print(f"Lazy load ürün görseli bulundu: {full_url}")
        
        # CSS background-image özelliklerini bul
        style_elements = soup.find_all(attrs={"style": True})
        for element in style_elements:
            style = element.get('style', '')
            if 'background-image' in style:
                urls = re.findall(r'url\(["\']?([^"\']*)["\']?\)', style)
                for url in urls:
                    if self.is_valid_product_image(url):
                        full_url = urljoin(self.base_url, url)
                        detected_category = self.categorize_product(full_url)
                        
                        image_data.append({
                            'url': full_url,
                            'alt': '',
                            'category': detected_category or category_key
                        })
                        print(f"CSS background ürün görseli bulundu: {full_url}")
        
        return image_data
    
    def is_valid_product_image(self, url, alt=""):
        """URL'nin geçerli bir ürün görseli olup olmadığını kontrol eder"""
        if not url or url.startswith('data:'):
            return False
        
        # Gereksiz URL'leri filtrele
        exclude_patterns = ['icon', 'logo', 'placeholder', 'loading', 'spinner', 'banner', 'slider', 'header', 'footer']
        url_lower = url.lower()
        alt_lower = alt.lower()
        
        # Exclude patterns kontrolü
        if any(pattern in url_lower for pattern in exclude_patterns):
            return False
        
        # Mutlu Makarna ürünü görseli olabilecek pattern'lar
        product_patterns = ['urun', 'product', 'makarna', 'pasta', 'spagetti', 'penne', 'burgu', 'jpg', 'jpeg', 'png', 'webp']
        
        # Görsel uzantılarını kontrol et
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        
        has_valid_extension = any(path.endswith(ext) for ext in valid_extensions)
        has_product_pattern = any(pattern in url_lower or pattern in alt_lower for pattern in product_patterns)
        
        return has_valid_extension or has_product_pattern
    
    def get_filename_from_url(self, url, category):
        """URL'den dosya adı çıkarır"""
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # Eğer dosya adı yoksa veya uzantısı yoksa, URL'den oluştur
        if not filename or '.' not in filename:
            filename = f"{category}_product_{hash(url) % 10000}.jpg"
        
        return filename
    
    def download_image(self, image_data):
        """Tek bir görseli indirir"""
        url = image_data['url']
        category = image_data['category']
        filename = self.get_filename_from_url(url, category)
        
        try:
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # İçerik türünü kontrol et
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print(f"Bu URL bir görsel değil: {url} (Content-Type: {content_type})")
                return False
            
            # Dosya uzantısını content-type'a göre ayarla
            if not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']):
                ext = mimetypes.guess_extension(content_type.split(';')[0])
                if ext:
                    filename += ext
            
            # Kategori dizinine kaydet
            category_dir = self.output_dir / category
            file_path = category_dir / filename
            
            # Eğer dosya zaten varsa, sayı ekle
            counter = 1
            original_path = file_path
            while file_path.exists():
                stem = original_path.stem
                suffix = original_path.suffix
                file_path = category_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Dosyayı kaydet
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"İndirildi ({category}): {file_path.name}")
            return True
            
        except requests.RequestException as e:
            print(f"İndirme hatası {url}: {e}")
            return False
        except Exception as e:
            print(f"Dosya kaydetme hatası {filename}: {e}")
            return False
    
    def scrape_with_requests(self):
        """Requests ile scraping yapar"""
        print("Requests ile ana sayfa scraping...")
        
        # Ana sayfa içeriğini al
        html_content = self.get_page_content(self.base_url)
        if not html_content:
            print("Ana sayfa içeriği alınamadı!")
            return 0
        
        # Ürün görsellerini çıkar
        image_data = self.extract_product_images(html_content, 'genel')
        
        if not image_data:
            print("Hiç ürün görseli bulunamadı!")
            return 0
        
        print(f"Toplam {len(image_data)} ürün görseli bulundu")
        
        # Görselleri indir
        successful_downloads = 0
        for i, data in enumerate(image_data, 1):
            print(f"[{i}/{len(image_data)}] İndiriliyor: {data['url']}")
            
            if self.download_image(data):
                successful_downloads += 1
            
            # İstekler arasında kısa bekleme
            time.sleep(0.5)
        
        return successful_downloads
    
    def scrape_all_products(self):
        """Tüm ürünleri scrape eder"""
        print("Mutlu Makarna Ürün Görselleri Çekici Başlatıldı")
        print("=" * 60)
        
        # WebDriver'ı kur
        driver = self.setup_driver()
        if not driver:
            print("WebDriver kurulamadı, requests ile devam ediliyor...")
            total_downloads = self.scrape_with_requests()
        else:
            try:
                # Ürün URL'lerini al
                product_urls = self.get_product_urls(driver)
                
                if not product_urls:
                    print("Hiç ürün URL'si bulunamadı, requests ile devam ediliyor...")
                    total_downloads = self.scrape_with_requests()
                else:
                    print(f"\nToplam {len(product_urls)} ürün bulundu:")
                    for key, info in product_urls.items():
                        print(f"  - {info['name']}: {info['url']}")
                    
                    # Ana sayfayı scrape et
                    total_downloads = self.scrape_with_requests()
                    
                    # Her ürün sayfasını scrape et
                    for product_key, product_info in product_urls.items():
                        if 'image_url' not in product_info:  # Ana sayfa görsellerini tekrar scrape etme
                            print(f"\nÜrün scraping: {product_info['name']}")
                            html_content = self.get_page_content(product_info['url'])
                            if html_content:
                                category = self.categorize_product(product_info['url'], product_info['name'])
                                image_data = self.extract_product_images(html_content, category)
                                
                                for data in image_data:
                                    if self.download_image(data):
                                        total_downloads += 1
                                    time.sleep(0.5)
                            
                            time.sleep(2)  # Sayfalar arası bekleme
            
            finally:
                driver.quit()
        
        print("\n" + "=" * 60)
        print(f"Tüm işlemler tamamlandı!")
        print(f"Toplam başarılı indirme: {total_downloads}")
        print(f"Görseller '{self.output_dir}' klasörüne kategorilere göre ayrılarak kaydedildi")
        
        # Kategori özetini göster
        print("\nKategori özetleri:")
        for category_key, category_name in self.categories.items():
            category_dir = self.output_dir / category_key
            if category_dir.exists():
                file_count = len(list(category_dir.glob('*')))
                if file_count > 0:
                    print(f"  - {category_name}: {file_count} dosya")

def main():
    """Ana fonksiyon"""
    scraper = MutluMakarnaScraper()
    scraper.scrape_all_products()

if __name__ == "__main__":
    main()