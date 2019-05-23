import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt

def simplifiedURL(url):
    
    if "www." in url:
        ind = url.index("www.")+4
        url = url[ind:]
    if not "http" in url:
        url = "http://"+url
    if url[-1] == "/":
        url = url[:-1]
    return url

def crawl(url, max_deep,  show=False, deep=0):
    global edgelist
    url = simplifiedURL(url)
    links = getAllLinks(url)

    deep += 1
    if show:
        if deep == 1:
            print("(%d)%s" %(len(links),url))
        else:
            print("|", end="")
            for i in range(deep-1): print("--", end="")
            print("(%d)%s" %(len(links),url))
    
    for link in links:
        edge = (url,link)
        if not edge in edgelist:
            edgelist.append(edge)
        if (deep != max_deep):
            crawl(link, max_deep, show, deep)
			
def getAllLinks(src):
    try:
        ind = src.find(':')+3
        url = src[ind:]
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
    

root = "https://thegorbalsla.com/"
nodelist = [root]
done = [root]
edgelist = []

tampilkan = True
crawl(root, 3, show=tampilkan)
if tampilkan:
    for i in range(10): print("")

#membuat Graph
g = nx.Graph()
g = g.to_directed()
g.add_edges_from(edgelist)
pos = nx.spring_layout(g)
pr = nx.pagerank(g)

print("keterangan node:")
nodelist = g.nodes
label= {}
for i, key in enumerate(nodelist):
    label[key]=i
    print(i, key, pr[key])

plt.title('Graph Koordinat')
nx.draw(g, pos)
nx.draw_networkx_labels(g, pos, label)

plt.axis("off")
plt.show()
