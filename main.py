from bs4 import BeautifulSoup
from couchpotato.core.helpers.encoding import tryUrlencode
from couchpotato.core.helpers.variable import tryInt
from couchpotato.core.logger import CPLog
from couchpotato.core.providers.torrent.base import TorrentProvider
import traceback
import cookielib
import json
import logging
import re
import time
import traceback
import urllib2
import xml.etree.ElementTree as XMLTree

log = CPLog(__name__)


class NxtGn(TorrentProvider):

	urls = {
		'test' : 'http://nxtgn.org/',
		'login' : 'http://nxtgn.org/takelogin.php?csrf=',
		'login_page' : 'http://nxtgn.org/login.php',
		'detail' : 'http://nxtgn.org/details.php?id=%s',
		'search' : 'http://nxtgn.org/browse.php?search=%s&cat=%d',
		'download' : 'http://nxtgn.org/download.php?id=%s',
	}
	
	cat_ids = [
		([9], ['720p', '1080p']),
		([38], ['720p', '1080p']),
		([17], ['dvdr']),
		([6], ['dvdr']),
		([25], ['dvdr']),
		([28], ['dvdr']),
		([5], ['cam', 'ts', 'dvdrip', 'tc', 'r5', 'scr', 'brrip']),
	]
	
	http_time_between_calls = 1 #seconds
	cat_backup_id = None
	login_opener = None
	last_login_check = 0
	
	def _searchOnTitle(self, title, movie, quality, results):
	
		url = self.urls['search'] % (tryUrlencode('%s %s' % (title.replace(':', ''), movie['library']['year'])), self.getCatId(quality['identifier'])[0])
		data = self.getHTMLData(url, opener = self.login_opener)
		
		if data:
			html = BeautifulSoup(data)
			try:
				result_table = html.find('table', attrs = {'class' : 'torrents'})
				if not result_table:
					return
				entries = result_table.find_all('tr')
				
				for result in entries[1:]:
					torrent_id = result.find_all('td')[3].find('a')['href'].replace('download.php?id=', '')
					torrent_title = result.find_all('td')[1].find('a')['title']
					
					torrent_title = torrent_title.replace('EXTENDED.CUT.','')
					torrent_title = torrent_title.replace('UNRATED.CUT.','')
					torrent_title = torrent_title.replace('THEATRICAL.CUT.','')
					torrent_title = torrent_title.replace('EXTENDED.','')
					torrent_title = torrent_title.replace('UNRATED.','')
					torrent_title = torrent_title.replace('THEATRICAL.','')
					torrent_title = torrent_title.replace('Extended.Cut.','')
					torrent_title = torrent_title.replace('Unrated.Cut.','')
					torrent_title = torrent_title.replace('Theatrical.Cut.','')
					torrent_title = torrent_title.replace('Extended.','')
					torrent_title = torrent_title.replace('Unrated.','')
					torrent_title = torrent_title.replace('Theatrical.','')
					
					torrent_size = self.parseSize(result.find_all('td')[8].contents[0])
					
					results.append({
						'id': torrent_id,
						'name': torrent_title,
						'url': self.urls['download'] % torrent_id,
						'detail_url': self.urls['detail'] % torrent_id,
						'size': torrent_size,
					})
			
			except:
				log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))
				
	def getLoginParams(self):
		return tryUrlencode({
			'username': self.conf('username'),
			'password': self.conf('password'),
		})

	def login(self):
	
		# Check if we are still logged in every hour
		now = time.time()
		if self.login_opener and self.last_login_check < (now - 3600):
			try:
				output = self.urlopen(self.urls['login_check'], opener = self.login_opener)
				if self.loginCheckSuccess(output):
					self.last_login_check = now
					return True
				else:
					self.login_opener = None
			except:
				self.login_opener = None

		if self.login_opener:
			return True

		try:
			cookiejar = cookielib.CookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
			data_login = self.getHTMLData(self.urls['login_page'])
			bs = BeautifulSoup(data_login)
			csrfraw = bs.find('form', attrs = {'name': 'loginbox'})['action']
			self.urls['login'] = 'https://nxtgn.org/' + csrfraw
			output = self.urlopen(self.urls['login'], params = self.getLoginParams(), opener = opener)
			
			if self.loginSuccess(output):
				self.last_login_check = now
				self.login_opener = opener
				return True
			
			error = 'unknown'
		except:
			error = traceback.format_exc()

		self.login_opener = None
		log.error('Failed to login %s: %s', (self.getName(), error))
		return False

	def loginSuccess(self, output):
		return 'Login fejl!' not in output
