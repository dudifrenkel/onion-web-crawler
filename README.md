# onion-web-crawler

Dockerfile to download and compile tor software for crawling onion websites using Python 3

# To build using the Dockerfile

<code>$ git clone https://github.com/dudifrenkel/onion-web-crawler.git</code>

<code>$ cd onion-web-crawler</code>

<code>$ docker build -t onion-wc .</code>


# To pull the image from the Docker repository

<code>$ docker pull zoom182/onion-wc:latest</code>

# To run

<code> docker run -it \<IMAGE ID\> sh </code>
  
# To run tor

<code> docker exec -it \<CONTAINER ID\> sh </code>  
  
<code> cd && tor </code>

# To run the crawler

<code> docker exec -it \<CONTAINER ID\> sh </code

<code> python3 WebCrawler.py </code>

# The data file will be in /StrongholdPaste.json
