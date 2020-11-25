import pyautogui
from time import sleep
from PIL import ImageEnhance, Image
import re

sleep(5)
print('executing scraping')
for i in range(57):
    title = 'knowledge_is_power{0}.png'.format(i+62)
    img = pyautogui.screenshot(title, region=(2564, 78, 3329-2564, 1069-78))
    print('Successfully Screenshotted page {0}'.format(i))
    pyautogui.press('down')

    # data = data.convert('L')
    # data = ImageEnhance.Contrast(data)


# Point(x=2564, y=78)
# Point (x=3329, y=1069)

# Point(x=941, y=739)