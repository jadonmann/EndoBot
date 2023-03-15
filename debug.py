# from html2image import Html2Image
# hti = Html2Image(custom_flags=["--default-background-color=000000"])

# hti.screenshot(html_str="spelling_bee.html", css_str="spelling_bee.css", save_as='spelling_bee_test.png')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import os

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

abs_path = os.path.abspath("spelling_bee.html")
abs_path_with_header = "file://" + abs_path

driver.get(abs_path_with_header)

driver.set_window_size(width=302, height=290)
driver.get_screenshot_as_file("spelling_bee.png")

driver.quit()