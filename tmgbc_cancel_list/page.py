from datetime import date
from selenium import webdriver
from locator import (
    BasePageLocator as BPL,
    HomePageLocator as HPL,
    LoginPageLocator as LPL,
    MyPageLocator as MPL,
    SearchResultPageLocator as SRPL,
    EmptyStatePageLocator as ESPL,
    ConfirmationPageLocator as CMPL,
)
from element import (
    UserIdElement,
    PasswordElement,
)


class BasePage(object):
    """ベースページ"""
    def __init__(self, driver: webdriver.Remote) -> None:
        self.driver = driver

    def find_body(self) -> str:
        locator = BPL.BODY
        return self.driver.find_element(*locator).text


class HomePage(BasePage):
    """ホームページ"""
    def click_login_button(self) -> None:
        locator = HPL.LOGIN_BUTTON
        self.driver.find_element(*locator).click()


class LoginPage(BasePage):
    """ログインページ"""
    user_id = UserIdElement()
    password = PasswordElement()

    def click_login_button(self) -> None:
        locator = LPL.LOGIN_BUTTON
        self.driver.find_element(*locator).click()


class MyPage(BasePage):
    """マイページ"""
    def click_find_by_park_button(self) -> None:
        locator = MPL.FIND_BY_PARK_BUTTON
        self.driver.find_element(*locator).click()


class SearchResultPage(BasePage):
    """検索結果ページ"""
    def find_parks(self) -> list[str]:
        locator = SRPL.PARK
        elements = self.driver.find_elements(*locator)
        return [e.text for e in elements]

    def click_select_button(self, park: str) -> None:
        locator = SRPL.generate_select_button_locator(park)
        self.driver.find_element(*locator).click()


class EmptyStatePage(BasePage):
    """空き状況ページ"""
    def click_calendar(self, target_date: date) -> None:
        d = target_date
        script = f"selectCalendarDate({d.year},{d.month},{d.day});"
        self.driver.execute_script(script)

    def find_sports(self) -> None:
        locator = ESPL.SPORT
        elements = self.driver.find_elements(*locator)
        return [e.text for e in elements]

    def find_timeframes(self, sport: str) -> list[str]:
        locator = ESPL.generate_timeframe_locator(sport)
        elements = self.driver.find_elements(*locator)
        return [e.text for e in elements]

    def find_empty_state(self, sport: str, tframe_i: str) -> str:
        locator = ESPL.generate_empty_state_locator(sport)
        empty_state = self.driver.find_elements(*locator)[tframe_i]
        return empty_state.get_attribute('alt')

    def click_check_box(self, sport: str, tframe_i: str) -> None:
        locator = ESPL.generate_empty_state_locator(sport)
        self.driver.find_elements(*locator)[tframe_i].click()

    def click_reserve_button(self) -> None:
        locator = ESPL.RESERVE_BUTTON
        self.driver.find_element(*locator).click()


class ConfirmationPage(BasePage):
    """予約内容確認ページ"""
    def click_confirm_button(self) -> None:
        locator = CMPL.CONFIRM_BUTTON
        self.driver.find_element(*locator).click()
