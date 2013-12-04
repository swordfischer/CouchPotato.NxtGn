# credits goes to https://github.com/TjaLfE/cps.nextgen

from bs4 import BeautifulSoup
from couchpotato.core.helpers.encoding import simplifyString, tryUrlencode
from couchpotato.core.helpers.variable import tryInt
from couchpotato.core.logger import CPLog
from couchpotato.core.providers.torrent.base import TorrentProvider
import traceback
import cookielib
import urllib2
import time

log = CPLog(__name__)


class NxtGn(TorrentProvider):

	urls = {
		'test' : 'https://nxtgn.org/',
		'login_page' : 'https://nxtgn.org/login.php',
		'login' : 'https://nxtgn.org/takelogin.php',
		'detail' : 'https://nxtgn.org/details.php?id=%s',
		'search' : 'http://nxtgn.org/browse.php?search=%s&cat=%d',
		'download' : 'https://nxtgn.org/download.php?id=%s',
	}
	
	cat_ids = [
		([9], ['720p', '1080p']),
		([38], ['720p', '1080p']),
		([33], ['720p', '1080p']),
		([43], ['720p', '1080p']),
		([47], ['1080p']),
		([17], ['dvdr']),
		([16], ['dvdr']),
		([6], ['dvdr']),
		([25], ['dvdr']),
		([28], ['dvdr']),
		([5], ['cam', 'ts', 'dvdrip', 'tc', 'r5', 'scr', 'brrip']),
	]

	http_time_between_calls = 1 #seconds

	cat_backup_id = None

	def _searchOnTitle(self, title, movie, quality, results):

		searchurl = self.urls['search'] % (tryUrlencode('%s %s' % (title.replace(':', ''), movie['library']['year'])), self.getCatId(quality['identifier'])[0])
		data = self.getHTMLData(searchurl, opener = self.login_opener)
		
		
		if data:
		
			html = BeautifulSoup(data)
			
			try:
				resultsTable = html.find('div', attrs = {'id' : 'torrent-table-wrapper'})
				if not resultsTable:
					return
				
				# Collecting entries
				entries_std = resultsTable.find_all('div' , attrs = {'id' : 'torrent-std'})
				entries_sticky = resultsTable.find_all('div' , attrs = {'id' : 'torrent-sticky'})
				
				# Extracting results from sticky entries
				for result in entries_sticky:
					
					torrentId = (((result.find('div', attrs = {'id' :'torrent-download'})).find('a'))['href']).replace('download.php?id=','')
					torrentName = ((result.find('div', attrs = {'id' :'torrent-udgivelse2-users'})).find('a'))['title']
					
					# Name trimming
					torrentName = torrentName.replace("3D.", "")
					torrentName = torrentName.replace('EXTENDED.CUT.','')
					torrentName = torrentName.replace('UNRATED.CUT.','')
					torrentName = torrentName.replace('THEATRICAL.CUT.','')
					torrentName = torrentName.replace('EXTENDED.','')
					torrentName = torrentName.replace('UNRATED.','')
					torrentName = torrentName.replace('THEATRICAL.','')
					torrentName = torrentName.replace('Extended.Cut.','')
					torrentName = torrentName.replace('Unrated.Cut.','')
					torrentName = torrentName.replace('Theatrical.Cut.','')
					torrentName = torrentName.replace('Extended.','')
					torrentName = torrentName.replace('Unrated.','')
					torrentName = torrentName.replace('Theatrical.','')
					
						
					results.append({
						'id': torrentId,
						'name': torrentName,
						'url': (self.urls['download'] % torrentId).encode('utf8'),
						'detail_url': (self.urls['detail'] % torrentId).encode('utf8'),
						'size': self.parseSize(result.find('div', attrs = {'id' : 'torrent-size'}).text),
						'seeders': tryInt(result.find('div', attrs = {'id' : 'torrent-seeders'})),
						'leechers': tryInt(result.find('div', attrs = {'id' : 'torrent-leechers'})),
				})
	
				# Extracting results from standard entries
				for result in entries_std:
					
					torrentId = (((result.find('div', attrs = {'id' :'torrent-download'})).find('a'))['href']).replace('download.php?id=','')
					torrentName = ((result.find('div', attrs = {'id' :'torrent-udgivelse2-users'})).find('a'))['title']

					# Name trimming
					torrentName = torrentName.replace("3D.", "")
					torrentName = torrentName.replace('EXTENDED.CUT.','')
					torrentName = torrentName.replace('UNRATED.CUT.','')
					torrentName = torrentName.replace('THEATRICAL.CUT.','')
					torrentName = torrentName.replace('EXTENDED.','')
					torrentName = torrentName.replace('UNRATED.','')
					torrentName = torrentName.replace('THEATRICAL.','')
					torrentName = torrentName.replace('Extended.Cut.','')
					torrentName = torrentName.replace('Unrated.Cut.','')
					torrentName = torrentName.replace('Theatrical.Cut.','')
					torrentName = torrentName.replace('Extended.','')
					torrentName = torrentName.replace('Unrated.','')
					torrentName = torrentName.replace('Theatrical.','')
	
						
					results.append({
						'id': torrentId,
						'name': torrentName,
						'url': (self.urls['download'] % torrentId).encode('utf8'),
						'detail_url': (self.urls['detail'] % torrentId).encode('utf8'),
						'size' :self.parseSize(result.find('div', attrs = {'id' : 'torrent-size'}).text),
						'seeders': tryInt(result.find('div', attrs = {'id' : 'torrent-seeders'})),
						'leechers': tryInt(result.find('div', attrs = {'id' : 'torrent-leechers'})),
				})
					

			except:
				log.error('Failed to parsing %s: %s', (self.getName(),traceback.format_exc()))


	def getLoginParams(self):
		return tryUrlencode({
			'username': self.conf('username'),
			'password': self.conf('password'),
		})

	def loginSuccess(self, output):
		if "<title>NextGen - Login</title>" in output:
			return False
		else:
			return True
		

	loginCheckSuccess = loginSuccess

	def login(self):

		# Check if we are still logged in every hour
		now = time.time()
		if self.login_opener and self.last_login_check < (now - 3600):
			try:
				output = self.urlopen(self.urls['test'], opener = self.login_opener)
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
			# Find csrf for login
			cookiejar = cookielib.CookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
			data_login = self.getHTMLData(self.urls['login_page'], opener = opener)
			bs = BeautifulSoup(data_login)
			csrfraw = bs.find('form', attrs = {'id': 'login'})['action']
			
			# Create 'login' in self.urls
			self.urls['login'] = (self.urls['test'] + csrfraw).encode('utf8')
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