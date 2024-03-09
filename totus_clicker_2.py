import time
import pyautogui

def auto_clicker(duration, interval):
    time.sleep(5)  # 5초 대기

    end_time = time.time() + duration
    while time.time() < end_time:
        pyautogui.click()
        time.sleep(interval)  # 지정된 간격만큼 대기

if __name__ == "__main__":
    # 실행 시간 및 클릭 간격 설정
    total_duration = 60000  # 예: 30초 동안 실행
    click_interval = 0.02  # 예: 0.1초 간격으로 클릭
    
    while True:
        try:
            auto_clicker(total_duration, click_interval)
        except:
            pass