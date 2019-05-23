# For crawling purpose
import requests
from bs4 import BeautifulSoup

# For Graph purpose
import networkx as nx
import matplotlib.pyplot as plt

def simplifiedURL(url):
    '''
    asumsi: alamat url tidak mengandung http(s) (misalnya "true-http-website.com"
            atau www (misalnya "true-www-website.com")
    '''
    # cek 1 : www
    if "www." in url:
        ind = url.index("www.")+4
        url = url[ind:]
    # cek 2 : http/https
    if not "http" in url:
        url = "http://"+url
    # cek 3 : tanda / di akhir
    if url[-1] == "/":
        url = url[:-1]
    return url

def crawl(url, max_deep,  show=False, deep=0):
    # returnnya ada di edgelist, 
    global edgelist
    
    # menyamakan format url, agar tidak ada url yg dobel
    url = simplifiedURL(url)
    
    # crawl semua link
    links = getAllLinks(url)
    
    # menambah counter kedalaman
    deep += 1

    #menampilkan proses
    if show:
        if deep == 1:
            print("(%d)%s" %(len(links),url))
        else:
            print("|", end="")
            for i in range(deep-1): print("--", end="")
            print("(%d)%s" %(len(links),url))
    
    for link in links:
        # Membentuk format jalan (edge => (dari, ke))
        edge = (url,link)
        # Mengecek jalan, apabila belum dicatat, maka dimasukkan ke list
        if not edge in edgelist:
            edgelist.append(edge)
        # Cek kedalaman, jika belum sampai terakhir, maka crawling.
        if (deep != max_deep):
            crawl(link, max_deep, show, deep)
			
def getAllLinks(src):
    # Pencegahan eror apabila link yang diambil mati
    try:
        # Get page html
        ind = src.find(':')+3
        url = src[ind:]
        page = requests.get(src)

        # Mengubah html ke object beautiful soup
        soup = BeautifulSoup(page.content, 'html.parser')

        # GET all tag <a>
        tags = soup.findAll("a")

        links = []
        for tag in tags:
            # Pencegahan eror apabila link tidak memiliki href
            try:
                # Get all link
                link = tag['href']
                if not link in links and 'http' in link:
                    links.append(link)
            except KeyError:
                pass
        return links
    except:
        #print("Error 404 : Page "+src+" not found")
        return list()

# Inisialisasi variabel awal
#root = "https://thegorbalsla.com/"
root = "https://www.safiindonesia.com/"
nodelist = [root]
done = [root]
edgelist = []
#crawl
tampilkan = True
crawl(root, 3, show=tampilkan)
if tampilkan:
    for i in range(10): print("")

#membuat Graph
g = nx.Graph()
#mengubah graph menjadi graph berarah
g = g.to_directed()

# Masukin ke Graph
g.add_edges_from(edgelist)

# deklarasi pos (koordinat) (otomatis)
pos = nx.spring_layout(g)

# hitung pagerank
pr = nx.pagerank(g)

# Membuat Label && print pagerank
print("keterangan node:")
nodelist = g.nodes
label= {}
for i, key in enumerate(nodelist):
    label[key]=i
    print(i, key, pr[key])

# Draw Graph
#plt.figure(1)
plt.title('Graph Koordinat')
nx.draw(g, pos)
nx.draw_networkx_labels(g, pos, label)

# show figure
plt.axis("off")
plt.show()
