from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.http.easynews import Base
from couchpotato.core.media.movie.providers.base import MovieProvider

log = CPLog(__name__)

autoload = 'Easynews'


class Easynews(MovieProvider, Base):
    pass
