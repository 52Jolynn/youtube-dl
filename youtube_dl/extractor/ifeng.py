# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class IfengIE(InfoExtractor):
    ''' ifeng extractor '''
    IE_NAME = 'ifeng'
    IE_DESC = '凤凰网'
    # http://v.ifeng.com/mil/mainland/201601/01d92436-8afe-4af0-82a4-cef889018295.shtml
    # http://v.ifeng.com/ent/mingxing/201601/01e29bc2-1e89-41ee-9a91-25d56e2b0740.shtml
    _VALID_URL = r'http://v\.ifeng\.com/.+?/(?P<id>[\w\-\d]+)\.shtml'
    _TESTS = [{
        'url': 'http://v.ifeng.com/mil/mainland/201601/01d92436-8afe-4af0-82a4-cef889018295.shtml',
        'info_dict': {
            'id': '01d92436-8afe-4af0-82a4-cef889018295',
            'ext': 'mp4',
            'title': '中国火箭军正式亮相 多支导弹旅携罕见导弹出镜',
        }
    },
        {
            'url': 'http://v.ifeng.com/ent/mingxing/201601/01e29bc2-1e89-41ee-9a91-25d56e2b0740.shtml',
            'info_dict': {
                'id': '01e29bc2-1e89-41ee-9a91-25d56e2b0740',
                'ext': 'mp4',
                'title': '陈羽凡锁骨骨折 盼早日康复',
            },
        },
        {
            'url': 'http://v.ifeng.com/mil/mainland/201601/01168f8e-bcd5-459b-91b4-f85893b3e40a.shtml',
            'info_dict': {
                'id': '01168f8e-bcd5-459b-91b4-f85893b3e40a',
                'ext': 'mp4',
                'title': '2015年中美两国组织多次演练',
            },
        }
    ]

    def _real_extract(self, url):
        ''' extract ifeng url '''
        video_id = self._match_id(url);

        d = video_id[-2]
        dd = video_id[-2:]

        info_doc = self._download_xml(
                'http://v.ifeng.com/video_info_new/{0}/{1}/{2}.xml'.format(d, dd, video_id),
                video_id, 'fetch video metadata')

        title = info_doc.find('./item').get('Name')

        for element in info_doc.findall('./videos/video'):
            if element.get('mediaType') != 'mp4':
                continue

            url = element.get('VideoPlayUrl')
            if element.get('type') == '500k':
                break

        return {
            'id': video_id,
            'title': title,
            'url': url,
            'ext': 'mp4',
        }
