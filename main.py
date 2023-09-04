import pytesseract
import cv2
import numpy as np
import urllib.request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

headless = True

def read_captcha(link):
    response = urllib.request.urlopen(link)
    image_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    kernel = np.ones((4,4),np.uint8)
    img = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    print("resim okunuyor")
    result = pytesseract.image_to_string(img).strip()[:6]
    print("resim okundu")
    return result   

#options.add_argument(r"--user-data-dir=C:\Users\ONAT\Desktop\Kargo Takip\Kargo Takip\bin\Debug\profile")

driver = None
def get_info(takip_kodu,firma):
    global driver
    options = webdriver.ChromeOptions()
    if headless: options.add_argument('headless')
    driver = webdriver.Chrome(executable_path=r"chromedriver.exe",chrome_options=options)
    if firma == "ARAS KARGO":
        url = "https://www.araskargo.com.tr/"
        driver.get(url)
        input_element = driver.find_element_by_id("mat-input-1")
        input_element.clear()
        input_element.send_keys(takip_kodu)
        while True:
            try:
                print("bekleniyor")
                driver.implicitly_wait(3)
                print("beklendi")
                captcha_element = driver.find_element_by_tag_name("captcha")
                img_element = captcha_element.find_element_by_tag_name("img")
                src_attribute = img_element.get_attribute("src")
                print("bulundu")
                break
            except:
                driver.execute_script("document.getElementsByTagName('mat-icon')[0].click()")
        input_element = driver.find_element_by_class_name("captcha-code")
        print("foto taranıyor")
        input_element.send_keys(read_captcha(src_attribute))
        print("tarandı ve yollandı")
        driver.find_element_by_class_name("small-btn").click()
        driver.implicitly_wait(1)
        while len(driver.find_elements_by_class_name("captcha-error")) > 0:
            driver.execute_script("document.getElementsByTagName('mat-icon')[0].click()")
            while True:
                try:
                    print("bekleniyor")
                    driver.implicitly_wait(3)
                    print("beklendi")
                    captcha_element = driver.find_element_by_tag_name("captcha")
                    img_element = captcha_element.find_element_by_tag_name("img")
                    src_attribute = img_element.get_attribute("src")
                    print("bulundu")
                    break
                except:
                    driver.execute_script("document.getElementsByTagName('mat-icon')[0].click()")
            input_element = driver.find_element_by_class_name("captcha-code")
            print("foto taranıyor")
            input_element.send_keys(read_captcha(src_attribute))
            print("tarandı ve yollandı")
            driver.find_element_by_class_name("small-btn").click()
            driver.implicitly_wait(1)
        while True:
            try:
               durum = driver.find_element_by_class_name("dialog__steps-title").get_attribute("innerText")
               break
            except: pass
        while True:
            try:
                driver.find_elements_by_class_name("dialog__selector")[1].click()
                line = driver.find_elements_by_class_name("kt-table__item__row")[-1]
                break
            except: pass
        return "Durum:"+durum+"\n"+"Son Olay:\n"+line.get_attribute("innerText")
    elif firma == "YURTİÇİ KARGO":
        url = "https://www.yurticikargo.com/tr/online-servisler/gonderi-sorgula?code="+takip_kodu
        driver.get(url)
        while str(driver.find_element_by_id("shipmentStatus").get_attribute("innerText")).startswith("***"):
            driver.implicitly_wait(1)
        return "Durum:"+driver.find_element_by_id("shipmentStatus").get_attribute("innerText")
    elif firma == "TRENDYOL EXPRESS":
        url = "https://kargotakip.trendyol.com/?orderNumber="+takip_kodu
        driver.get(url)
        while True:
            try:
                return "Durum:"+driver.find_element_by_class_name("delivery-history__first-item__left__status").get_attribute("innerText")
            except: pass
    elif firma == "MNG KARGO":
        url = "https://www.mngkargo.com.tr/gonderi-takip"
        driver.get(url)
        while True:
            try:
                driver.execute_script("document.getElementsByClassName('exit')[0].click()")
                break
            except:
                pass
        driver.implicitly_wait(2)
        captcha_code = driver.find_elements_by_class_name("captcha")[0].get_attribute("innerText")
        driver.execute_script(f"document.getElementsByTagName('input')[0].value = '{takip_kodu}'")
        driver.execute_script(f"document.getElementsByTagName('input')[1].value = '{captcha_code}'")
        driver.execute_script(f"document.getElementsByTagName('form')[0].submit()")
        driver.implicitly_wait(2)
        return driver.find_element_by_class_name('dispatchQuery_Bottom').get_attribute("innerText")
    elif firma == "PTT KARGO":
        url = "https://gonderitakip.ptt.gov.tr/"
        driver.get(url)
        driver.find_element_by_id("search-area").send_keys(takip_kodu)
        driver.find_element_by_id("searchButton").click()
        src = ""
        for element in driver.find_elements_by_tag_name("img"):
            if element.get_attribute("src") != None:
                if "gonderitakiplogolar" in element.get_attribute("src"):
                    src = element.get_attribute("src")
                    break
        print(src)
        if "1" in src: return "Kargoya verildi."
        elif "2" in src: return "Transfer Sürecinde"
        elif "3" in src: return "İl içi aktarmada"
        elif "4" in src: return "Dağıtımda"
        elif "5" in src: return "Teslim Edildi"
        else: return "hata"
        
    
      



    
