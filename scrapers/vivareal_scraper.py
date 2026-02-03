import requests
from bs4 import BeautifulSoup
 
url = 'https://www.indeed.com/jobs?q=web+developer&l=New+York'
 
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
 
results = soup.find(id='resultsCol')
if results:
    print(results.prettify())
else:
    print("Error: Element with id='resultsCol' not found. The page structure may have changed.")