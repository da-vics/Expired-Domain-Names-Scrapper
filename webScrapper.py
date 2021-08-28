import configs
from DbContext import DataBaseManager

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions


# download chrome driver
# https://sites.google.com/a/chromium.org/chromedriver/downloads

class Scrapper:

    def __init__(self):
        self.PATH = "C:\chromedriver.exe"
        self.isLoggIn = False
        self.driver = webdriver.Chrome(self.PATH)
        self.DB_Manager = DataBaseManager()
        self.DB_Manager.ConnectDB()

    def Login(self):
    
        self.driver.get("https://member.expireddomains.net/login/")

        login = self.driver.find_element_by_id('inputLogin')
        login.send_keys(configs.username)
        login = self.driver.find_element_by_id('inputPassword')
        login.send_keys(configs.password)
        login.send_keys(Keys.RETURN)

        if "» ExpiredDomains.net" in self.driver.title:
            print("Logged in")
            self.isLoggIn = True;
            self.driver.get(self.driver.current_url +
                       "domains/pendingdelete/?activetab=expireddomains")

        else:
            self.isLoggIn = False;
            print(self.driver.title)

    def GetDomainList(self):

        PageNum = 0;
        while True and self.isLoggIn:
        
            try:
                WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "base1")) ##name of table class
                )
                print("success!")

            except exceptions.WebDriverException:
                print("chrome not reachable!")
                break;

            except :
                page = self.driver.find_element_by_tag_name("body")
                if "You have reached the maximum page limit" in page.text:
                    print("Process Complete!")
                else:
                    print("Error can't load table! network error?")
                self.CloseBrower()
                break;
            
            try:
                list_elems = self.driver.find_element_by_class_name("base1")
                list_elems = list_elems.find_element_by_tag_name("tbody")
                list_elems = list_elems.find_elements_by_tag_name("tr")
                PageNum = PageNum+1
                print(F"Processing Page{PageNum} Data do not close the Dev Broswer!....")

                for elems in list_elems:
                    domain_name = elems.find_element_by_class_name("field_domain")
                    expiring_time = elems.find_element_by_class_name("field_enddate")
                    page_rank = elems.find_element_by_class_name("field_majestic_globalrank")
                    alexa_rank = elems.find_element_by_class_name("field_alexa")
                    backlink = elems.find_element_by_class_name("field_bl")
                    self.DB_Manager.InsertData(domain_name.text,expiring_time.text,page_rank.text,alexa_rank.text,backlink.text)
                    # print('{0} {1} {2} {3} {4}'.format(domain_name.text,expiring_time.text,page_rank.text,alexa_rank.text,backlink.text))

                link = self.driver.find_element_by_link_text("Next Page »")
                link.click()

            except exceptions.WebDriverException:
                print("chrome not reachable!")
                break;

            except Exception as err:
                    exception_type = type(err).__name__
                    print(exception_type)
                
    def CloseBrower(self):
        self.driver.quit()
