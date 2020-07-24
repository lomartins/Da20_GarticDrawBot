from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import random
import time

from image_handle import load_image


color_btn = {'0,0,0': '//*[@id="cores"]/div[1]',
             '102,102,102': '//*[@id="cores"]/div[2]',
             '0,0,255': '//*[@id="cores"]/div[3]',
             '255,255,255': '//*[@id="cores"]/div[4]',
             '170,170,170': '//*[@id="cores"]/div[5]',
             '0,255,255': '//*[@id="cores"]/div[6]',
             '0,140,0': '//*[@id="cores"]/div[7]',
             '140,0,0': '//*[@id="cores"]/div[8]',
             '140,69,0': '//*[@id="cores"]/div[9]',
             '0,255,0': '//*[@id="cores"]/div[10]',
             '255,0,0': '//*[@id="cores"]/div[11]',
             '255,127,0': '//*[@id="cores"]/div[12]',
             '140,105,0': '//*[@id="cores"]/div[13]',
             '141,2,80': '//*[@id="cores"]/div[14]',
             '141,105,103': '//*[@id="cores"]/div[15]',
             '255,255,0': '//*[@id="cores"]/div[16]',
             '255,0,147': '//*[@id="cores"]/div[17]',
             '255,193,191': '//*[@id="cores"]/div[18]'}


def set_range(driver, el,):
    ac = ActionChains(driver)
    ac.move_to_element(el)
    ac.click_and_hold()
    ac.move_by_offset(0, 50)
    ac.release()
    ac.perform()


def _get_start_offset(canvas):
    x = -(canvas.size['width'] // 2) + 50
    y = -(canvas.size['height'] // 2) + 50

    return x, y


class WebDriver:
    def __init__(self, driver='chrome'):
        if driver == 'chrome':
            self.driver = webdriver.Chrome(executable_path='./chromedriver')
        elif driver == 'firefox':
            self.driver = webdriver.Firefox(executable_path='./geckodriver')
        else:
            print('invalid driver')
            exit()

        self.driver.maximize_window()
        self.action = ActionChains(self.driver)

        self.img = None
        self.word = None

        self._msg_xpath = '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]'

    def join_gartic_room(self, room_url):
        self.driver.get(room_url)
        nickname = f'Da20_{random.randint(0, 99)}'
        try:
            self.driver.find_element_by_id('nick').send_keys(nickname)  # input nick
            self.driver.find_element_by_class_name('bt_orange_medium').click()  # play

        except NoSuchElementException:
            print('Invalid Gartic URL')

        wait = WebDriverWait(self.driver, 10)
        try:
            exit_xpath = "/html/body/div/div[3]/div[2]/div[2]/button"
            wait.until(ec.visibility_of_element_located((By.XPATH, exit_xpath)))

            self.driver.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[1]').click()
        except NoSuchElementException:
            pass

        except TimeoutException:
            pass

    def play(self):
        try:
            if self.is_my_turn():
                self.get_word(new_word=True)
                self.get_image()
                self.draw()

        except NoSuchElementException:
            pass

        except WebDriverException:
            print('WebDriverException')
            exit()

    def is_my_turn(self):
        message_one = self.driver.find_element_by_xpath(self._msg_xpath + '/div[2]')
        return message_one.text == 'SUA VEZ'

    def get_word(self, new_word=False):
        # if new_word true return a new word, otherwise just returns the current word.
        if new_word:
            self.word = self.driver.find_element_by_xpath(self._msg_xpath + '/div[3]').text
        return self.word

    def get_image(self):
        # TODO: implement google images search API
        self.img = load_image('flor.png')

    def draw(self):
        driver = self.driver
        self._start_drawing()

        canvas = driver.find_element_by_id('telaCanvas')

        x_start, y_start = _get_start_offset(canvas)

        act = ActionChains(driver)

        act.move_to_element(canvas).perform()
        act.move_by_offset(x_start, y_start).perform()

        img_dict = self._get_image_dictionary()

        for color in img_dict.keys():
            if color not in color_btn.keys() or color == '255,255,255':  # Skip White
                continue

            total_offset = [0, 0]

            self._choose_color(color)

            pixel_list = img_dict[color]

            for pixel in pixel_list:
                x_offset = (pixel[0] - total_offset[0])
                y_offset = (pixel[1] - total_offset[1])

                total_offset[0] += x_offset
                total_offset[1] += y_offset

                act.move_by_offset(x_offset, y_offset)
                act.click()

            act.move_by_offset(-total_offset[0], -total_offset[1])
            act.reset_actions()
            act.perform()

    def _start_drawing(self):
        self.driver.find_element_by_id('desenhar').click()
        time.sleep(3)
        brush_size = self.driver.find_element_by_id('tamanho')
        set_range(self.driver, brush_size)

    def _get_image_dictionary(self):
        return self.img.to_palette_dict()

    def _choose_color(self, color):
        if color in color_btn.keys():
            self.driver.find_element_by_xpath(color_btn[color]).click()