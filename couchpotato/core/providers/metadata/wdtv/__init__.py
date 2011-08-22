from .main import WDTV

def start():
    return WDTV()

config = [{
    'name': 'wdtv',
    'groups': [
        {
            'tab': 'renamer',
            'name': 'metadata',
            'label': 'WDTV',
            'description': 'Enable metadata WDTV can understand',
            'options': [
                {
                    'name': 'meta_enabled',
                    'default': False,
                    'type': 'enabler',
                },
                {
                    'name': 'meta_thumbnail',
                    'default': True,
                    'type': 'bool',
                },
            ],
        },
    ],
}]
