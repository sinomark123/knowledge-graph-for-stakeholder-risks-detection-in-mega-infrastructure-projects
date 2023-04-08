import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By

link: str = "https://www.webofscience.com/wos/woscc/summary/9d814b9c-45f4-493c-bf8a-8cd309e560a7-593e357a/relevance/1"
driverPath: str = r"D:\Code Working Area\Python\RealEstate_Project\venv\chromedriver_win32\chromedriver"
cookies: dict = {}


def originalCookies() -> bool:
    strings = """WOSSID=EUW1ED0C19aHLjzPvCm7XhQZU42rm; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; OptanonAlertBoxClosed=2022-10-09T13:20:04.795Z; bm_sz=7D0A15B066B9D6CF25CD8927CB6E39D1~YAAQTDlDF/pVpqaDAQAACMsuzxEhOULX3kpOOd08O4X7AgvCN5EJBpc3dUfmA4wP5rfCEVEsmtqLmE1KAUod9/AX0S3xlNSBHvEWrMICw4M/8IeulRrY/xDPWUTwwzzmR/sQCsxksqKBVlzF5f5CVV5WzwEzqJQM4kZXXvyFbHixtqbO4Z4cTeLTQFilxPEDsFOBbYjVprY0MWyf24jCakk7YV7vmq1nOKBzmCy7UeibBSkaaO++1XVkZCGahTGPDXaRSrSjK5OgAKoptfDL9PoI5tJxRhtUSxUh5QKoqgh/06B21IrjjsY=~3551793~4604978; _abck=A201DF1689AE93DA7214BF5D803E7C59~0~YAAQTDlDFwJWpqaDAQAAVs8uzwi0KaDn6h1jpY7IArc/wx+9XJtgN6ovYBjKtP603/tA+5Ovnl/8UsKhl+Qvob6byXYN4CTehiXRmul17ycTuG6vo2sJJz2P9p6ZrgnFgXJ336uaOAIeZcloxuYl3Rd2itRBWZQh0fddUBdmuumvnzKQ8e2aW5nqNhz++cmyH/b8E15+Orehqxk1fdd6uX3s6n4S4eY+tnKAKUEzacw81zYcHuiOoHv3Fiqrt8FuyI3cY+OTcGr/jFI7WZ1+5s12c7mFHwqK8d/ALDXWFGNDCFjK3UW6RXFVOvdrV16KWn8BucHizoK64j1xRPERgIC2+vie6w13jdRMK7eG1sMdUvWCgkI+8/wzUvb+1+9KHtk0uj+1sdrdph8LIXvjvq+ct3szam3zxvZBGlIG~-1~-1~-1; _sp_ses.840c=*; ak_bmsc=D76E149324116AEC0D8E537FDF732578~000000000000000000000000000000~YAAQHjlDFxPxxa2DAQAAXNzLzxFYOH4I5Rv0heuh+2Fj+G8UrrrYcxAfqfivUw97/u9ujnwwPcyPKXDOIvCJCq2oBc9UjcgsvIiO8837nnVpY/CeDo+G+/67pUWch13aZaz1ASTSkL4/YconkwKcye1p5qz0EMUrHvQWYQkQ26YoLwyXs9ja2rvguwfxGk+0lZgaDHQUFRpD+GoLFCJGGfgLQHTblrRe3z/q0GPkq2cMrodhadaxADqBp4ZSrl1EKZlerOOunPme+HTUuSn38WiQ6kkjlyW8TCO47TwJH+LcpgFF5j/OJZx9IJbAnMYcb8tYhc8MeMAp28ZMMU57mdShchFOAawI3ZB/fqH8RhxSHWJBPjsde+c3y+HFmE5sK/A1nB3Wl47z2La4x7wZXPQ=; _sp_id.840c=8c62babc-f257-4506-9888-870ad1606f33.1665321596.5.1665638955.1665628342.5b63f5b4-4679-42e6-b2c6-099cbb67ff40.f0d8584a-e555-432d-bf80-65ea9c4e763d.b34d1767-316c-41a1-8f71-c7416b6b4326.1665638587418.7; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Oct+13+2022+13:29:15+GMT+0800+(香港标准时间)&version=6.39.0&isIABGlobal=false&hosts=&consentId=489e98b0-37cf-4943-ba66-8059c7b91636&interactionCount=1&landingPath=NotLandingPage&groups=C0001:1,C0003:1,C0004:1,C0005:1,C0002:1&geolocation=HK;HCW&AwaitingReconsent=false; bm_sv=379C8082B7FDA1AE7684FDF6DCD978DE~YAAQHjlDF5Pzxa2DAQAARWTVzxEBKrBZSN5rLdYQu9rX817Cih3yjTnJBc3iyG1T3VIxfRUWawRpNu00tO4jiO19reA43mnS8jv2QbwbnB6Ym5tF8SnLpY/ORcXgNV44YNZtvepoMc9+XE9AWNU7R8KOQfdIdXGz16yYsnu8ZXzMFS7bpkAkEQ3ISqvL2qWYV7LaHw9YroYKMmn4K8GSO2cKSyrnBJZ1pIM4LuANFeRFrw6RuhgmCb3FvcLnXdE16bPVL0zj~1; RT="z=1&dm=www.webofscience.com&si=e00b35d2-e2a3-4047-b904-777685511d3f&ss=l96mfe05&sl=0&tt=0&bcn=//684d0d48.akstat.io/&ld=6cj7o&ul=5jg0&hd=5k0d" """
    strSplit = strings.split("; ")
    for obstcle in strSplit:
        temp: list = obstcle.split("=")
        cookies[temp[0]] = "=".join(temp[1:])
    return True


class Trivial:

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(driverPath))
        self.driver.implicitly_wait(10)

    def initial(self):
        driver = self.driver
        driver.get(link)
        driver.get(
            "https://access.clarivate.com/login?app=wos&detectSession=true&referrer=TARGET%3Dhttps%253A%252F%252Fwww.webofscience.com%252Fwos%253Fmode%253DNextgen%2526path%253D%25252Fwos%25252Fwoscc%25252Fsummary%25252F9d814b9c-45f4-493c-bf8a-8cd309e560a7-593e357a%25252Frelevance%25252F1%2526IsProductCode%253DYes%2526Init%253DYes%2526DestApp%253DUA%2526Func%253DFrame%2526action%253Dtransfer%2526SrcApp%253DCR%2526SID%253DEUW1ED0A6AcJ9JrySNLqZBovmZpjA%26SID%3DEUW1ED0A6AcJ9JrySNLqZBovmZpjA%26detectSessionComplete%3Dtrue")
        driver.get(
            "https://www.webofscience.com/wos?app=wos&Func=Frame&SrcApp=CR&locale=zh-CN&SID=EUW1ED0A6AcJ9JrySNLqZBovmZpjA&mode=Nextgen&path=%2Fwos%2Fwoscc%2Fsummary%2F9d814b9c-45f4-493c-bf8a-8cd309e560a7-593e357a%2Frelevance%2F1&IsProductCode=Yes&Init=Yes&DestApp=UA&action=transfer")
        driver.get(link)
        # step into cookies selection
        driver.find_element("xpath", u"(.//*[normalize-space(text()) and normalize-space(.)='隐私偏好中心'])[1]/preceding::button[1]").click()
        # goto export
        driver.find_element("xpath", "//div[@id='snRecListTop']/app-export-menu/div/button/span").click()



if __name__ == "__main__":
    Trivial().initial()
