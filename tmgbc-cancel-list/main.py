from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    presence_of_all_elements_located,
)
from time import sleep
from getpass import getpass


def main():
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions(),
    )
    driver.implicitly_wait(10)
    url = "https://yoyaku.sports.metro.tokyo.lg.jp/user/view/user/homeIndex.html"  # noqa

    try:
        # ホーム画面
        driver.get(url)
        driver.find_element(By.ID, "login").click()

        # ログイン画面
        userid = input("ユーザーID (登録番号): ")
        passwd = getpass("パスワード: ")
        login(driver, userid, passwd)

        # マイページ画面
        driver.find_element(By.ID, "nameSearch").click()

        # 検索結果画面
        park_list = find_labels_by_id(driver, "bnamem")
        _, park = input_from_list(park_list, "公園 (上記から番号を選択): ")
        select_park(driver, park)

        # 利用可能な施設と空き状況画面
        date = input("年月日 (yyyymmdd): ")
        select_date(driver, date)
        sport_list = find_labels_by_id(driver, "ppsname")
        _, sport = input_from_list(sport_list, "種目 (上記から番号を選択): ")
        tzone_list = find_tzones(driver, sport)
        tzone_index, _ = input_from_list(tzone_list, "時間帯 (上記から番号を選択): ")

    finally:
        input('終了します')
        driver.quit()


def login(driver: webdriver.Remote, userid: str, passwd: str) -> None:
    sleep(3)  # すぐにログインするとエラーになるためスリープする
    driver.find_element(By.ID, "userid").send_keys(userid)
    driver.find_element(By.ID, "passwd").send_keys(passwd)
    driver.find_element(By.ID, "login").click()


def find_labels_by_id(driver: webdriver.Remote, id_: str) -> list[str]:
    wait = WebDriverWait(driver, 10)
    element_list = wait.until(presence_of_all_elements_located((By.ID, id_)))
    return [element.text for element in element_list]


def select_park(driver: webdriver.Remote, park: str) -> None:
    xpath = f'//span[text()="{park}"]/../following-sibling::td[3]/div/input'
    driver.find_element(By.XPATH, xpath).click()


def input_from_list(list_: list[str], prompt: str = "上記から番号を選択: ") -> str:
    print()
    for i, v in enumerate(list_):
        print(f"{i}: {v}")
    print()
    index = int(input(prompt))
    return index, list_[index]


def select_date(driver: webdriver.Remote, date: str) -> None:
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    driver.execute_script(f"selectCalendarDate({year},{month},{day});")


def find_tzones(driver: webdriver.Remote, sport: str) -> list[str]:
    tbody = f'//span[text()="{sport}"]/ancestor::td[@id="blabel"]/../..'
    xpath = f'{tbody}//span[@id="tzoneStimeLabel"]'
    wait = WebDriverWait(driver, 10)
    locator = presence_of_all_elements_located((By.XPATH, xpath))
    element_list = wait.until(locator)
    return [element.text for element in element_list]


if __name__ == "__main__":
    main()
