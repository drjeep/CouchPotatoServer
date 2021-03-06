import os
import requests
import urllib

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup

from datetime import datetime
from dateutil import parser
from couchpotato.core.helpers.encoding import simplifyString
from couchpotato.core.helpers.variable import getTitle
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.http.base import HTTPProvider

log = CPLog(__name__)


class Base(HTTPProvider):

    urls = {
        'search': 'http://members.easynews.com/global5/index.html?fty[]=VIDEO&s1=dsize&s1d=-&u=1',
    }

    def _search(self, movie, quality, results):
        """
        defaults = {
            'id': 0,
            'type': self.provider.type,
            'provider': self.provider.getName(),
            'download': self.provider.download,
            'url': '',
            'name': '',
            'age': 0,
            'size': 0,
            'description': '',
            'score': 0
        }
        """
        q = '%s %s %s' % (simplifyString(getTitle(movie)), movie['info']['year'], quality['identifier'])
        log.info(q)

        search = []
        r = requests.get(self.urls['search'],
                     params={'gps': q},
                     auth=(self.conf('username'), self.conf('password')))

        soup = BeautifulSoup(r.text)
        rows = soup.find_all('tr', 'rRow1') + soup.find_all('tr', 'rRow2')
        for tr in rows:
            url = tr.find('td', 'subject').find('a')['href']
            search.append({
                'id': tr.find('input', 'checkbox')['value'],
                'file': urllib.unquote(os.path.basename(url)),
                'url': url,
                'size': tr.find('td', 'fSize').string,
                'date': tr.find('td', 'timeStamp').string
            })

        for s in search:

            def extra_score(item):
                group1 = (0, 50)[any(g in s['file'].lower() for g in ('ctrlhd', 'wiki', 'esir', 'shitsony', 'cytsunee', 'don.mkv'))]
                group2 = (0, 30)[any(g in s['file'].lower() for g in ('chd', 'hdc', 'hdchina'))]
                hires = (0, 10)['1080p' in s['file'].lower()]

                return group1 + group2 + hires

            d = parser.parse(s['date'])
            if d > datetime.now():
                d = datetime(d.year - 1, d.month, d.day)
            age = (datetime.now() - d).days + 1

            results.append({
                'id': s['id'],
                'name': s['file'],
                'age': age,
                'size': self.parseSize(s['size']),
                'url': s['url'],
                'detail_url': r.url,
                'extra_score': extra_score
            })

    def download(self, url='', nzb_id=''):
        return url


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