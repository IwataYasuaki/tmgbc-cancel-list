from selenium import webdriver
from time import sleep
from getpass import getpass
from datetime import date, datetime, timezone, timedelta
import page


def main():
    """
    これは東京都スポーツ施設サービスのキャンセル待ちをするプログラムです。
    SeleniumでGoogle Chromeを操作し、東京都スポーツ施設サービスの
    Webページへアクセスします。ログイン情報やキャンセル待ちする施設や
    時間帯は、コンソールでユーザーに入力してもらいます。空き状況ページ
    まで行ったら、1分おきに空き状況を確認して空いていたら予約します。
    """
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions(),
    )
    driver.implicitly_wait(10)
    base_url = "https://yoyaku.sports.metro.tokyo.lg.jp"

    try:
        driver.get(f'{base_url}/user/view/user/homeIndex.html')

        home_page = page.HomePage(driver)
        home_page.click_login_button()

        login_page = page.LoginPage(driver)
        login_page.user_id = input("ユーザーID (登録番号): ")
        login_page.password = getpass("パスワード: ")
        login_page.click_login_button()

        my_page = page.MyPage(driver)
        my_page.click_find_by_park_button()

        sleep(1)  # 一部の要素しか取得できないことがあるため少しスリープ
        search_result_page = page.SearchResultPage(driver)
        parks = search_result_page.find_parks()
        _, park = input_from_list(parks, "公園 (上記から番号を選択): ")
        search_result_page.click_select_button(park)

        empty_state_page = page.EmptyStatePage(driver)
        target_date = date.fromisoformat(input("年月日 (yyyymmdd): "))
        empty_state_page.click_calendar(target_date)
        sleep(1)  # 一部の要素しか取得できないことがあるため少しスリープ
        sports = empty_state_page.find_sports()
        _, sport = input_from_list(sports, "種目 (上記から番号を選択): ")
        tframe = empty_state_page.find_timeframes(sport)
        tframe_i, tframe = input_from_list(tframe, "時間帯 (上記から番号を選択): ")

        # 1分おきに空き状況を確認して空いていたら予約する
        while True:
            now_ = datetime.now(timezone(timedelta(hours=9)))
            today_ = now_.date()
            empty_state = empty_state_page.find_empty_state(sport, tframe_i)
            if empty_state == '空き':
                print(f'{now_} 空きました')
                empty_state_page.click_check_box(sport, tframe_i)
                empty_state_page.click_reserve_button()
                confirmation_page = page.ConfirmationPage(driver)
                confirmation_page.click_confirm_button()
                current_page = page.BasePage(driver)
                if '予約が完了しました' in current_page.find_body():
                    print(f'{now_} 予約が完了しました: {park}, {target_date}, {tframe}')
                    break
                else:
                    raise RuntimeError('何らかの理由で予約に失敗しました')
            elif target_date <= today_:
                print(f'{now_} 入力された年月日を迎えました: {target_date}')
                break
            else:
                print(f'{now_} 空いていません: {empty_state}')
                sleep(60)
                empty_state_page.click_calendar(target_date)

    finally:
        print('処理を終了します')
        current_page = page.BasePage(driver)
        print(current_page.find_body())
        driver.save_screenshot('screenshot.png')
        driver.quit()


def input_from_list(list_: list[str], prompt: str) -> tuple[int, str]:
    print()
    for i, v in enumerate(list_):
        print(f"{i}: {v}")
    print()
    index = int(input(prompt))
    return index, list_[index]


if __name__ == "__main__":
    main()
