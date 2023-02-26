import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from bs4.element import Comment
import time
from urllib.parse import urljoin
from googletrans import Translator
import google

# import translators 


# translator = Translator()
def translate_text(target, text):
    import six
    from google.cloud import translate_v2 as translate
    translate_client = translate.Client()
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')
    result = translate_client.translate(text, target_language=target)
    return result
# Start the Selenium WebDriver and navigate to the website

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--remote-debugging-port=9222") 
options.add_argument('--ignore-certificate-errors')
driver_path = '/home/ahmad/bin/chromedriver.exe'

service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service, options=options)

url = "https://www.classcentral.com/"

driver.get(url)

# Wait for any dynamic JavaScript to execute
driver.execute_script("return setTimeout(function() {}, 1000)")

# Get the rendered HTML
html = driver.page_source

# translation = translators.translate_html(html, if_ignore_empty_query=False, translator='iciba', to_language='hi')
# Save the HTML to a file
# with open('index.html', 'w') as f:
#     f.write(translation)

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

element = ['p', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'button', 'li', 'a', 'span']

# for text in soup.find_all(string=True):
#     if text.parent.name in ['style', 'script', 'head', 'title', '[document]'] :
#         continue
#     if isinstance(text, Comment):
#         continue
#     if not text or text == "" or text == "\n":
#         continue
#     print(text)
#     print(text.string)
#     # translation = translator.translate(text, src='es', dest='hi')
#     try:
#         translation = translate_text('hi', text)
#         # translation = translator.translate(text, src='en', dest='hi')
#         # translation = translators.translate_html(text, if_ignore_empty_query=False, from_language='en', to_language='hi')
#     except  IndexError : #translators.server.TranslatorError:
#         continue
#     text.replace_with(translation['translatedText'])
#     print(translation['translatedText'])
#     print(text)

# with open('index.html', 'w', encoding='utf-8') as f:
#     f.write(str(soup))


# Find all JavaScript and CSS resources and download them
for script in soup.find_all('script'):
    if script.has_attr('src') and script['src'].endswith('.js'):
        if script['src'].startswith('//'):
            f_url = 'https:' + script['src']
        elif script['src'].startswith('/'):
            f_url = 'https:/' + script['src']
        try :
            content = requests.get(f_url).text
        except requests.exceptions.ConnectionError:
            pass
        filename = f_url.split('/')[-1] + '.js'
        with open(filename, 'w') as f:
            f.write(content)

for css in soup.find_all('link'):
    if css.has_attr('rel') and css['rel'] == 'stylesheet':
        f_url = 'https:' + css['href']
        content = requests.get(css['href']).text
        filename = f_url.split('/')[-1] + '.css'
        with open(filename, 'w') as f:
            f.write(content)


for link in soup.find_all("a"):
    link_url = link.get("href")
    print(link_url)
    if link.has_attr('href'):
        if not (link_url.startswith("http") or link_url.startswith("https")):
            link_href = urljoin(url, link_url) 
            driver.get(link_href)
            driver.execute_script("return setTimeout(function() {}, 10)")
            html = driver.page_source
            # link_response = requests.get(link_href)
            # link_html_content = link_response.content
            file_name = link_url[1:] + '.html'
            print(file_name)
            if "http://www.facebook.com/sharer.php?u=https%3A%2F%2Fwww.classcentral.com%2F" == file_name:
                continue
            if "mailto:?subject=&body=%20https%3A%2F%2Fwww.classcentral.com%2F" == file_name:
                continue
            done = ['.html', 'rankings.html','subjects.html', 'collections.html', 'subject/business.html', 'subject/cs.html', 'subject/health.html', 'subject/humanities.html', 'subject/maths.html', 'subject/engineering.html', 'subject/science.html', 'subject/education.html', 'subject/social-sciences.html', 'subject/art-and-design.html', 'subject/data-science.html', 'subject/programming-and-software-development.html', 'subject/personal-development.html', 'subject/infosec.html', 'universities.html', 'report/.html', 'collection/top-free-online-courses.html', 'starting-this-month.html', 'collection/ivy-league-moocs.html', 'new-online-courses.html', 'most-popular-courses.html', 'subject/ai.html', 'subject/algorithms-and-data-structures.html', 'subject/information-technology.html', 'subject/internet-of-things.html', 'subject/devops.html', 'subject/education.html', 'subject/machine-learning.html', 'subject/health.html', 'subject/computer-networking.html', 'subject/deep-learning.html', 'subject/cryptography.html', 'subject/hci.html', 'subject/quantum-computing.html', 'subject/distributed-systems.html', 'subject/blockchain.html', 'subject/operating-systems.html', 'subject/computer-graphics.html', 'subject/nutrition-and-wellness.html', 'subject/disease-and-disorders.html', 'subject/public-health.html', 'subject/health-care.html', 'subject/nursing.html', 'subject/anatomy.html', 'subject/cme.html' ]  

            if file_name.startswith('subject/'):
                continue
            if file_name in done :
                continue
            
            link_soup = BeautifulSoup(html, 'html.parser')
            for  text in link_soup.find_all(string=True):
                print(text)
                if text.parent.name in ['style', 'script',  '[document]'] :
                    continue
                if isinstance(text, Comment):
                    continue
                
                if not text or text == "" or text == "\n":
                    continue
                # translation = translator.translate(text, src="en", dest="hi")
                try:
                    translation = translate_text('hi', text)
                    # translation = translator.translate(text, src='en', dest='hi')
                    # translation = translators.translate_html(text, if_ignore_empty_query=False, to_language='hi')
                except  IndexError: #translators.server.TranslatorError:
                    continue
                except google.auth.exceptions.TransportError:
                    continue
                except requests.exceptions.ReadTimeout:
                    continue
                except requests.exceptions.ConnectionError:
                    continue
                text.replace_with(translation['translatedText'])
                print(translation['translatedText'])
                print(text)

            # translation = translators.translate_html(html, translator='iciba', to_language='hi')
            with open(file_name, 'w', encoding='utf-8') as f:
                # f.write(translation)
                f.write(str(link_soup))

            for script in link_soup.find_all('script'):

                if script.has_attr('src') and script['src'].endswith('.js'):
                    if script['src'].startswith('//'):
                        f_url = 'https:' + script['src']
                    elif script['src'].startswith('/'):
                        f_url = 'https:/' + script['src']
                    try :
                        content = requests.get(f_url).text
                    except requests.exceptions.ConnectionError:
                        pass
                    # content = requests.get(f_url).text
                    filename = f_url.split('/')[-1] + '.js'
                    with open(filename, 'w') as f:
                        f.write(content)

            for css in link_soup.find_all('link'):
                if css.has_attr('rel') and css['rel'] == 'stylesheet':
                    f_url = 'https:' + css['href']
                    content = requests.get(css['href']).text
                    filename = f_url.split('/')[-1] + '.css'
                    with open(filename, 'w') as f:
                        f.write(content)


# Quit the WebDriver
time.sleep(3)  # add a delay of 3 seconds

driver.quit()
