import xmlrpclib
import traceback
from couchpotato.core._base.downloader.main import DownloaderBase
from couchpotato.core.logger import CPLog

log = CPLog(__name__)

autoload = 'Aria2'


def true_false(val):
    lookup = {
        True: 'true',
        False: 'false',
    }
    return lookup.get(val, 'false')


class Aria2(DownloaderBase):

    protocol = ['http']
    log = CPLog(__name__)
    rpc = None

    def connect(self):
        try:
            self.rpc = xmlrpclib.ServerProxy('http://%s/rpc' % self.conf('host'))
            self.rpc.aria2.addUri()
        except xmlrpclib.Fault as e:
            if not e.faultString == 'The parameter at 0 is required but missing.':
                log.error('Could not connect to aria2: %s' % str(e))
                return False
        return True

    def download(self, data=None, media=None, filedata=None):
        if not media: media = {}
        if not data: data = {}

        log.info('Sending "%s" to aria2 (%s)', (data.get('name'), data.get('protocol')))
        log.debug(data)

        if not self.connect():
            return False

        if not filedata and data.get('protocol') == 'http':
            log.error('Failed sending URL to aria2, no data')
            return False

        # s = xmlrpclib.ServerProxy('http://%s/rpc' % self.conf('host'))
        r = self.rpc.aria2.addUri([data.get('url')], {'pause': true_false(self.conf('pause'))})
        log.debug(r)

        log.info('URL sent to aria2 successfully.')
        return self.downloadReturnId('test')

    def test(self):
        return self.connect()

    def getAllDownloadStatus(self, ids):
        """
        status = {'id': '', 'name': '', 'status': '', 'original_status': '', 'timeleft': ''}
        """
        log.debug('Checking aria2 download status...')

        statuses = []

        return statuses

    def removeFailed(self, item):
        if not self.conf('delete_failed', default=True):
            return False

        log.info('%s failed downloading, deleting...', item['name'])

        return True

config = [{
    'name': 'aria2',
    'groups': [
        {
            'tab': 'downloaders',
            'name': 'aria2',
            'label': 'aria2',
            'description': 'Send download URLs to aria2.',
            'wizard': True,
            'options': [
                {
                    'name': 'enabled',
                    'default': 0,
                    'type': 'enabler',
                    'radio_group': 'http',
                },
                {
                    'name': 'host',
                    'default': 'htpc:6800',
                },
                {
                    'name': 'pause',
                    'default': True,
                    'type': 'bool',
                    'advanced': True,
                    'description': 'Pause download after added.',
                },
                {
                    'name': 'manual',
                    'default': True,
                    'type': 'bool',
                    'advanced': True,
                    'description': 'Disable this downloader for automated searches, but use it when I manually send a release.',
                },
                {
                    'name': 'delete_failed',
                    'default': False,
                    'type': 'bool',
                    'description': 'Delete a release after the download has failed.',
                },
            ],
        }
    ],
}]
