# -*-coding: utf-8 -*-
import urllib


class GoogleQuery():

    base_url_tpl = 'https://www.google.{zone}/search?q={query}{params}'

    zone_params = {
        'com.ua': {
            'hl': 'ru'
        },
        'co.uk': {
            'hl': 'en'
        },
        'co.id': {
            'hl': 'en',
            'custom': 'gl=en'
        },
        'com.hk': {
            'hl': 'en',
            'custom': 'gl=en&pws=0&gcs=Hongkong'
        },
        'bg': {
            'hl': 'bg'
        },
        'com.uag': {
            'hl': 'ru',
            'custom': 'tbs=ctr:countryUA&cr=countryUA'
        },
        'com': {
            'hl': 'en',
            'custom': 'gl=US&gr=US-UT&gcs=NewYork'
        }
    }

    num = 10

    def __init__(self, zone, query, region=None, start=0, num=10, zone_params=None, always_params='as_dt=e', custom_params=None):
        self.zone = zone
        self.query = query
        self.region = region
        self.start = int(start) * num
        self.always_params = always_params
        self.num = int(num) if num else self.num
        self.custom_params = custom_params

        if zone_params:
            self.zone_params = zone_params

    def _get_crutch_zone(self):
        if self.zone == 'com.uag':
            return 'com.ua'
        return self.zone

    def get_url(self):
        u"""Возвращает урл"""

        params = ''

        if self.num:
            params += '&num={0}'.format(self.num)

        if self.start:
            params += '&start={0}'.format(self.start)

        zone_params = self.zone_params.get(self.zone, {})
        hl = zone_params.get('hl')
        if hl:
            params += '&hl={0}'.format(hl)

        zone_custom = zone_params.get('custom', {})
        if zone_custom:
            params += '&{}'.format(zone_custom)

        if self.always_params:
            params += '&{}'.format(self.always_params)

        if self.region:
            params += '&near={0}'.format(urllib.quote(self.region))

        if self.custom_params:
            params += '&{0}'.format(self.custom_params)

        return self.base_url_tpl.format(
            zone=self._get_crutch_zone(), query=urllib.quote(self.query), params=params
        )