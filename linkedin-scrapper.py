from selenium import webdriver
import time
from bs4 import BeautifulSoup
import xlsxwriter
from tkinter import *

class Linkedin():
    def getData(self):
        driver = webdriver.Chrome('../chromedriver.exe')
        driver.get('https://www.linkedin.com/login')
        driver.find_element_by_id('username').send_keys('USER NAME') #Enter username of linkedin account here
        driver.find_element_by_id('password').send_keys('PASSWORD')  #Enter Password of linkedin account here
        driver.find_element_by_xpath("//*[@type='submit']").click()

        #*********** Search Result ***************#
        search_key = "data analyst" # Enter your Search key here to find people
        key = search_key.split()
        keyword = ""
        for key1 in key:
            keyword = keyword + str(key1).capitalize() +"%20"
        keyword = keyword.rstrip("%20")
            
        global data
        data = []

        for no in range(1,30):
            start = "&page={}".format(no) 
            search_url = "https://www.linkedin.com/search/results/people/?keywords={}&origin=SUGGESTION{}".format(keyword,start)
            driver.get(search_url)
            driver.maximize_window()
            for scroll in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            search = BeautifulSoup(driver.page_source,'lxml')
            peoples = search.findAll('a', attrs = {'data-control-name':'search_srp_result'})
            count = 0
            print("Going to scrape Page {} data".format(no))
            
            for people in peoples:
                count+=1

                if count%2==0:
                    
                    
                    
                    profile_url = "https://www.linkedin.com" + str(people['href'])
                    driver.get(profile_url)

                    # #********** Profile Details **************#
                    loc = ""
                    page = BeautifulSoup(driver.page_source,'lxml')
                    try:
                        cover = page.find('img', attrs = {'class':'profile-background-image__image relative full-width full-height'})['src']
                    except:
                        cover = 'None'

                    try:
                        profile = page.find("img", attrs = {
                            'class':'lazy-image pv-top-card-section__photo presence-entity__image EntityPhoto-circle-9 loaded'})['src']
                        
                    except:
                        profile = "None"

                    try:
                        title = str(page.find("li", attrs = {'class':'inline t-24 t-black t-normal break-words'}).text).strip()
                    except:
                        title = 'None'
                    try:
                        heading = str(page.find('h2', attrs = {'class':'mt1 t-18 t-black t-normal'}).text).strip()
                    except:
                        heading = 'None'
                    try:
                        loc = str(page.find('li', attrs = {'class':'t-16 t-black t-normal inline-block'}).text).strip()
                    except:
                        heading = 'None'


                    #*******  Contact Information **********#
                    time.sleep(2)
                    driver.get(profile_url + 'detail/contact-info/')

                    info = BeautifulSoup(driver.page_source, 'lxml')
                    details = info.findAll('section',attrs = {'class':'pv-contact-info__contact-type'})
                    try:
                        websites = details[1].findAll('a')
                        for website in websites:
                            website = website['href']
                            
                    except:
                        website = 'None'
                    try:
                        phone = details[2].find('span').text
                    except:
                        phone = 'None'
                    try:
                        email = str(details[3].find('a').text).strip()
                    except:
                        email = 'None'
                    try:
                        connected = str(details[-1].find('span').text).strip()
                    except:
                        connected = 'None'

                    
                    data.append({'profile_url':profile_url,'cover':cover,'profile':profile,'title':title,'heading':heading,'loc':loc,'website':website,'phone':phone,'email':email,'connected':connected,})
            print("!!!!!! Data scrapped !!!!!!")
                
        driver.quit()
    def writeData(self):
        workbook = xlsxwriter.Workbook("linkedin-search-data.xlsx")
        worksheet = workbook.add_worksheet('Peoples')
        bold = workbook.add_format({'bold': True})
        worksheet.write(0,0,'profile_url',bold)
        worksheet.write(0,1,'Name',bold)
        worksheet.write(0,2,'cover',bold)
        worksheet.write(0,3,'profile image',bold)
        worksheet.write(0,4,'heading',bold)
        worksheet.write(0,5,'location',bold)
        worksheet.write(0,6,'website',bold)
        worksheet.write(0,7,'phone',bold)
        worksheet.write(0,8,'email',bold)
        worksheet.write(0,9,'connected',bold)
        for i in range(1,len(data)+1):
           
            try:
                worksheet.write(i,0,data[i]['profile_url'])
            except:
                pass
            try:
                worksheet.write(i,1,data[i]['title'])
            except:
                pass
            try:
                worksheet.write(i,2,data[i]['cover'])
            except:
                pass
            try:
                worksheet.write(i,3,data[i]['profile'])
            except:
                pass
            try:
                worksheet.write(i,4,data[i]['heading'])
            except:
                pass
            try:
                worksheet.write(i,5,data[i]['loc'])
            except:
                pass
            try:
                worksheet.write(i,6,data[i]['website'])
            except:
                pass
            try:
                worksheet.write(i,7,data[i]['phone'])
            except:
                pass
            try:
                worksheet.write(i,8,data[i]['email'])
            except:
                pass
            try:
                worksheet.write(i,9,data[i]['connected'])
            except:
                pass
            
        workbook.close()

    def start(self):
        self.getData()
        self.writeData()
if __name__ == "__main__":
    obJH = Linkedin()
    obJH.start()
