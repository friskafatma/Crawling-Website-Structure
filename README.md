## Crawling Structure Website



Friska Fatmawatiningrum (160411100084)



Target website : https://thegorbalsla.com/

Program yang dibutuhkan : Python 3.6 (dengan library requests, beautifulsoup4, networkx, matplotlib)



**Step :**

1. #### Crawling link

   ​	dIgunakan untuk mengambil data dari sebuah website. Dan kali ini akan mengambil data berupa link. Dengan meng-import library BeautifulSoup4 terlebih dahulu.



   ```
   import requests
   from bs4 import BeautifulSoup
   import networkx as nx
   import matplotlib.pyplot as plt
   ```



   ```
   def simplifiedURL(url):
       
       if "www." in url: #untuk mengecek www
           ind = url.index("www.")+4
           url = url[ind:]
       if not "http" in url: #untuk mengecek http/https
           url = "http://"+url
       if url[-1] == "/": #untuk garing penutup link
           url = url[:-1]
       return url
   ```

   Fungsi diatas digunakan untuk menyamakan format url, agar tidak ada url yang sama.  apabila depan link nya menggunakan www atau http namun isi webnya sama. Misal https://thegorbalsla.com/ akan dianggap berbeda dengan thegorbalsia.com.



   ```
   def getAllLinks(src):
   
   	#mencegah error apabila link yang terdapat di html nya tidak berfungsi
       try:
       	#mengambil halaman html
           ind = src.find(':')+3
           url = src[ind:]
           page = requests.get(src)
           
           #mengubah html ke object dengan beautiful soup
           soup = BeautifulSoup(page.content, 'html.parser')
           #mengambil semua tag <a> yang berada di html karena link di simpan di dalam tag <a>
           tags = soup.findAll("a")
   
           links = []
           for tag in tags:
           #mencegah error apabila link tidak memiliki href
               try:
                   link = tag['href']
                   if not link in links and 'http' in link:
                   #memasukkan link yang didapat didalam list
                       links.append(link)
               except KeyError:
                   pass
           return links
       except:
           return list()
   ```

   Fungsi diatas digunakan untuk mendapatkan semua link dalam html website yang akan di crawl.



   ```
   def crawl(url, max_deep,  show=False, deep=0):
   	#menampung hasil return
       global edgelist
       
       #mengambil fungsi simplifiedURL(url) disimpan di var url
       url = simplifiedURL(url)
       
       #mengambil fungsi getAllLinks(url) disimpan di var links
       links = getAllLinks(url)
       
       #iterasi kedalaman crawl
       deep += 1
       
       if show:
           if deep == 1:
               print("(%d)%s" %(len(links),url))
           else:
               print("|", end="")
               for i in range(deep-1): print("--", end="")
               print("(%d)%s" %(len(links),url))
       
       for link in links:
       	#membentuk format jalan (edge, dari url ke link)
           edge = (url,link)
           
           #apabila edge belum dicatat maka akan di masukkan ke list
           if not edge in edgelist:
               edgelist.append(edge)
               
           #cek kedalaman jika belum sampai kedalaman maksimal yang diinginkan maka tidak berhenti
           if (deep != max_deep):
               crawl(link, max_deep, show, deep)
   ```



Fungsi diatas digunakan untuk melakukan crawling berdasarkan 4 parameter. 

***def crawl(url, max_deep,  show=False, deep=0):*** 

 - url : untuk alamat website yang akan di crawling
 - max_deep : untuk maksimal kedalaman crawling
 - show : untuk menampilkan proses crawling, dan saya berikan kondisi boolean false agar tidak ditampilkan.
 - deep : untuk mengecek kedalaman proses crawling.



```
root = "https://thegorbalsla.com/"
nodelist = [root]
done = [root]
edgelist = []
```

code diatas digunakan mengisikan url link yang dituju dalam variabel root dan membuat list edgelist untuk menyimpan jalan atau edge.



```
tampilkan = True
crawl(root, 3, show=tampilkan)
if tampilkan:
    for i in range(10): print("")
```

mengisi value untuk fungsi crawl dengan kondisi booleannya true.



2. #### Membuat Graph

```
g = nx.Graph()
#mengubah graph menjadi graph berarah
g = g.to_directed()

#memasukkan yang ada di list ke dalam graph
g.add_edges_from(edgelist)

#mendeklarasikan koordinat graph
pos = nx.spring_layout(g)

#menghitung pagerank
pr = nx.pagerank(g)

#membuat label dan meng-print hasil pagerank
print("keterangan node:")
nodelist = g.nodes
label= {}
for i, key in enumerate(nodelist):
    label[key]=i
    print(i, key, pr[key])

plt.title('Graph Koordinat')
#menggambar graph nya
nx.draw(g, pos)
nx.draw_networkx_labels(g, pos, label)

#menampilkan figure (layout/window untuk tampilan graphnya)
plt.axis("off")
plt.show()
```



##### Referensi :

<https://www.geeksforgeeks.org/page-rank-algorithm-implementation/>

<https://networkx.github.io/documentation/latest/_modules/networkx/drawing/layout.html>

