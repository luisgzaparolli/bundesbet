from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from src.params import Params


def get_links():
    """
    Get links of all games in season of bundesliga in foxsports site
    :return: list with links of games in site
    """
    # make a driver to create a section were we going to work, and get the source of page
    driver = webdriver.Chrome(executable_path=Params.path_crome)
    driver.get('https://www.foxsports.com./soccer/schedule?competition=4&season=2019&round=1&week=0&group=0&sequence=1')
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="wisfoxbox"]/section[3]/div[1]/div/div[1]/div[2]/a')))
    html = driver.page_source
    # read the page source with BeautifulSoup, and make a lista with all links game
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('td', {'class': 'wisbb_gameInfo'})
    # with list comprehension select only the games have ended
    links = ['https://www.foxsports.com' + item.find('a')['href'] for item in urls if
             item.find('span', {'class': 'wisbb_status'}).text == 'FINAL']
    # end a driver and return a list with links
    driver.quit()
    return links
