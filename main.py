import requests
import json
import os
from typing import List
from pyquery import PyQuery


def ambil_link(link_hal): # mendifinisikan fungsi ambil_link dengan parameter (link_hal)
    response = requests.get(link_hal) # mengirim request ke link yang diberikan
    html = PyQuery(response.text) #parsing teks html dari response

    links = [] # membuat list kosong untuk menyimpan link

    for a in html.find('div[class="lm_content mt10"] li a'): # looping melalui inspect element untuk menemukan link
        links.append(PyQuery(a).attr('href')) # menambahkan link kedalam list dengan element html (a) yang memiliki atribut 'href'

    return links

def buat_folder(folder): # mendefinisikan fungsi untuk membuat folder
     if not os.path.exists(folder): #memeriksa folder apakah sudah ada
          os.makedirs(folder) # membuat folder jika belum ada


def text_bersih(bersih): # mendefinisikan fungsi untuk membersihkan text dari karakter yang tidak valid
     bersih_text = bersih.replace("?", "").replace(" ", "_").replace(",", "").replace("/", "") # membersihkan teks
     return bersih_text 

def extract(link_web): #mendefinisikan fungsi extract dengan parameter (link_web)
    response = requests.get(link_web)
    html = PyQuery(response.text)

    results = { # membuat dictionary 'results' untuk menyimpan hasil ekstraksi
        "url": [PyQuery(url).attr('href') for url in html.find('head>link[href="https://www.cnbcindonesia.com"]')], # mencari dan menyimpan link kedalam "url"
        "url_page": [PyQuery(url_page).attr('href') for url_page in html.find('head>link[rel="canonical"]')],
        "title": html.find('div.jdl div[class="container"] h1').text(),
        "data": { # membuat sub-dictionary 'data' untuk menyimpan data lainnya
            "author": html.find('div[class="author"]').text(),
            "posted": html.find('div[class="date"]').text(),
            "url_media": [PyQuery(url_media).attr('src') for url_media in html.find('div[class="media_artikel"] img ')],
            "description": html.find('div[class="detail_text"] p').text(),
            "tags": [PyQuery(tag).text() for tag in html.find('div[class="trending-tag mt35 mb45 gtm_tag"] a')]
        }
        
    }

    folder = "data_sample" # folder untuk menyimpan data
    buat_folder(folder) # membuat folder jika belum ada
    title = text_bersih(results.get("title")) 
    path_file = os.path.join(folder, f'{title}.json') #membuat path file json
    with open(path_file, 'w', encoding='utf-8') as file: # membuka file json
        json.dump(results, file, ensure_ascii=False, indent=2, default=str) # menyimpan data ke dalam file json


def jalankan(): # mendefinisikan fungsi jalankan
    link_utama = 'https://www.cnbcindonesia.com/indeks' #link utama

    halaman = 1 
    while True:
        halaman += 1 #menambah nilai halaman
        linkks = ambil_link(f'{link_utama}/{halaman}') # mengambil link dari halaman yang diberikan
        for url in linkks: # melakukan iterasi pada link yang diperoleh
            extract(url) # mengekstrak data dari link
            break # berhenti dari loop setelah mengekstrak data dari satu link
        if halaman == 6: # berhenti setelah mencapai halaman ke-6
            break

        

jalankan() # memanggil fungsi jalankan untuk memulai
