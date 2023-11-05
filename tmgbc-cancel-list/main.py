from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    presence_of_all_elements_located,
)
from time import sleep
from getpass import getpass
from datetime import date, datetime, timezone, timedelta


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
        sleep(1)  # 一部の要素しか取得できないことがあるため少しスリープ
        park_list = find_labels_by_id(driver, "bnamem")
        _, park = input_from_list(park_list, "公園 (上記から番号を選択): ")
        select_park(driver, park)

        # 利用可能な施設と空き状況画面
        target_date = date.fromisoformat(input("年月日 (yyyymmdd): "))
        select_date(driver, target_date)
        sleep(1)  # 一部の要素しか取得できないことがあるため少しスリープ
        sport_list = find_labels_by_id(driver, "ppsname")
        _, sport = input_from_list(sport_list, "種目 (上記から番号を選択): ")
        tzone_list = find_tzones(driver, sport)
        tzone_index, tzone = input_from_list(tzone_list, "時間帯 (上記から番号を選択): ")

        # 1分おきに空き状況を確認して空いていたら予約する
        while True:
            now = datetime.now(timezone(timedelta(hours=9)))
            today = now.date()
            empty_state = find_status(driver, sport, tzone_index)
            if empty_state == '空き':
                print(f'{now} 空きました')
                reserve(driver, sport, tzone_index)
                if is_complete(driver):
                    print(f'{now} 予約が完了しました: {park}, {target_date}, {tzone}')
                    break
                else:
                    raise RuntimeError('何らかの理由で予約に失敗しました')
            elif target_date <= today:
                print(f'{now} 入力された年月日を迎えました: {target_date}')
                break
            else:
                print(f'{now} 空いていません: {empty_state}')
                sleep(60)
                select_date(driver, target_date)

    finally:
        print('処理を終了します')
        print(driver.find_element(By.TAG_NAME, 'body').text)
        driver.save_screenshot('screenshot.png')
        driver.quit()


def login(driver: webdriver.Remote, userid: str, passwd: str) -> None:
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


def select_date(driver: webdriver.Remote, target_date: date) -> None:
    year = target_date.year
    month = target_date.month
    day = target_date.day
    driver.execute_script(f"selectCalendarDate({year},{month},{day});")


def find_tzones(driver: webdriver.Remote, sport: str) -> list[str]:
    tbody = f'//span[text()="{sport}"]/ancestor::td[@id="blabel"]/../..'
    xpath = f'{tbody}//span[@id="tzoneStimeLabel"]'
    element_list = driver.find_elements(By.XPATH, xpath)
    return [element.text for element in element_list]


def find_status(driver: webdriver.Remote, sport: str, index: int) -> str:
    tbody = f'//span[text()="{sport}"]/ancestor::td[@id="blabel"]/../..'
    xpath = f'{tbody}//img[@id="emptyStateIcon"]'
    return driver.find_elements(By.XPATH, xpath)[index].get_attribute('alt')


def reserve(driver: webdriver.Remote, sport: str, index: int) -> None:
    tbody = f'//span[text()="{sport}"]/ancestor::td[@id="blabel"]/../..'
    xpath = f'{tbody}//img[@id="emptyStateIcon"]'
    driver.find_elements(By.XPATH, xpath)[index].click()
    driver.find_element(By.ID, 'doReserve').click()
    driver.find_element(By.ID, 'apply').click()


def is_complete(driver: webdriver.Remote) -> bool:
    body = driver.find_element(By.TAG_NAME, 'body').text
    return '予約が完了しました' in body


if __name__ == "__main__":
    main()
