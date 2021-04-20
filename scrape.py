import requests
import urllib.request
from bs4 import BeautifulSoup #https://crummy.com/software/BeautifukSoup/bs4/doc/
import json
from urllib.parse import urlparse
import os
import json
import base64


#http://filetrance.tander.ru/ef73eb2889668cf2adfa2b9fa58751fc


class PublicWP():
	"""
	Генерация паролей, скрипт запроса
	https://stackoverflow.com/questions/41532738/publish-wordpress-post-with-python-requests-and-rest-api
	"""
	def __init__(self, data, **kargs):
		self.user = data['user']
		self.pwd = data['pwd']  # pwd in plugin "Application Password" https://wordpress.org/plugins/application-passwords/
		self.url = data['url']
	def set_url(self, url): #URL Blog https://exemple.ru/
		self.url = url
	def set_auth(self):
		self.auth = str(base64.b64encode('{user}:{passwd}'.format(user=self.user, passwd=self.pwd).encode()), 'utf-8')
	def set_headers(self):
		self.set_auth()
		self.headers = {
				'Content-Type': 'application/json',
				'Authorization': 'Basic '+self.auth,
				'Username': 'admin',
				'Password':self.auth,
				}

	def create_post(self, data):
		"""
		CREATE_POST
		"""
		self.data=data
		self.set_headers()
		data = requests.post("{url}wp-json/wp/v2/posts/".format(url=self.url), data=json.dumps(self.data), headers=self.headers)
		self.last_post = json.loads(data.text)
		return self.last_post


	def remove_post(self,id_post):
		"""
		REMOVE POST
		"""
		self.set_headers()
		print("{url}wp-json/wp/v2/posts/{id_post}".format(url=self.url, id_post=id_post))
		data = requests.post("{url}/wp-json/wp/v2/posts/{id_post}?_method=DELETE".format(url=self.url, id_post=id_post), headers=self.headers)
		print(json.loads(data.text))


	def load_media(self, img, data={}):
		"""
		LOAD IMAGE in MediaLib in WP
		"""
		self.set_headers()
		self.headers['Content-Type']=None
		media = {
			'file': img,
		}
		resp = requests.post("{url}wp-json/wp/v2/media/".format(url=self.url), headers=self.headers, data=data, files=media)
		#for key, val in json.loads(resp.text).items(): print(key, ' ==> ', val)
		self.last_img = json.loads(resp.text)
		return self.last_img









"""
PARSE SITE
"""


