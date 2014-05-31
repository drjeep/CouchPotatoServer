import xmlrpclib
import traceback
from couchpotato.core.downloaders.base import Downloader
from couchpotato.core.logger import CPLog

log = CPLog(__name__)


def true_false(val):
    lookup = {
        True: 'true',
        False: 'false',
    }
    return lookup.get(val, 'false')


class Aria2(Downloader):

    protocol = ['http']

    def connect(self, reconnect=False):
        try:
            self.rpc = xmlrpclib.ServerProxy('http://%s/rpc' % self.conf('host'))
            self.rpc.aria2.addUri()
        except xmlrpclib.Fault as e:
            if e.faultString == 'The parameter at 0 is required but missing.':
                return True
        return False

    def download(self, data=None, media=None, filedata=None):
        if not media: media = {}
        if not data: data = {}

        if not filedata:
            log.error('Unable to get file: %s', traceback.format_exc())
            return False
        
        log.info('Sending "%s" to aria2', data.get('name'))
        
        if not self.connect():
            return False

        #s = xmlrpclib.ServerProxy('http://%s/rpc' % self.conf('host'))
        return self.rpc.aria2.addUri([data['url']], {'pause': true_false(self.conf('pause'))})

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
