import json

from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException

from config import USER_DIR


def scrape_cookie():
    """
    通过selenium保存cookie至pixiv_cookie
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('user-data-dir=' + USER_DIR)

    try:
        driver = webdriver.Chrome(chrome_options=chrome_options)
    except InvalidArgumentException as e:
        exit()
    else:
        driver.get("https://www.pixiv.net")
        cookies = driver.get_cookies()
        driver.quit()

        with open("pixiv_cookie", "w") as f:
            json.dump(cookies, f)


def get_cookie() -> RequestsCookieJar:
    """
    读取pixiv_cookie并返回CookieJar\n
    :return: CookieJar
    """
    with open("pixiv_cookie", "r", encoding="utf8") as fp:
        cookies = json.load(fp)
        cookie_jar = RequestsCookieJar()
        for cookie in cookies:
            cookie_jar.set(cookie['name'], cookie['value'])
    return cookie_jar


if __name__ == '__main__':
    scrape_cookie()
