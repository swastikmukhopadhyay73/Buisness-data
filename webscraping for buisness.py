import requests
from bs4 import BeautifulSoup
import csv

def scrape_business_listings(base_url, max_page):
    all_business_data = []

    for page in range(1, max_page + 1):
        page_url = f"{base_url}?page={page}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        business_listings = soup.find_all('div', class_='listing')
        for listing in business_listings:
            business_data = {}
            business_data['Name'] = listing.find('h2').text.strip()
            business_data['Location'] = listing.find('span', class_='location').text.strip()
            business_data['City'] = listing.find('span', class_='city').text.strip()
            business_data['P.O. Box'] = listing.find('span', class_='po-box').text.strip()
            business_data['Phone'] = listing.find('span', class_='phone').text.strip()
            business_data['Mobile'] = listing.find('span', class_='mobile').text.strip()
            business_data['Company Page Link'] = listing.find('a')['href']
            business_data['Logo URL'] = listing.find('img')['src']
            all_business_data.append(business_data)

    return all_business_data

def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)
        print(f"Success!\nData written to CSV file: {filename}")

if __name__ == "__main__":
    base_url = 'https://www.yellowpages-uae.com/uae/restaurant'
    max_page = 7  

    business_data = scrape_business_listings(base_url, max_page)
    save_to_csv(business_data, 'results.csv')
    
