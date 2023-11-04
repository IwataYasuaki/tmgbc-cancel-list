from selenium import webdriver
import time

options = webdriver.ChromeOptions()
driver = webdriver.Remote(
    command_executor="http://selenium:4444/wd/hub",
    options=options,
)

driver.implicitly_wait(10)

url = "https://yoyaku.sports.metro.tokyo.lg.jp/user/view/user/homeIndex.html"
driver.get(url)

time.sleep(3)
print(driver.title)
driver.quit()
