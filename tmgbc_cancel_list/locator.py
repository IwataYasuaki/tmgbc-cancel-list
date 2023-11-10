from selenium.webdriver.common.by import By


class BasePageLocator(object):
    """ベースページのロケータ"""
    BODY = (By.TAG_NAME, "body")


class HomePageLocator(object):
    """ホームページのロケータ"""
    LOGIN_BUTTON = (By.ID, "login")


class LoginPageLocator(object):
    """ログインページのロケータ"""
    USER_ID = (By.ID, "userid")
    PASSWORD = (By.ID, "passwd")
    LOGIN_BUTTON = (By.ID, "login")


class MyPageLocator(object):
    """マイページのロケータ"""
    FIND_BY_PARK_BUTTON = (By.ID, "nameSearch")


class SearchResultPageLocator(object):
    """検索結果ページのロケータ"""
    PARK = (By.ID, "bnamem")

    def generate_select_button_locator(park: str) -> str:
        xpath = f'//span[text()="{park}"]/../..//input[@id="srchBtn"]'
        return (By.XPATH, xpath)


class EmptyStatePageLocator(object):
    """空き状況ページのロケータ"""
    SPORT = (By.ID, "ppsname")
    RESERVE_BUTTON = (By.ID, "doReserve")

    def generate_timeframe_locator(sport: str) -> str:
        tbody = f'//span[text()="{sport}"]/ancestor::td[@id="blabel"]/../..'
        xpath = f'{tbody}//span[@id="tzoneStimeLabel"]'
        return (By.XPATH, xpath)

    def generate_empty_state_locator(sport: str) -> str:
        tbody = f'//span[text()="{sport}"]/ancestor::td[@id="blabel"]/../..'
        xpath = f'{tbody}//img[@id="emptyStateIcon"]'
        return (By.XPATH, xpath)


class ConfirmationPageLocator(object):
    """予約内容確認ページのロケータ"""
    CONFIRM_BUTTON = (By.ID, "apply")
