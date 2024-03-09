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
TASK_URL:str = "https://hermes.totus.pro/ko/task?taskUuid=b6deb2b8-d2da-4626-95c9-24c54298f43a"

# Options
options = {
    'driverLoadSpeed': 3,
    'redirectPageSpeed': 5,
    'scrollAmount': 250,
    'scrollSpeed': 0.5,
    'insertSpeed': 0.25,
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
try:
    with open('translate.txt', encoding='UTF-8') as data:
        for line in data:
            if (not line) or line == "\n":
                continue
            print(line)

            temp = list(filter(lambda u: u, re.split(r'(\![0-9]+\..+ \&\&)', line.replace('\n', ''))))
            trans.append({
                'timeId': re.sub(r'(\!.+\. )', "", temp[0]).replace(' &&', ''), # time stamp / ex: 00:06:930~00:08:345
                'text': temp[1].split('@@ ')[1] # Text
            })
except:
    pass
    
#print("Transcript ====>")
#print(trans)

# FIND CONTENT BOX ====>
contentsDiv = driver.find_element(By.CLASS_NAME, 'scroll-area')
wrapperDiv = driver.find_element(By.ID, 'script-scroll-area')

# INSERT =====>
print("INSERT START ==>")
def scroll_element(driver, element, scrollAmount):
    driver.execute_script("arguments[0].scrollTop += arguments[1];", element, scrollAmount)

is_scroll_y_end_script = """
function isScrollYEnd(ele) {
    return Math.ceil(ele.scrollTop + ele.offsetHeight) >= ele.scrollHeight;
}

return isScrollYEnd(arguments[0]);
"""

lastScrollTop = -1
while True:
    wrapperDiv = driver.find_element(By.CLASS_NAME, 'scroll-area').find_element(By.XPATH, '..')

    # GET CONTESTS =====>
    # get newest content
    contentsDiv = driver.find_element(By.CLASS_NAME, "scroll-area")
    videoScriptBoxDiv = contentsDiv.find_elements(By.XPATH, '*')

    for box in videoScriptBoxDiv:
        if (len(trans) == 0):
             break

        timeEl = None
        try:
            timeEl = box.find_element(By.CSS_SELECTOR, "[class*='ScriptArea__ScriptTimeWrapper'] p")
        except:
            break
        if timeEl == None:
            break

        timeId = timeEl.get_attribute("innerHTML").replace("<br>", "~")
        textField = box.find_elements(By.CLASS_NAME, "script-textarea")[1].find_element(By.TAG_NAME, "textarea")

        foundElements = [element for element in trans if element.get("timeId") == timeId]
        if (len(foundElements) == 0):
            continue
        print(box.find_element(By.CLASS_NAME, "script-textarea").get_attribute("innerText"))

        # Erase origin text
        driver.execute_script("arguments[0].value = '';", textField)

        # Insert
        texts = foundElements[0]['text'].split('%%')

        textField.click()
        for idx, text in enumerate(texts):
            textField.send_keys(text)

            if idx < len(texts) - 1:
                textField.send_keys(Keys.ENTER)
                
        trans.remove(foundElements[0])

        time.sleep(options["insertSpeed"])
    
    contentHeight = driver.execute_script("return arguments[0].scrollHeight", wrapperDiv)
    # Get the current scroll position
    currentScrollPosition = driver.execute_script("return arguments[0].scrollTop", wrapperDiv)

    isEndOfScroll = currentScrollPosition >= contentHeight - wrapperDiv.size['height']
    if not isEndOfScroll or len(trans) == 0:
        print("End of scroll reached")
        break

    scroll_element(driver, wrapperDiv, options['scrollAmount'])
    time.sleep(options['scrollSpeed'])

print("완료되었습니다... 검토 후 임시저장을 해주세요.")