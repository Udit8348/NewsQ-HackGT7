'''from bs4 import BeautifulSoup
import requests
l={}
u=list()
# http://www.ip2country.net/ip2country/country_code.html
country_code = "KZ"
url="https://www.proxynova.com/proxy-server-list/country-"+country_code+"/"
respo = requests.get(url).text
soup = BeautifulSoup(respo,'html.parser')
allproxy = soup.find_all("tr")
for proxy in allproxy:
 foo = proxy.find_all("td")
 try: 
     l["ip"]=foo[0].text.replace("\n","").replace("document.write(","").replace(")","").replace("\’","").replace(";","")
 except:
   l["ip"]=None
 try:
  l["port"]=foo[1].text.replace("\n","").replace(" ","")
 except:
  l["port"]=None
 try:
  l["country"]=foo[5].text.replace("\n","").replace(" ","")
 except:
  l["country"]=None
 if(l["port"] is not None):
  u.append(l)
 
 l={}
print(u)'''

'''
Pool of IP's, each one has 3 properties
IP | port | country
'''

'''import requests
from bs4 import BeautifulSoup
from random import choice

def proxy_generator():
    response = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(response.content, 'html5lib')
    proxy = {'https': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, 
	   soup.findAll('td')[::8]), map(lambda x:x.text, soup.findAll('td')[1::8]))))))}
    return proxy

def data_scraper(request_method, url, **kwargs):
    while True:
        try:
            proxy = proxy_generator()
            print("Proxy currently being used: {}".format(proxy))
            response = requests.request(request_method, url, proxies=proxy, timeout=25.0, **kwargs)
            break
            # if the request is successful, no exception is raised
        except:
            print("Connection error, looking for another proxy")
            pass
    return response

p = data_scraper('GET', "https://apnews.com/article/election-2020-joe-biden-russia-024b553e9a4ffb2716286dd134876f8a")
print(p)'''