class ScrapeSite():
	def __init__(self, headers={}, **kargs):
		"""
		pass adress site in karg by name url
		self.url - host adress
		self.headers - browser headers

		"""
		self.url = kargs['url']
		self.host = '%s://%s' % ( urlparse(self.url).scheme, urlparse(self.url).netloc )
		self.page = urlparse(self.url).path
		self.netloc = urlparse(self.url).netloc
		self.headers = headers
		self.api_translate = 'trnsl.1.1.20190830T050137Z.3da1e57d45cf1dfb.7e3aea091eb581c7d0ef4449710e6ae983d8842d'
		self.url_translate='https://translate.yandex.net/api/v1.5/tr.json/translate?key='+self.api_translate

	def rule_page_links(self, **kargs):
		self.container = kargs['container']

	def rule_page(self, **kargs):
		self.rule=kargs['rule']
		pass



	def load_page(self, url=None):
		if url is None : url = self.url
		self.response = requests.get(url, headers=self.headers)
		self.soup = BeautifulSoup(self.response.text, "html.parser")
		return self.soup

	def get_links(self, rule = 'links'):
		add_atr = { 'class': self.rule[rule]['class'] }
		self.links=[]
		try:
			for links in self.soup.findAll( self.rule[rule]['container'], add_atr ):
				if self.host in links.find('a').get('href'): #Check URL path
					self.links.append(links.find('a').get('href'))
				else:
					self.links.append(self.host+links.find('a').get('href'))
		except: pass

	def get_objects(self, html_obj):
		self.obj = {}

		for obj in html_obj:
			self.obj[obj] = self.soup.findAll(obj)
	def get_title(self, inner=True):
		try:
			self.title = self.soup.find(self.rule['title']['tag'], {'class':self.rule['title']['class']})
			if inner: self.title = self.title.get_text()
		except AttributeError:
			self.title='None'

	def get_page(self, rule=None):
		"""
		Получаем текст переданного блока страницы.
		stripped - удаляет символы форматирования
		obj - предаем объект обработки, по умолчанию self.page
		Результат присваивается в переменной self.text
		"""

		if rule==None:
			self.page = self.soup.find(self.rule['page']['tag'], {'class':self.rule['page']['class']})
		else:
			self.page = self.soup.find(rule['tag'], {'class':rule['class']})





	def remove_attr(self, soup):

		self.REMOVE_ATTRIBUTES = [
			'lang','language','onmouseover','onmouseout','script','style','font',
			'dir','face','size','color','style','class','width','height','hspace',
			'border','valign','align','background','bgcolor','text','link','vlink',
			'alink','cellpadding','cellspacing', 'id', 'href', 'title', 'aria-label']
		for attribute in self.REMOVE_ATTRIBUTES:
			for tag in soup.find_all(attrs={attribute: True}):
				del tag[attribute]
		return soup.prettify()



	def replase_tag(self, content, tag_from, tag_to):
		"""replase html tags"""
		try:
			for t in content.findAll(tag_from):
				t.name = tag_to
		except: pass
		return content



	def get_clean_html(self, content):
		"""
		Get clear html? whith out tag's attr, tag img, etc.

		"""
		content = self.replase_tag(content, 'a', 'span')
		self.clean_html = self.remove_attr(content)
		return self.clean_html



	def get_list_text(self, stripped=False, obj=None, with_tags = False):
		self.list_text = []
		if obj == None: page = self.page
		else: page = obj

		try:
			if stripped: # if delete special html symbols
				for string in page.stripped_strings:
					if string != None:
						self.list_text.append(string)
			else:
				for string in page.strings:
					if string.string != None:
						if with_tags: self.list_text.append(string)
						else: self.list_text.append(string.string)
		except AttributeError: self.list_text.append('None')




	def get_translate(self, lang_translate='en-ru', text=None, separate='\n', api='google'):
		self.lang_translate = lang_translate
		try:
			if text == None: text = self.title+"~~"+separate.join(self.list_text)
		except: text = "Not text"

		if api =='yandex':
                    #Determinate translate text:
                    url = self.url_translate + '&lang='+self.lang_translate+'&text='+text
                    translate_page=self.load_page(url=url)
                    res = json.loads(str(translate_page))
                    self.translate_text = res['text'][0]
		else:
                    from googletrans import Translator
                    translator = Translator()
                    a=translator.translate(text, src='en', dest='ru')
                    self.translate_text=a.text

		try:
                    self.translate_title = self.translate_text.split("~~")[0]
                    self.translate_content = self.translate_text.split("~~")[1].split(separate)
		except: pass







	def get_full_link(self, link):
		"""
		Determinate full link to object
		"""
		if not self.host in link: full_link = self.host+link
		return full_link

	def get_attr(self,obj, attr):
		try:
			return obj[attr]
		except:
			return None


	def get_images(self, content=None, rule='images'):
		page = self.page
		if content != None: page = content
		self.images = []

		for img in page.findAll(self.rule[rule]['tag']): #<img ..>  img - TAG
			self.images.append(
				{
					'name':self.get_file_name(img[self.rule[rule]['container']]).split('.')[0],
					'alt': self.get_attr(img, 'alt'),
					'title': self.get_attr(img, 'title'),
					'file_name':self.get_file_name(img[self.rule[rule]['container']]),# <img SRC='.......'> src- container
					'link':self.get_full_link(img[self.rule[rule]['container']]), #link to object
					#'file':self.get_file(self.get_full_link(img[self.rule[rule]['container']])), #File objects
				}

			)

	def get_file_name(self, url):
		file_name = url.split("/")[-1]
		return file_name


	def download_images(self, save='', urls = None):
		if urls == None: urls = self.images

		try:
                    os.makedirs(save)
		except FileExistsError:
                    pass# directory already exists

		for url in urls:
			if not self.host in url: url=self.host+url
			name=url.split('/')[-1]

			with open(save+name, 'wb') as handle:
				response = requests.get(url, stream=True)

				if not response.ok:
					print(response)

				for block in response.iter_content(1024):
					if not block:
						break
					handle.write(block)

				print(name,"-Ok")



	def get_file(self, url):
		with open(self.get_file_name(url), 'wb') as handler:
			response = requests.get(url, stream=True)

			if not response.ok:
				print(response)

			for block in response.iter_content(1024):
				if not block:
					break
				handler.write(block)
		file = open(self.get_file_name(url), 'rb')
		os.remove(self.get_file_name(url))
		return file

	def test(self):
		#print('Url: ' + self.url)
		#print('Host: ' + self.host)
		#print('Host: ' + self.netloc)
		#rint('Page: ' + self.page)
		#print('Headers: ' + str(self.headers))
		#print('Container links: ' + self.rule['links']['container'])
		#print('Class container links: ' + self.rule['links']['class'])
		#print('Links: ' + str(self.links))
		#print(self.obj)

		# for CIAN

		rule = {
			'links':{
				'container':'td',
				'class':'catalog__cell'
			},
			'title':{
				'tag':'a',
				'class':'catalog__cell-content'
			},
			'page':{
				'tag':'div',
				'class': 'catalog__table-container',
			}
		}
		self.rule_page( rule = rule )
		self.load_page()
		self.get_links()






