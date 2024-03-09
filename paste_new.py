# 설치법
# Py version: 3.11.6
# 1. pip install -r requirements.txt

# 사용법
# 1. translate.txt 파일에 입력할 텍스트들을 형식에 맞게 넣는다.
# 2. 하단 TASK_URL에 작업할 URL을 넣어준다.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

driver = webdriver.Chrome()

# GPT API Key
GPT_API_KEY:str = ""

# URL: 번역할 작업물이 있는 URL 주소
URL:str = "https://totus.pro/ko" # Main Page
TASK_URL:str = "https://main.totus.pro/ko/videoEditor?taskUuid=0a370d56-7274-40b0-99ae-21839f481fdb"

# Options
options = {
    'driverLoadSpeed': 3,
    'redirectPageSpeed': 5,
    'scrollAmount': 100,
    'scrollSpeed': 0.1,
    'insertSpeed': 0.2,
}

# Driver Load ==============>
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),  options=chromeOptions)
driver.get(URL)
time.sleep(options["driverLoadSpeed"])

# Login ========>
#loginBtn = driver.find_element(By.CLASS_NAME, "signin-button")
#loginBtn.click()
input("로그인을 한 다음 터미널에 Enter를 입력해주세요.")

# TASK START =======>
driver.get(TASK_URL)
time.sleep(options["redirectPageSpeed"])

# GET TEXT FILE ====>
trans = []
with open('translate.txt', encoding="UTF-8") as data:
    for line in data:
        if (not line) or line == "\n":
            continue
        #print(line)
        temp = list(filter(lambda u: u, re.split(r'(\![0-9]+\.)', line.replace('\n', ''))))
        trans.append({
            'textId': int(re.sub(r'(\!|\.)', "", temp[0])), # Number
            'text': temp[1].split('@@ ')[1] # Text
        })
        print(temp[1])
#print(trans)

# FIND CONTENT BOX ====>
contentsDiv = driver.find_element(By.ID, "script").find_element(By.CLASS_NAME, "content")
wrapperDiv = contentsDiv.find_element(By.XPATH, '..')

# INSERT =====>
print("INSERT START ==>")
def scroll_element(driver, element, scrollAmount):
    driver.execute_script("arguments[0].scrollTop += arguments[1];", element, scrollAmount)

lastScrollTop = -1
while True:
    # GET CONTESTS =====>
    # get newest content
    contentsDiv = driver.find_element(By.ID, "script").find_element(By.CLASS_NAME, "content")
    videoScriptBoxDiv = contentsDiv.find_elements(By.CLASS_NAME, "video-script-box")

    for box in videoScriptBoxDiv:
        if (len(trans) == 0):
             break

        textId = int(box.find_element(By.CLASS_NAME, "layer-text").get_attribute("innerText").split('#')[1])
        textFieldDiv = box.find_elements(By.CLASS_NAME, "editable-text")[1]

        foundElements = [element for element in trans if element.get("textId") == textId]
        if (len(foundElements) == 0):
            continue
        print(box.find_element(By.CLASS_NAME, "layer-text").get_attribute("innerText"))

        # Erase origin text
        driver.execute_script("arguments[0].innerText = '';", textFieldDiv)

        # Insert
        texts = foundElements[0]['text'].split('%%')

        textFieldDiv.click()
        for idx, text in enumerate(texts):
            textFieldDiv.send_keys(text)

            if idx < len(texts) - 1:
                print("enter!")
                textFieldDiv.send_keys(Keys.ENTER)
                
        trans.remove(foundElements[0])

        time.sleep(options["insertSpeed"])
    
    # Move Scroll
    currentScrollTop = driver.execute_script("return arguments[0].scrollTop;", wrapperDiv)
    # Check End of scroll
    if currentScrollTop == lastScrollTop:
        break
    lastScrollTop = currentScrollTop

    scroll_element(driver, wrapperDiv, options['scrollAmount'])
    time.sleep(options['scrollSpeed'])

print("완료되었습니다... 검토 후 임시저장을 해주세요.")