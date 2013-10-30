from .main import NxtGn

def start():
	return NxtGn()

config = [{
	'name': 'nxtgn',
	'groups': [
		{
			'tab': 'searcher',
			'subtab': 'torrent_providers',
			'name': 'NxtGn',
			'description': 'See <a href="http://nxtgn.org">NxtGn</a>',
			'wizard': True,
			'options': [
				{
					'name': 'enabled',
					'type': 'enabler',
					'default': False,
				},
				{
					'name': 'username',
					'default': '',
				},
				{
					'name': 'password',
					'default': '',
					'type': 'password',
				}
			],
		},
	],
}]
