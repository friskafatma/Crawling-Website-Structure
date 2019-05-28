import pandas as pd
import requests
from bs4 import BeautifulSoup


import networkx as nx
import matplotlib.pyplot as plt

def simplifiedURL(url):
    if "www." in url:
        ind = url.index("www.")+4
        url = "http://"+url[ind:]
    if url[-1] == "/":
        url = url[:-1]
    parts = url.split("/")
    url = ''
    for i in range(3):
        url += parts[i] + "/"
    return url

def crawl(url, max_deep,  show=False, deep=0, done=[]):
    global edgelist

    deep += 1
    url = simplifiedURL(url)


    if not url in done:

        links = getAllLinks(url)
        done.append(url)
        if show:
            if deep == 1:
                print(url)
            else:
                print("|", end="")
                for i in range(deep-1): print("--", end="")
                print("(%d)%s" %(len(links),url))
            
        for link in links:
            link = simplifiedURL(link)
            edge = (url,link)
            if not edge in edgelist:
                edgelist.append(edge)
            if (deep != max_deep):
                crawl(link, max_deep, show, deep, done)
			
def getAllLinks(src):
    try:
        page = requests.get(src)
        soup = BeautifulSoup(page.content, 'html.parser')

        tags = soup.findAll("a")

        links = []
        for tag in tags:
            try:
                link = tag['href']
                if not link in links and 'http' in link:
                    links.append(link)
            except KeyError:
                pass
        return links
    except:
        return list()


root = "https://www.safiindonesia.com/"
nodelist = [root]
edgelist = []

#crawl
crawl(root, 3, show=True)
edgelistFrame = pd.DataFrame(edgelist, None, ("From", "To"))

#membuat Graph
g = nx.from_pandas_edgelist(edgelistFrame, "From", "To", None, nx.DiGraph())

# deklarasi pos (koordinat) (otomatis)
pos = nx.spring_layout(g)

# hitung pagerank
damping = 0.85
max_iterr = 100
error_toleransi = 0.0001
pr = nx.pagerank(g, alpha = damping, max_iter=max_iterr, tol=error_toleransi)

# Membuat Label && print pagerank
print("keterangan node:")
nodelist = g.nodes
label= {}
data = []
for i, key in enumerate(nodelist):
    data.append((pr[key], key))
    label[key]=i

#Mengurutkan hasil pagerank
urutpr = data.copy()
for x in range(len(urutpr)):
    for y in range(len(urutpr)):
        if urutpr[x][0] > urutpr[y][0]:
            urutpr[x],urutpr[y] = urutpr[y],urutpr[x]
        
urutpr = pd.DataFrame(urutpr, None, ("PageRank", "Node"))
print(urutpr)

# Draw Graph
nx.draw(g, pos)
nx.draw_networkx_labels(g, pos, label, font_color="w")

# show figure
plt.axis("off")
plt.show()
