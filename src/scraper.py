import requests
from bs4 import BeautifulSoup
import subprocess
#getting the parent url 
#of that particular parent url get all the child hrefs
#save all these into the file
URL = "https://elhacker.info/Cursos/DevOps/"
def getHrefs(url):
    targetHref = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        anchor_tags = soup.find_all('a')
        for anchor_tag in anchor_tags:
            href_value = anchor_tag.get('href')
            img_tag = anchor_tag.find('img', {'alt': '[Directorio]'})
            if href_value:
                targetHref.append(href_value)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    return targetHref

def parent():
    
    parentHref = getHrefs(URL)
    child(URL, parentHref[4:])

def child(parentUrl, hrefList):
    # print(parentUrl,hrefList)
    finalUrls = []
    for i in hrefList:  
        newUrl = parentUrl+i
        tempUrls = getHrefs(newUrl)
        # print(tempUrls)
        for j in tempUrls:
            # print(i+j)
            finalUrls.append(URL+i+j+"\n")
    with open("url.txt","w") as f:
        for i in set(finalUrls):
            print(i)
            f.write(i)
if __name__=="__main__":
    parent()
