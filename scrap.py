import requests
from bs4 import BeautifulSoup

page = requests.get('https://ca.indeed.com/?r=us')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')
print(soup)