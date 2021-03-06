import parse
import settings
import utils
from mydb import CrawlerDb

#TODO: [1]Multi tags stroage in db.(mydb.py)
#      [2]Page rank algorithm.(crawler.py)
#      [3]Hashing operation/db design to be modified.(mydb.py)
#      [4]Deal with network exception.(parse.py)

class Crawler:
	def __init__(self):
		self.crawlerdb=CrawlerDb()
		# if check_url(settings.START_URL):# check if the url is available or not
		self.update_url_data(settings.START_URL)
		self.add_rank()
	
	def quit(self):
		"""
		Do something after crawl process.
		In v0.1 it just closes db connection.
		"""
		self.crawlerdb.close()

	def get_url(self):
		"""
		Get an url from data base.
		"""
		#this func determine that the way you crawl websites, depth-first, breadth-first or ohters
		# need database to get url
		return self.crawlerdb.get_url()

	def update_evaluate(self,key_id):
		""" 
		Update rank info for the reason that each time one url got more times,
		then the url should be considerd more important.
		In v0.1 it does nothing.
		"""
		pass
	
	def handle_collision(self):
		"""
		Handle url_hash collision.
		In v0.1 it does nothing.
		"""
		pass

	def update_url_data(self,url):
		"""
		If url is not in db then it is inserted into db,
		Esle reevaluate the weight of the url.
		"""
		# put url to datbase
		url_hash=utils.calc_hash(url)
		key_id=self.crawlerdb.check_db(url,url_hash)
		if key_id==None:
			self.crawlerdb.add_url(url,url_hash)
			# VERY LIKELY to add the next line code:to initlize rank info of url,
			# or we always get only the fitst url in db from get_url() func.
			# self.crawlerfb.add_rank_info()
			if settings.DEBUG_FLAG:
				print 'insert %s, %s in update_url_data' %(url,url_hash)	
			# #IMPROVE(ifkite): use namedtule
			# result_book=parse_page(url)#return tuple
			# ext_result_book=utils.merge_tups(result_book,new_key_id)
			# add_page(ext_result_book)
			# evalu=rank_page()
			# add_evalu(evalu)
		elif key_id>0:
			self.update_evaluate(key_id)#page has been in db
		else:
			self.handle_collision()

	def add_rank(self,rating_info=0,votes_info=0,key_id=1):
		"""
		Calcuate the rank variable and insert rank info into db.
		In v0.1 calcuating process is naive but workable.
		"""
		# write your rank func here
		# calc rank by rating_info and roves_info
		rank=rating_info
		self.crawlerdb.add_rank_info(rank,key_id)

	def add_book_info(self,book_info):
		"""
		Add parsed info into db.
		In v0.1, crawler parse book info.
		"""
		self.crawlerdb.add_book_info(book_info)

	def crawl(self):
		"""
		Crawl the websites.
		Do the following things.
		[0]Get one url from db.
		[1]Parse url and get page.
		[2]Parse info from page and add them into db.
		[3]Fetch urls from page and add them into db.
		"""
		# utils.init_condition()
		run_time,begin=utils.init_condition()
		handle=parse.HandleUrl()
		while not utils.stop_condition(run_time,begin):
			key_id,url=self.get_url()
			page=handle.get_page(url)
			urls=handle.fetch_urls()
			# add_book_data(key_id,page)
			title_info,author_info,isbn_info,tag_info,rating_info,votes_info=handle.parse_book_info()

			self.add_rank(rating_info,votes_info,key_id)
			result_book_info=(title_info,author_info,isbn_info,tag_info)
			final_book_info=utils.merge_tups(result_book_info,(key_id,))
			self.add_book_info(final_book_info)
			for url in urls:
				self.update_url_data(url)
			
			run_time,begin=utils.update_flag(run_time,begin)
		self.quit()

if __name__=='__main__':
	craw_obj=Crawler()
	craw_obj.crawl()