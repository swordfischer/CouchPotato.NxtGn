from bs4 import BeautifulSoup
from couchpotato.core.helpers.encoding import tryUrlencode
from couchpotato.core.helpers.variable import tryInt
from couchpotato.core.logger import CPLog
from couchpotato.core.providers.torrent.base import TorrentProvider
import traceback


log = CPLog(__name__)


class NxtGn(TorrentProvider):

	urls = {
		'test' : 'http://nxtgn.org/',
		'login' : 'http://nxtgn.org/takelogin.php?csrf=c75117e01fa83270e68cfcec8a7b43bd',
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
		([44], ['brrip']),
	]

	http_time_between_calls = 1 #seconds
	cat_backup_id = None

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

					torrent_id = result.find_all('td')[2].find('a')['id'].replace('details.php?id=', '')
					torrent_title = result.find_all('td')[1].find('a')['title']
					torrent_size = self.parseSize(result.find_all('td')[7].contents[0])
					torrent_seeders = tryInt(result.find_all('td')[8].find('a')['class'])
					torrent_leechers =  tryInt(result.find_all('td')[9].find('a')['class'])
					imdb_id = getImdb(result.find_all('td')[1], check_inside = True)

					results.append({
						'id': torrent_id,
						'name': torrent_title,
						'url': self.urls['download'] % torrent_id,
						'detail_url': self.urls['detail'] % torrent_id,
						'size': torrent_size,
						'seeders': torrent_seeders if torrent_seeders else 0,
						'leechers': torrent_leechers if torrent_leechers else 0,
						'description': imdb_id if imdb_id else '',
					})

			except:
				log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))


	def getLoginParams(self):
		return tryUrlencode({
			'username': self.conf('username'),
			'password': self.conf('password'),
			'login': 'submit',
		})

	def loginSuccess(self, output):
		return 'Login fejl!' not in output
