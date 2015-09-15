from .main import NxtGn

def autoload():
  return NxtGn()

config = [{
  'name': 'nxtgn',
  'groups': [
    {
      'tab': 'searcher',
      'list': 'torrent_providers',
      'name': 'NxtGn',
      'description': 'See <a href="https://nxgn.org">NxtGn</a>',
      'wizard': True,
      'icon': 'AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAMIeAADCHgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACqABQiqgAUiKoAFIgAAAAAAAAAAAAAAAAAAAAAqgAUZgAAAAAAAAAAqgAUiKoAFIiqABSIqgAUiKoAFCIAAAAAqgAUVaoAFP+qABT/qgAUEQAAAAAAAAAAqgAUu6oAFKqqABQiqgAU7qoAFP+qABT/qgAU/6oAFP+qABRVAAAAAKoAFFWqABT/qgAU/6oAFBEAAAAAqgAUu6oAFP+qABSqqgAUzKoAFP+qABT/qgAU/6oAFP+qABT/qgAUVQAAAACqABRVqgAU/6oAFP+qABQRqgAUu6oAFP+qABT/qgAUu6oAFP+qABT/qgAUqgAAAACqABTuqgAU/6oAFFUAAAAAqgAUVaoAFP+qABT/qgAUu6oAFP+qABT/qgAU/6oAFLuqABT/qgAU/6oAFHcAAAAAqgAU7qoAFP+qABRVAAAAAKoAFFWqABT/qgAU/6oAFP+qABT/qgAU/6oAFP+qABSqqgAU3aoAFP+qABT/qgAUiKoAFIiqABSIqgAUVQAAAACqABQiqgAU3aoAFP+qABT/qgAUu6oAFMyqABT/qgAUqqoAFGaqABT/qgAU/6oAFP+qABT/qgAU/6oAFO6qABQzAAAAAKoAFCKqABTuqgAUuwAAAACqABTMqgAU/6oAFKoAAAAAqgAUZqoAFMyqABT/qgAU/6oAFP+qABT/qgAU7gAAAAAAAAAAAAAAAAAAAAAAAAAAqgAUd6oAFIiqABRmAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//8AAP//AAD//wAAHsEAAAwBAAAIAQAAABEAAAARAAAAAQAAAAAAAIiAAAD4/wAA//8AAP//AAD//wAA//8AAA%3D%3D',
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
          'name': 'seed_ratio',
          'label': 'Seed ratio',
          'type': 'float',
          'default': 1,
          'description': 'Will not be (re)moved until this seed ratio is met.',
        },
        {
          'name': 'seed_time',
          'label': 'Seed time',
          'type': 'int',
          'default': 48,
          'description': 'Will not be (re)moved until this seed time (in hours) is met.',
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

