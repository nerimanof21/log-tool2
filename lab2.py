import re
import csv
import json
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By

# Çıxış fayllarının yolları
URL_STATUS_REPORT_FILE = "url_status_report.txt"
MALWARE_CANDIDATES_FILE = "malware_candidates.csv"
ALERT_JSON_FILE = "alert.json"
SUMMARY_REPORT_FILE = "summary_report.json"

# 1. Access log-dan URL-ləri və status kodlarını çıxarmaq
def parse_access_log(log_file):
    url_status = []
    try:
        with open(log_file, 'r') as file:
            for line in file:
                match = re.search(r'^(\S+) \S+ \S+ \[.*?\] ".*? (.*?) HTTP/\d\.\d" (\d{3})', line)
                if match:
                    url = match.group(2)  # URL
                    status_code = match.group(3)  # Status kodu
                    url_status.append((url, status_code))
    except FileNotFoundError:
        print(f"Xəta: {log_file} faylı tapılmadı.")
    except Exception as e:
        print(f"Xəta: {e}")
    return url_status

# 2. 404 status kodu ilə URL-ləri müəyyən etmək
def count_404_urls(url_status):
    count = defaultdict(int)
    for url, status in url_status:
        if status == '404':
            count[url] += 1
    return count

# 3. URL-ləri status kodları ilə fayla yazmaq
def write_url_status_report(url_status, output_file):
    try:
        with open(output_file, 'w') as file:
            for url, status in url_status:
                file.write(f"{url} {status}\n")
        print(f"URL statusları yazıldı: {output_file}")
    except Exception as e:
        print(f"Xəta: {e}")

# 4. 404 URL-ləri CSV faylında yazmaq
def write_malware_candidates(counts, output_file):
    try:
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['URL', '404_count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for url, count in counts.items():
                writer.writerow({'URL': url, '404_count': count})
        print(f"404 URL-ləri yazıldı: {output_file}")
    except Exception as e:
        print(f"Xəta: {e}")

# 5. Veb scraping (Selenium ilə)
def scrape_blacklist(url):
    blacklist = []
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        elements = driver.find_elements(By.XPATH, "//li")
        for element in elements:
            blacklist.append(element.text)
        driver.quit()
        print(f"Qara siyahı uğurla analiz edildi: {url}")
    except Exception as e:
        print(f"Xəta: Qara siyahı çəkilmədi. {e}")
    return blacklist

# 6. URL-ləri qara siyahı ilə müqayisə etmək
def find_matching_urls(url_status, blacklist):
    matches = []
    for url, status in url_status:
        domain = re.sub(r'https?://(www\.)?', '', url).split('/')[0]
        if domain in blacklist:
            matches.append((url, status))
    return matches

# 7. JSON faylında uyğun URL-ləri yazmaq
def write_alert_json(matches, output_file):
    try:
        alerts = [{'url': url, 'status': status} for url, status in matches]
        with open(output_file, 'w') as json_file:
            json.dump(alerts, json_file, indent=4)
        print(f"Uyğun URL-lər JSON formatında yazıldı: {output_file}")
    except Exception as e:
        print(f"Xəta: {e}")

# 8. Xülasə hesabatı yaratmaq
def write_summary_report(url_status, counts, output_file):
    summary = {
        'total_urls': len(url_status),
        'total_404': sum(counts.values()),
        'unique_404_urls': len(counts)
    }
    try:
        with open(output_file, 'w') as json_file:
            json.dump(summary, json_file, indent=4)
        print(f"Xülasə hesabatı yaradıldı: {output_file}")
    except Exception as e:
        print(f"Xəta: {e}")

# Əsas funksiya
def main():
    log_file = 'access_log.txt'
    blacklist_url = 'http://127.0.0.1:8000'

    print("Analiz prosesi başlanır...")

    # 1. Access log-dan URL-ləri və status kodlarını çıxarın
    url_status = parse_access_log(log_file)
    if not url_status:
        print("URL və status kodları çıxarıla bilmədi.")
        return

    # 2. 404 status kodu ilə URL-ləri müəyyən edin
    counts = count_404_urls(url_status)
    if not counts:
        print("Heç bir 404 status kodlu URL tapılmadı.")

    # 3. URL-lərin siyahısını status kodları ilə yazın
    write_url_status_report(url_status, URL_STATUS_REPORT_FILE)

    # 4. 404 URL-ləri CSV faylında yazın
    write_malware_candidates(counts, MALWARE_CANDIDATES_FILE)

    # 5. Veb scraping (Selenium ilə)
    blacklist = scrape_blacklist(blacklist_url)
    if not blacklist:
        print("Qara siyahı uğurla çəkilə bilmədi.")

    # 6. URL-ləri qara siyahı ilə müqayisə edin
    matches = find_matching_urls(url_status, blacklist)

    # 7. Uyğun URL-ləri JSON faylında yazın
    write_alert_json(matches, ALERT_JSON_FILE)

    # 8. Xülasə hesabatı yaradın
    write_summary_report(url_status, counts, SUMMARY_REPORT_FILE)

    print("Analiz prosesi tamamlandı!")

if __name__ == "__main__":
    main()
