from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import random
import urllib.parse
import pymongo
from pymongo import MongoClient

a= "12345"
client = MongoClient("mongodb+srv://melekmbbal:"+a+"@datas.ws7ckaq.mongodb.net/?retryWrites=true&w=majority&appName=datas")
db = client["Yazlab_Project"] # database
collection = db["datas"] # collection

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    
url = "https://dergipark.org.tr/tr/search?q=deep+learning&section=articles"

data = {"name": "Melek", "surname": "Bal", "age": 21}
collection.insert_one(data)


datam = None

def index(request):
    global datam
    
    if request.method=='POST':
        data=request.POST.get('search')
        datam = data
        return render(request, 'pages/index.html',{'data':data})
        
    return render(request, 'pages/index.html')
print ("helloo melekcim")
print (datam)

if(datam != None):
    arama_url = urllib.parse.quote_plus(datam)

    url1 = f"https://dergipark.org.tr/tr/search?q={arama_url}"

    def get_data(url):
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        return soup

    soup = get_data(url1)

    def find_links(soup):
        links = soup.find_all('h5', class_='card-title')
        link_result = []
        for link in links[:10]:
            link_result.append(link.a['href'])
            
        return link_result

    def scrapping(soup):
        soup = get_data(url1)
        titles = soup.find_all('h5', class_='card-title')
        title_result = []
        for title in titles[:10]:  
            title_result.append(title.a.text.strip())
            
    def get_authours(soup):
        authors_result = []    
        for i in range(len(find_links(soup))):
            soup1 = get_data(find_links(soup)[i]) 
            authors = soup1.find_all('p', class_='article-authors') 
            for a in authors[:1]:  
                authors_result.append(' '.join(a.text.strip().split()))
                
        return authors_result
                    
    def get_dates(soup):   
        dates = soup.find_all('small', class_='article-meta')   
        date_result = []
        for date in dates[:20]:
            text = date.get_text(strip=True)
            if '(' in text and ')' in text:
                year = text[text.find('(') + 1: text.find(')')]
                date_result.append(year)
                
        return date_result
                
    def get_types(soup):    
        type = soup.find_all('span', class_='badge badge-secondary')
        type_result = []
        for t in type[:10]:
            type_result.append(t.text.strip())
            
        return type_result

    def get_publishers(soup):    
        publisher_result = []  
        for i in range(len(find_links(soup))):
            soup1 = get_data(find_links(soup)[i]) 
            publisher = soup1.find_all('h1', id='journal-title') 
            for p in publisher[:10]:  
                publisher_result.append(p.text.strip())  
                
        return publisher_result

    def get_keywords(soup):
        keywords_result = []    
        for i in range(len(find_links(soup))):
            soup1 = get_data(find_links(soup)[i]) 
            keywords = soup1.find_all('div', class_='article-keywords data-section')
            for k in keywords[:9]:  
                if k.p:
                    keywords_result.append(k.p.text.strip()) 
                    
        return keywords_result[1:]

    def get_sums(soup):
        sums_result = []    
        for i in range(len(find_links(soup))):
            soup1 = get_data(find_links(soup)[i]) 
            sums = soup1.find_all('div', class_='article-abstract data-section') 
            for a in sums:  
                summary = a.p.text.strip()
                if summary:  # Boş özetlerin eklenmemesi için kontrol
                    sums_result.append(summary)
                
        return sums_result
                
    def get_id():
        id = []
        for _ in range(10):
            rastgele_sayi = random.randint(1, 999999)        
            while rastgele_sayi in id:
                rastgele_sayi = random.randint(1, 999999)
            id.append(rastgele_sayi)
        
        
        return id


    print(get_authours(soup)) 
