from .main import Easynews


def start():
    return Easynews()

config = [{
    'name': 'easynews',
    'groups': [
        {
            'tab': 'searcher',
            'list': 'http_providers',
            'name': 'Easynews',
            'description': 'Easynews global search',
            'wizard': True,
            'options': [
                {
                    'name': 'enabled',
                    'type': 'enabler',
                },
                {
                    'name': 'username',
                    'label': 'Username',
                },
                {
                    'name': 'password',
                    'label': 'Password',
                },
            ],
        },
    ],
}]
