from couchpotato.core.media._base.providers.base import YarrProvider
# import time


class HTTPProvider(YarrProvider):
    protocol = 'http'

#     def calculateAge(self, unix):
#         return int(time.time() - unix) / 24 / 60 / 60
