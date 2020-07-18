from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import random


class WebDriver:
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path='./geckodriver')
        self.driver.maximize_window()
        self.action = ActionChains(self.driver)

        self.word = None

    def join_gartic_room(self, room_url):
        self.driver.get(room_url)
        try:
            self.driver.find_element_by_id('nick').send_keys(f'Da20_{random.randint(0, 99)}')
            self.driver.find_element_by_class_name('bt_orange_medium').click()
        except NoSuchElementException:
            print('Invalid Gartic URL')

        wait = WebDriverWait(self.driver, 10)
        try:
            exit_xpath = "/html/body/div/div[3]/div[2]/div[2]/button"
            exit_btn = wait.until(ec.visibility_of_element_located((By.XPATH, exit_xpath)))

            self.driver.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[1]').click()
        except NoSuchElementException:
            pass

    def play(self):
        buttons_xpath = '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]'
        try:
            message = self.driver.find_element_by_xpath(buttons_xpath + '/div[2]')
            if message.text == 'SUA VEZ':
                self.word = self.driver.find_element_by_xpath(buttons_xpath + '/div[3]').text
                self.driver.find_element_by_id('desenhar').click()
                self.draw()

        except NoSuchElementException:
            pass

        except WebDriverException:
            exit()

    def draw(self):
        print(self.word)
