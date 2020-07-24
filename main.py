from gartic_webdriver import WebDriver

# room_url = 'https://gartic.com.br/01496196'
# room_url = 'https://gartic.com.br/01495887'
room_url = 'https://gartic.com.br/03158885'

gartic = WebDriver(driver='chrome')
gartic.join_gartic_room(room_url)
while True:
    gartic.play()
