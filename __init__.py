from .main import NxtGn

def start():
	return NxtGn()

config = [{
	'name': 'nxtgn',
	'groups': [
		{
			'tab': 'searcher',
			'list': 'torrent_providers',
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
				},
				{
					'name': 'extra_score',
					'advanced': True,
					'label': 'Extra Score',
					'type': 'int',
					'default': 20,
					'description': 'Starting score for each release found via this provider.',
				}
			],
		},
	],
}]
