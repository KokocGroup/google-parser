#! coding: utf-8


import unittest
from google_query import GoogleQuery, GoogleQueryError
from google_query.tests import GoogleQueryTests


class GoogleParserTests(GoogleQueryTests):
    def test1(self):
        q = GoogleQuery('ru', 'стол')
        self.assertEqual(q.get_url(), 'https://www.google.ru/search?q=%D1%81%D1%82%D0%BE%D0%BB&num=10&as_dt=e')

    def test2(self):
        q = GoogleQuery('ru', 'стол', region='Москва')
        self.assertEqual(q.get_url(), 'https://www.google.ru/search?q=%D1%81%D1%82%D0%BE%D0%BB&num=10&as_dt=e&near=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0')

    def test3(self):
        q = GoogleQuery('ru', 'стол', region='Москва', start=0)
        self.assertEqual(q.get_url(), 'https://www.google.ru/search?q=%D1%81%D1%82%D0%BE%D0%BB&num=10&as_dt=e&near=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0')

    def test4(self):
        q = GoogleQuery('ru', 'стол', region='Москва', start=1)
        self.assertEqual(q.get_url(), 'https://www.google.ru/search?q=%D1%81%D1%82%D0%BE%D0%BB&num=10&start=10&as_dt=e&near=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0')

    def test5(self):
        q = GoogleQuery('ru', 'стол', region='Москва', start=2)
        self.assertEqual(q.get_url(), 'https://www.google.ru/search?q=%D1%81%D1%82%D0%BE%D0%BB&num=10&start=20&as_dt=e&near=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0')

    def test6(self):
        q = GoogleQuery('ru', 'стол', region='Москва', start=2, num=50)
        self.assertEqual(q.get_url(), 'https://www.google.ru/search?q=%D1%81%D1%82%D0%BE%D0%BB&num=50&start=100&as_dt=e&near=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0')

    def test8(self):
        q = GoogleQuery('com', 'стол', region='Washington', start=2, num=50)
        self.assertEqual(q.get_url(), 'https://www.google.com/search?q=%D1%81%D1%82%D0%BE%D0%BB&num=50&start=100&hl=en&gl=US&gr=US-UT&gcs=NewYork&as_dt=e&near=Washington')

    def test9(self):
        q = GoogleQuery('info', 'стол', region='Washington', start=2, num=50)
        self.assertEqual(q.get_url(), 'https://www.google.info/search?q=%D1%81%D1%82%D0%BE%D0%BB&num=50&start=100&as_dt=e&near=Washington')

    def test10(self):
        q = GoogleQuery('info', 'стол', region='Washington', start=2, num=50, custom_params='oq=table&psi=1231231231')
        self.assertEqual(q.get_url(), 'https://www.google.info/search?q=%D1%81%D1%82%D0%BE%D0%BB&num=50&start=100&as_dt=e&near=Washington&oq=table&psi=1231231231')

    def test11(self):
        q = GoogleQuery('com.uag', 'стол', region='Washington', start=2, num=50, custom_params='oq=table&psi=1231231231')
        self.assertEqual(q.get_url(), 'https://www.google.com.ua/search?q=%D1%81%D1%82%D0%BE%D0%BB&num=50&start=100&hl=ru&tbs=ctr:countryUA&cr=countryUA&as_dt=e&near=Washington&oq=table&psi=1231231231')

    def test12(self):
        cookie = GoogleQuery.get_region_cookie(u'Москва')
        self.assertTrue(cookie)

    def test13(self):
        cookie = GoogleQuery.get_region_cookie(u'москва')
        self.assertTrue(cookie)

    def test14(self):
        cookie = GoogleQuery.get_region_cookie(u'Санкт-Петербург')
        self.assertTrue(cookie)

    def test15(self):
        cookie = GoogleQuery.get_region_cookie(u'Марс')
        self.assertEquals(cookie, {})

    def test16(self):
        with self.assertRaises(GoogleQueryError) as e:
            GoogleQuery.get_zone_and_region(u'Марс')

    def test17(self):
        res = GoogleQuery.get_zone_and_region(u'Москва')
        self.assertEquals(res['uule'], 'a+cm9sZToxCnByb2R1Y2VyOjEyCnByb3ZlbmFuY2U6Ngp0aW1lc3RhbXA6IDE0OTI2MDk1MTAwMDAwMApsYXRsbmd7CmxhdGl0dWRlX2U3OjU1NzU1ODI2MApsb25naXR1ZGVfZTc6Mzc2MTczMDAwCn0KcmFkaXVzOjI5MTQw')
        self.assertEquals(res['zone'], 'ru')

    def test18(self):
        res = GoogleQuery.get_zone_and_region(u'Казахстан')
        self.assertEquals(res['uule'], 'a+cm9sZToxCnByb2R1Y2VyOjEyCnByb3ZlbmFuY2U6Ngp0aW1lc3RhbXA6IDE0OTI2MDk1MTAwMDAwMApsYXRsbmd7CmxhdGl0dWRlX2U3OjQ4MDE5NTczMApsb25naXR1ZGVfZTc6NjY5MjM2ODQwCn0KcmFkaXVzOjI5MTQw')
        self.assertEquals(res['zone'], 'kz')
