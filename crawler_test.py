import requests
from bs4 import BeautifulSoup
import os
os.makedirs("downloads")
website_data = requests.get("https://www.ceec.edu.tw/xmfile?xsmsid=0J052424829869345634")
soup_data = BeautifulSoup(website_data.text,"html.parser")
select_data =  soup_data.select("div.pages a")
pages = select_data[-1]["href"][select_data[-1]["href"].rfind("=")+1:]
for i in range(1,int(pages)+1):
    website_data = requests.get("https://www.ceec.edu.tw/xmfile?xsmsid=0J052424829869345634&page={}".format(i))
    soup_data = BeautifulSoup(website_data.text,"html.parser")
    select_data =  soup_data.select("tr")
    for selection_data in select_data:
        selection = selection_data.select("td.title")
        for subject in selection:
            os.makedirs("downloads\\{}\\{}".format(subject.text[2:subject.text.find("學")],subject.text[2:subject.text.find(" ")]))
        selection = selection_data.select("td.download a")
        for link in selection:
            if link["class"][1]=="file_pdf":
                link_temp = link["href"].split("/")
                link["href"]="https://www.ceec.edu.tw/files/file_pool/1/"+"/".join(link_temp[-2:])
                file = requests.get(link["href"])
                #print(link["href"])
                open("downloads\\{}\\{}\\{}.pdf".format(subject.text[2:subject.text.find("學")],subject.text[2:subject.text.find(" ")],link["title"]),"wb").write(file.content)
                