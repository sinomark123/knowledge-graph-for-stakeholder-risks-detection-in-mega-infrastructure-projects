# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        binary = FirefoxBinary(r"C:\Program Files\Mozilla Firefox\firefox.exe")
        self.driver = webdriver.Firefox(firefox_binary=binary ,executable_path=r"D:\Code Working Area\Python\knowledge-graph-for-stakeholder-risks-detection-in-mega-infrastructure-projects\geckodriver-v0.32.0-win32\geckodriver.exe")
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("https://www.webofscience.com/wos/woscc/summary/9d814b9c-45f4-493c-bf8a-8cd309e560a7-593e357a/relevance/1")
        driver.get("https://access.clarivate.com/login?app=wos&detectSession=true&referrer=TARGET%3Dhttps%253A%252F%252Fwww.webofscience.com%252Fwos%253Fmode%253DNextgen%2526path%253D%25252Fwos%25252Fwoscc%25252Fsummary%25252F9d814b9c-45f4-493c-bf8a-8cd309e560a7-593e357a%25252Frelevance%25252F1%2526IsProductCode%253DYes%2526Init%253DYes%2526DestApp%253DUA%2526Func%253DFrame%2526action%253Dtransfer%2526SrcApp%253DCR%2526SID%253DEUW1ED0A6AcJ9JrySNLqZBovmZpjA%26SID%3DEUW1ED0A6AcJ9JrySNLqZBovmZpjA%26detectSessionComplete%3Dtrue")
        driver.get("https://www.webofscience.com/wos?app=wos&Func=Frame&SrcApp=CR&locale=zh-CN&SID=EUW1ED0A6AcJ9JrySNLqZBovmZpjA&mode=Nextgen&path=%2Fwos%2Fwoscc%2Fsummary%2F9d814b9c-45f4-493c-bf8a-8cd309e560a7-593e357a%2Frelevance%2F1&IsProductCode=Yes&Init=Yes&DestApp=UA&action=transfer")
        driver.get("https://www.webofscience.com/wos/woscc/summary/9d814b9c-45f4-493c-bf8a-8cd309e560a7-593e357a/relevance/1")
        driver.find_element("xpath", u"(.//*[normalize-space(text()) and normalize-space(.)='隐私偏好中心'])[1]/preceding::button[1]").click()
        driver.find_element("xpath", "//div[@id='snRecListTop']/app-export-menu/div/button/span").click()
        driver.find_element("id", "exportToExcelButton").click()
        driver.find_element("xpath", "//mat-radio-button[@id='radio3']/label/span[2]").click()
        driver.find_element("id", "mat-input-0").click()
        driver.find_element("id", "mat-input-0").clear()
        driver.find_element("id", "mat-input-0").send_keys("1001")
        driver.find_element("id", "mat-input-1").click()
        driver.find_element("id", "mat-input-1").clear()
        driver.find_element("id", "mat-input-1").send_keys("2000")
        driver.find_element("xpath", "(.//*[normalize-space(text()) and normalize-space(.)='Record Content:'])[1]/following::button[1]").click()
        driver.find_element("xpath", "//div[@id='global-select']/div/div[2]/div[4]/button/span").click()
        driver.find_element("xpath", "//mat-checkbox[@id='mat-checkbox-66']/label/span[2]").click()
        driver.find_element("xpath", "//mat-checkbox[@id='mat-checkbox-68']/label/span[2]").click()
        driver.find_element("xpath", "//mat-checkbox[@id='mat-checkbox-69']/label/span[2]").click()
        driver.find_element("xpath", "//mat-dialog-container[@id='mat-dialog-0']/app-custom-field-selection-dialog/div/div[5]/div/button[2]/span").click()
        driver.find_element("xpath", "(.//*[normalize-space(text()) and normalize-space(.)='Custom selection (14)'])[1]/following::button[1]").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
