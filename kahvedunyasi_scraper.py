#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kahve Dünyası Ürün Görselleri Çekici
Bu script Kahve Dünyası'nın ana sayfasındaki tüm ürün görsellerini indirir.
"""

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import time
from pathlib import Path
import mimetypes
import json

class KahveDunyasiScraper:
    def __init__(self, base_url="https://www.kahvedunyasi.com/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Çıktı dizini oluştur
        self.output_dir = Path("kahvedunyasi_images")
        self.output_dir.mkdir(exist_ok=True)
        
        # Kategori dizinleri oluştur
        self.categories = {
            'kahve': self.output_dir / 'kahve',
            'cikolata': self.output_dir / 'cikolata',
            'aksesuar': self.output_dir / 'aksesuar',
            'dondurma': self.output_dir / 'dondurma',
            'pastacilik': self.output_dir / 'pastacilik',
            'hediye': self.output_dir / 'hediye_kutulari',
            'genel': self.output_dir / 'genel'
        }
        
        for category_dir in self.categories.values():
            category_dir.mkdir(exist_ok=True)
        
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
    
    def categorize_image(self, img_url, img_alt=""):
        """Görseli kategoriye göre sınıflandırır"""
        img_url_lower = img_url.lower()
        img_alt_lower = img_alt.lower()
        
        # Kategori kelimelerine göre sınıflandır
        if any(word in img_url_lower or word in img_alt_lower for word in ['kahve', 'coffee', 'espresso', 'latte', 'cappuccino', 'türk']):
            return 'kahve'
        elif any(word in img_url_lower or word in img_alt_lower for word in ['çikolata', 'chocolate', 'choco', 'kakao']):
            return 'cikolata'
        elif any(word in img_url_lower or word in img_alt_lower for word in ['aksesuar', 'mug', 'bardak', 'fincan', 'grinder']):
            return 'aksesuar'
        elif any(word in img_url_lower or word in img_alt_lower for word in ['dondurma', 'ice', 'cream']):
            return 'dondurma'
        elif any(word in img_url_lower or word in img_alt_lower for word in ['pasta', 'cake', 'tart', 'kurabiye']):
            return 'pastacilik'
        elif any(word in img_url_lower or word in img_alt_lower for word in ['hediye', 'gift', 'kutu', 'box']):
            return 'hediye'
        else:
            return 'genel'
    
    def extract_image_urls(self, html_content):
        """HTML içeriğinden görsel URL'lerini çıkarır"""
        soup = BeautifulSoup(html_content, 'html.parser')
        image_data = []
        
        # Ürün görsellerini bul
        product_images = soup.find_all('img', class_=lambda x: x and ('product' in x.lower() or 'image' in x.lower()))
        print(f"Ürün görselleri bulundu: {len(product_images)}")
        
        # Tüm img etiketlerini kontrol et
        all_images = soup.find_all('img')
        print(f"Toplam img etiketi: {len(all_images)}")
        
        for img in all_images:
            # src özelliğini kontrol et
            src = img.get('src')
            alt = img.get('alt', '')
            
            if src and self.is_valid_image_url(src):
                full_url = urljoin(self.base_url, src)
                category = self.categorize_image(full_url, alt)
                image_data.append({
                    'url': full_url,
                    'alt': alt,
                    'category': category
                })
                print(f"Görsel URL bulundu ({category}): {full_url}")
            
            # data-src özelliğini kontrol et (lazy loading)
            data_src = img.get('data-src')
            if data_src and self.is_valid_image_url(data_src):
                full_url = urljoin(self.base_url, data_src)
                category = self.categorize_image(full_url, alt)
                image_data.append({
                    'url': full_url,
                    'alt': alt,
                    'category': category
                })
                print(f"Lazy load görsel URL bulundu ({category}): {full_url}")
        
        # CSS background-image özelliklerini bul
        style_elements = soup.find_all(attrs={"style": True})
        for element in style_elements:
            style = element.get('style', '')
            if 'background-image' in style:
                import re
                urls = re.findall(r'url\(["\']?([^"\']*)["\']?\)', style)
                for url in urls:
                    if self.is_valid_image_url(url):
                        full_url = urljoin(self.base_url, url)
                        category = self.categorize_image(full_url)
                        image_data.append({
                            'url': full_url,
                            'alt': '',
                            'category': category
                        })
                        print(f"CSS background görsel bulundu ({category}): {full_url}")
        
        return image_data
    
    def is_valid_image_url(self, url):
        """URL'nin geçerli bir görsel URL'si olup olmadığını kontrol eder"""
        if not url or url.startswith('data:'):
            return False
        
        # Gereksiz URL'leri filtrele
        exclude_patterns = ['icon', 'logo', 'placeholder', 'loading', 'spinner']
        url_lower = url.lower()
        
        if any(pattern in url_lower for pattern in exclude_patterns):
            return False
        
        # Görsel uzantılarını kontrol et
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        
        return any(path.endswith(ext) for ext in valid_extensions) or 'image' in url_lower
    
    def get_filename_from_url(self, url, category):
        """URL'den dosya adı çıkarır"""
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # Eğer dosya adı yoksa veya uzantısı yoksa, URL'den oluştur
        if not filename or '.' not in filename:
            filename = f"{category}_image_{hash(url) % 10000}.jpg"
        
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
            category_dir = self.categories.get(category, self.categories['genel'])
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
            
            print(f"✓ İndirildi ({category}): {file_path.name}")
            return True
            
        except requests.RequestException as e:
            print(f"✗ İndirme hatası {url}: {e}")
            return False
        except Exception as e:
            print(f"✗ Dosya kaydetme hatası {filename}: {e}")
            return False
    
    def scrape_images(self):
        """Ana scraping fonksiyonu"""
        print("Kahve Dünyası Görsel Çekici Başlatıldı")
        print("=" * 50)
        
        # Ana sayfa içeriğini al
        html_content = self.get_page_content(self.base_url)
        if not html_content:
            print("Ana sayfa içeriği alınamadı!")
            return
        
        # Görsel URL'lerini çıkar
        print("\nGörsel URL'leri çıkarılıyor...")
        image_data = self.extract_image_urls(html_content)
        
        if not image_data:
            print("Hiç görsel URL'si bulunamadı!")
            return
        
        # Kategorilere göre grupla
        category_counts = {}
        for data in image_data:
            category = data['category']
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print(f"\nToplam {len(image_data)} görsel URL'si bulundu")
        print("Kategori dağılımı:")
        for category, count in category_counts.items():
            print(f"  - {category}: {count} adet")
        
        print("\nİndirme işlemi başlatılıyor...\n")
        
        # Görselleri indir
        successful_downloads = 0
        for i, data in enumerate(image_data, 1):
            print(f"[{i}/{len(image_data)}] İndiriliyor: {data['url']}")
            
            if self.download_image(data):
                successful_downloads += 1
            
            # İstekler arasında kısa bekleme
            time.sleep(0.5)
        
        print("\n" + "=" * 50)
        print(f"İşlem tamamlandı!")
        print(f"Başarılı indirme: {successful_downloads}/{len(image_data)}")
        print(f"Görseller '{self.output_dir}' klasörüne kategorilere göre ayrılarak kaydedildi")
        
        # Kategori özetini göster
        print("\nKategori özetleri:")
        for category, directory in self.categories.items():
            if directory.exists():
                file_count = len(list(directory.glob('*')))
                if file_count > 0:
                    print(f"  - {category}: {file_count} dosya")

def main():
    """Ana fonksiyon"""
    scraper = KahveDunyasiScraper()
    scraper.scrape_images()

if __name__ == "__main__":
    main()