if __name__ == '__main__':
	Scrape = ScrapeSite(
		#url='https://www.swiftdirectblinds.co.uk/blog/',
		url = 'https://budgetblinds.com/search-results/?q=blind&p=1',
		headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/2010010 Firefox/45.0'
		}
	)

	#Создаем правила парсинга для страницы
	rule_links = {
			'links':{
				'container': 'h2',
				'class': 'search-result__title',
			},
			'title':{
				'tag':'h1',
				'class':'blog__title',
			},
			'page':{
				'tag':'section',
				'class':'blog-main'
			},

			'images':{
				'tag':'img',
				'container':'data-src'
			},
		}
	#Передаем правила классу
	Scrape.rule_page( rule = rule_links )


	Scrape.load_page() #Загружаем страницу, указанную при инициализации класса
	Scrape.get_links() #Получаем все ссылки на страниц
	print(Scrape.links)


	#for link in Scrape.links:

	#Производим перебор страниц, по полученным ссылкам
	for num, link in enumerate(Scrape.links):
		Scrape.load_page(link)

		#Парсим заголовок
		#Scrape.get_title()
		#print(Scrape.title)

		#Получаем содержимое контента страницы, сохраняем результат в переменную self.page
		Scrape.get_page()
		print(Scrape.page)
		#Парсим содержимое контета



		#Scrape.get_list_text(stripped=False, with_tags = True)
		#Получаем текст из контента, сформированным блоком get_page()
		#print(Scrape.list_text)
		#### ПОЧИСТИТЬ АТРИБУТЫ ТЕГОВ

		#['text ...', 'text2....']



		#Scrape.get_images()
		#for im in Scrape.images: print(im) ## LIST IMAGES


		#Downlods img, save in dir
		#Scrape.download_images(save='/home/l/lleonidd/wspacepy3/public_html/uploads/'+Scrape.netloc+'/images/')



		#Переводим текст lang_translate='en-ru', text=None, 'separate'='\n' - разделитель элементов списка
		#Scrape.get_translate(separate='|\n')
		#Scrape.get_translate(separate='|\n')

		#print(Scrape.translate_title)
		#print(Scrape.translate_content)


		#print(Scrape.title)
		#print(Scrape.list_text)
		#print(Scrape.images)







		## Публикация в WP#########
		"""
		data = {
			'url': 'https://zhaluzi-v-krasnodare.ru/',
			'user':'admin',
			'pwd':'mm2f eLry ZrW4 qhb1 Tuik dKrE',
		}
		wp = PublicWP(data)





		#Load IMG in WP Library
		data_img = {
			'title':Scrape.images[0]['title'],
			'alt_text': Scrape.images[0]['alt'],
			'caption': '',
			'description':'',
		}
		load_img = wp.load_media(
			img=Scrape.images[0]['file'],
			data=data_img
		)


		#Public POST
		data_post = {
			'title':Scrape.translate_title,
			'content':"".join(Scrape.translate_content),
			'featured_media':load_img['id'], ## ID image for post
		}
		wp.create_post(data=data_post)
		"""











		if num == 0: break

	#Scrape.test()











	#wp.remove_post('3703')
	#################################
