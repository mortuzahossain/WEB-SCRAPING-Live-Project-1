from selenium import webdriver
from bs4 import BeautifulSoup
import csv


driver = webdriver.PhantomJS('phantomjs.exe')

def DownloadPageHtml(url):
	print 'Downloading : ' + url
	driver.get(url)
	html = driver.page_source
	return html


start_page = 1
end_page = 3

for x in xrange(start_page,end_page + 1):
	url = 'https://yts.am/browse-movies?page='+ str(x)

	filename = url.split('?')[-1] + '.csv'

	f = open(filename,'a+')
	data = [['post_type','post_status','post_title','post_content','post_category','post_tags','post_thumbnail','download_link']]

	with f:
	    writer = csv.writer(f)
	    writer.writerows(data)

	html = DownloadPageHtml(url)
	soup = BeautifulSoup(html,'lxml')
	allmovie = soup.find('div',class_ = 'browse-content').find_all('div',class_ = 'browse-movie-wrap')

	for movie in allmovie:
		detailurl = DownloadPageHtml(movie.find('a')['href'])
		
		soup = BeautifulSoup(detailurl,'lxml')
		movie_info = soup.find('div',{'id':'movie-info'})
		name = movie_info.find('h1').text.encode('utf-8')
		tag = movie_info.find_all('h2')[0].text.encode('utf-8')
		catagory = movie_info.find_all('h2')[1].text.replace(' / ',',').encode('utf-8')
		download_link = movie_info.find('a')['href'].encode('utf-8')
		image = soup.find('div',{'id':'movie-poster'}).find('img')['src'].encode('utf-8')
		post_content = soup.find('div',{'id':'synopsis'}).find('p').text.encode('utf-8')
		data = [['post','publish',name,post_content,catagory,tag,image,download_link]]
		f = open(filename,'a+')
		with f:
		    writer = csv.writer(f)
		    writer.writerows(data)
		print 'Done : ' + name


print '\n\n Finish'
f.close()
driver.close()