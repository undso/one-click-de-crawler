import os
import requests
import time

from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from urllib.parse import urlencode, quote_plus
from pprint import pprint

mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
profile = FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/tmp/home')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', mime_types)
profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
profile.set_preference("pdfjs.disabled", "true")
opts = Options()
opts.headless = True
print("Starte FireFox")
browser = Firefox(firefox_profile=profile, options=opts)

#Setzen der Variablen
oneclickurl = os.environ.get('ONECLICKURL')
clientnumber = os.environ.get('CLIENTNUMBER')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
telegrambotkey = os.environ.get('TELEGRAMBOTKEY')
chatid = os.environ.get('CHATID')

# Startseite
browser.get(oneclickurl)
time.sleep(30)
browser.get_screenshot_as_file("/tmp/1.png")
browser.find_element_by_id('clientnumber').send_keys(clientnumber)
browser.find_element_by_id('username').send_keys(username)
browser.find_element_by_id('password').send_keys(password)

# Seite nach Login
browser.find_element_by_id('password').submit()
time.sleep(30)
browser.get_screenshot_as_file("/tmp/2.png")

# Uebersicht PDFs
browser.find_element_by_class_name('sidebar-icon-container').click()
time.sleep(20)
browser.get_screenshot_as_file("/tmp/3.png")

# Erstes Element der Liste
pdfs = browser.find_elements_by_class_name("bolder")
print("{} PDF gefunden".format("string", len(pdfs)))
output = ""
if len(pdfs) > 0:
    for pdf in pdfs:
        print(pdf.text)
        output = output + pdf.text + "\n"
        payload = {'chat_id': chatid, 'text': output}
        result = urlencode(payload, quote_via=quote_plus)
        r = requests.get("https://api.telegram.org/" + telegrambotkey + "/sendMessage?" + result)
        pprint(r.json())
else:
    print("Keine neuen PDF")

browser.quit()
exit(0)