from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import datetime as dt
from colorama import Fore, Style
from colorama import init
import win32api
import json

init()
options = ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument('--headless')

with open("settings.json", "r") as file:
    json_data = json.load(file)

driver = Chrome(options=options)
driver.set_window_size(800, 600)
login = {
    "xf_user": "",
    "xf_tfa_trust": "",
    "G_ENABLED_IDPS": "",
    "xf_language_id": "",
    "dfuid": "", 
    "xf_logged_in": "",
    "xf_session": "", 
    "xf_feed_custom_order": "first_post_likes", 
    "xf_chatbox_roomId": "1", 
    "xf_viewedContestsHidden": "1",
    "zelenka.guru_xf_tc_lmad": ""
}
lolz_thread = []
lolz_link = 'https://zelenka.guru'
contests_count = 0

def on_exit(sig, func=None):
    print("Завершаем работу...")
    driver.quit()
win32api.SetConsoleCtrlHandler(on_exit, True)


def anti_captha():
    button = driver.find_elements(By.XPATH, '//button[text()="Я не робот"]')
    if button:
        print('Ответили сайту: я не робот')
        button[0].click()
        
size = driver.execute_script("return [window.innerWidth, window.innerHeight];")
print(f"{Fore.LIGHTCYAN_EX}Текущее разрешение: {Fore.GREEN}{size}")

def update_contests_threads():
    anti_captha()
    driver.get(f'{lolz_link}/forums/contests/?node_id=766&order=post_date&direction=desc')
    anti_captha()
    for name, value in login.items():
        driver.add_cookie({'name': name, 'value': value})
    anti_captha()
    driver.refresh()
    anti_captha()
    discussion_list = driver.find_element(By.CSS_SELECTOR, ".discussionListItems")
    if discussion_list:
        latest_threads = driver.find_element(By.CSS_SELECTOR, ".latestThreads")
        if latest_threads:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.find_all('a', {'class': 'listBlock main PreviewTooltip'})
            print(f"{Fore.GREEN}{dt.datetime.now()} | {Fore.YELLOW}Найдено новых розыгрышей: {Style.RESET_ALL}{len(elements)}")
            for element in elements:
                lolz_thread.append(element.get('href'))

def solver_contests():
    global contests_count
    for i in lolz_thread:
        try:
            anti_captha()
            driver.get(f'{lolz_link}/{i}')
            driver.execute_async_script("""
                var callback = arguments[arguments.length - 1];
                
                var intervalId = setInterval(function() {
                    var element = document.getElementsByClassName('messageText SelectQuoteContainer baseHtml ugc')[0];
                    if (element) {
                        clearInterval(intervalId);
                        element.remove();
                        callback();
                    }
                }, 100);
            """)
            anti_captha()
            print(f'{Fore.GREEN}{dt.datetime.now()} | {Fore.LIGHTBLACK_EX}Пытаюсь принять участие // {Fore.LIGHTBLUE_EX}{lolz_link}/{i}')
            iframe = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[id^="cf-chl-widget-"]'))
            )
            driver.switch_to.frame(iframe)
            success_elem = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, "success")) and
                EC.presence_of_element_located((By.CSS_SELECTOR, '#success[style*="display: inline; visibility: visible;"]'))
            )
            driver.switch_to.default_content()
            wait = WebDriverWait(driver, 30)
            button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "LztContest--Participate")))
            driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top - window.innerHeight/2)", button)
            time.sleep(2)
            button.click()
            wait = WebDriverWait(driver, 30)
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "LztContest--alreadyParticipating")))
            print(f'{Fore.GREEN}{dt.datetime.now()} | {Fore.LIGHTCYAN_EX}Успешно приняли участие // {Fore.LIGHTBLUE_EX}{lolz_link}/{i}')
            contests_count += 1
            time.sleep(2)
        except Exception as e:
            continue
            
while True:
    try:
        update_contests_threads()
        solver_contests()
        print(f"{Fore.GREEN}{dt.datetime.now()} | {Fore.LIGHTRED_EX}Отдыхаем // Принял участие в розыгрышах: {Style.RESET_ALL}{contests_count}")
        lolz_thread.clear()
        time.sleep(13)
    except Exception as e:
        print(f"{Fore.GREEN}{dt.datetime.now()} | {Fore.LIGHTBLACK_EX}Новых розыгрышей не найдено. Повторная проверка через {Fore.LIGHTWHITE_EX}2 {Fore.LIGHTBLACK_EX}минуты.")
        time.sleep(120)

