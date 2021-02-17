import csv
from bs4 import BeautifulSoup
from selenium import webdriver

def get_url(search_term,page):
    search_term = search_term.replace(" ","+")
    target = f"https://www.amazon.in/s?k={search_term}&ref=nb_sb_noss_2&page={page}"
    return target

#Generalize the pattern 
def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    i_url = "https://www.amazon.in"+atag.get('href')

    try:
        # price_parent = item.find('span','a-price')
        # price = price_parent.find('span','a-offscreen').text
        price = item.find('span','a-price-whole').text
    except AttributeError:
        return

    try:
        rating = item.i.text
        review = item.find('span',{'class':'a-size-base','dir':'auto'}).text
    except AttributeError:
        rating = ""    
        review =""

    result = (description,price,rating,review,i_url)
    return result


def main(search_term):
    driver = webdriver.Chrome("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")

    records =[]
    for page in range(1,21):
        driver.get(get_url(search_term,page))
        soup = BeautifulSoup(driver.page_source,'html.parser')
        results = soup.find_all('div',{'data-component-type' : 's-search-result'})
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    driver.close()

    with open('results.csv', 'w',newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['Description','Price (Rs.)','Rating','Review','URL'])
        writer.writerows(records)

main('refrigerator')