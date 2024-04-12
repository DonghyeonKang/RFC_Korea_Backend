from selenium import webdriver 
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# 원본 html 가져오기
def getOriginal(documentNumber):
    # 크롬 디버그 모드로 실행 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.rfc-editor.org/rfc/rfc" + documentNumber + ".html"

    driver.get(url)
    wait = WebDriverWait(driver, 5)  # 5초 동안 대기
    aram_html = driver.page_source # 웹 페이지의 전체 HTML 소스 코드 가져오기
    file = open("htmls/" + documentNumber + ".html","w",encoding="utf-8")
    file.write(aram_html)
    driver.quit()

    return aram_html

# 