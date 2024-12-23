# log-tool2
# URL Status Analizi və Qara Siyahı Müqayisəsi

Bu layihə, serverin `access.log` faylından URL-ləri və onların status kodlarını çıxarmaq, 404 status kodu ilə olan URL-ləri tapmaq, bu URL-ləri bir CSV faylında saxlamaq, qara siyahı ilə URL-ləri müqayisə etmək və nəticələri müxtəlif formatlarda (TXT, CSV, JSON) saxlamaq məqsədini daşıyır.

## Tələblər

- Python 3.x
- Selenium (Veb scraping üçün)
- Chrome WebDriver (Selenium ilə işləmək üçün)
- `re`, `csv`, `json`, `collections` modulları

Bu layihə üçün aşağıdakı Python paketlərinə ehtiyacınız var:
- Selenium (`pip install selenium`)

## Layihənin Əsas Fəaliyyətləri

Bu layihə aşağıdakı funksiyaları yerinə yetirir:

1. **Access log-dan URL-ləri və status kodlarını çıxarmaq**  
   Serverin `access.log` faylından URL-ləri və onların status kodlarını çıxarır.

2. **404 Status Kodlu URL-ləri Tapmaq**  
   404 status koduna sahib URL-ləri tapır və bunları sayır.

3. **URL-ləri Status Kodları ilə Fayla Yazmaq**  
   Tapılan URL-ləri və status kodlarını `url_status_report.txt` faylında saxlayır.

4. **404 URL-lərini CSV Faylında Yazmaq**  
   404 status kodu olan URL-ləri `malware_candidates.csv` faylında saxlayır.

5. **Qara Siyahı ilə Veb Scraping**  
   Selenium istifadə edərək bir URL-dən qara siyahı məlumatlarını çəkir.

6. **URL-ləri Qara Siyahı ilə Müqayisə Etmək**  
   Çəkilən qara siyahı ilə `access.log` faylındakı URL-ləri müqayisə edir.

7. **Uyğun URL-ləri JSON Faylında Yazmaq**  
   Qara siyahıya uyğun URL-ləri `alert.json` faylında saxlayır.

8. **Xülasə Hesabatı Yaratmaq**  
   URL-lərin ümumi sayını, 404 status kodlu URL-ləri və bunların unikallığını xülasə edən bir hesabat `summary_report.json` faylında saxlayır.

## Fayl Strukturu

- `access_log.txt` – Giriş log faylı (əldə edilən URL-lər və status kodları).
- `url_status_report.txt` – URL-lərin və onların status kodlarının saxlanıldığı fayl.
- `malware_candidates.csv` – 404 status kodu olan URL-lərin siyahısı.
- `alert.json` – Qara siyahıya uyğun olan URL-lərin saxlanıldığı fayl.
- `summary_report.json` – Xülasə hesabatı faylı.

## İstifadə

1. **Kodun icrasına başlamadan əvvəl, aşağıdakıları təmin edin:**
   - `access_log.txt` faylının mövcudluğu.
   - Chrome WebDriver-ın düzgün şəkildə quraşdırılması.
   - Selenium paketinin quraşdırılması (`pip install selenium`).

2. **Kodu icra etmək üçün:**

   ```bash
   python script_name.py
