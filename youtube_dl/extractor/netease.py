# coding: utf-8
from __future__ import unicode_literals

import re
from .common import InfoExtractor
from ..compat import (
    compat_urllib_parse_unquote,
)

class NeteaseIE(InfoExtractor):
    ''' netease extractor '''
    IE_NAME = 'netease'
    IE_DESC = '网易视频'
    # http://v.163.com/paike/VAP4BFE3U/VBC780V5O.html
    # http://v.163.com/zixun/V5HPAE5GL/VBCKAF95G.html
    _VALID_URL = r'http://v\.163\.com/.+?/(?P<id>[\w_\-\d]+)\.html'
    _TESTS = [{
        'url': 'http://v.163.com/paike/VAP4BFE3U/VBC780V5O.html',
        'info_dict': {
            'id': 'VBC780V5O',
            'ext': 'flv',
            'title': '一起来感受下印度开挂民族的达人秀',
        }
    },
        {
            'url': 'http://v.163.com/zixun/V5HPAE5GL/VBCKAF95G.html',
            'info_dict': {
                'id': 'VBCKAF95G',
                'ext': 'flv',
                'title': '剧组拍战争戏炸药出意外 演员被炸伤截肢',
            },
        }
    ]

    def _real_extract(self, url):
        ''' extract netease url '''
        video_id = self._match_id(url);

        webpage = self._download_webpage(url, video_id)
        topicId = self._search_regex(r'(?is)topicid\s*=\s*\'(?P<topicId>\d+)\'', webpage, 'topicId')

        # http://xml.ws.126.net/video/F/E/1000_VBBV9DKFE.xml
        xml = self._download_webpage('http://xml.ws.126.net/video/{0}/{1}/{2}_{3}.xml'.format(video_id[-2], video_id[-1], topicId, video_id),
                video_id)
        title =  compat_urllib_parse_unquote(self._search_regex(r'(?is)<title>[\r\n]*(?P<title>.+?)[\r\n]*</title>', xml, 'title'))

        entry = {
            'id': '{0}'.format(video_id),
            'title': title,
            'formats': []
        }

        regex = re.search(r'(?is)<flvUrl>(?:[\r\n]*<flv>[\r\n]*(?P<url>.+?)[\r\n]*</flv>[\r\n]*)+</flvUrl>', xml)
        if (regex):
            entry['formats'].append({
                'url' : regex.group('url'),
                'ext' : 'flv',
                'quality' : -1
            })

        regex = re.search(r'(?is)<hdUrl>(?:[\r\n]*<flv>[\r\n]*(?P<url>.+?)[\r\n]*</flv>[\r\n]*)+</hdUrl>', xml)
        if (regex):
            entry['formats'].append({
                'url' : regex.group('url'),
                'ext' : 'flv',
                'quality' : -1
            })

        regex = re.search(r'(?is)<shdUrl>(?:[\r\n]*<flv>[\r\n]*(?P<url>.+?)[\r\n]*</flv>[\r\n]*)+</shdUrl>', xml)
        if (regex):
            entry['formats'].append({
                'url' : regex.group('url'),
                'ext' : 'flv',
                'quality' : -1
            })

        return {
            'id': video_id,
            'title': title,
            '_type': 'multi_video',
            'entries': [entry],
        }
