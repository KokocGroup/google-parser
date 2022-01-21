#! coding: utf-8
import json

import unittest

from google_parser.exceptions import GoogleParserError
from google_parser.tests import GoogleParserTests
from google_parser.google import GoogleParser, SnippetsParserDefault, GoogleJsonParser, GoogleMobileParser
from google_parser.google_query import GoogleQuery


class GoogleParserTestCase(GoogleParserTests):
    def test_http(self):
        snippets = [
            (1, "https://www.express-bank.ru/moscow/faq/cards", u"Часто задаваемые вопросы о банковских картах | Восточный ...", u"Карты Восточного экспресс банка можно использовать за границей? ... экспресс банком, можно использовать за рубежом: оплачивать товары и услуги в ..."),
            (2, "https://www.express-bank.ru/moscow/private/payments", u"Оплата товаров и услуг | Восточный экспресс банк", u"Банковская карта Visa от Восточного экспресс банка принимается к оплате везде, где стоит знак Visa. Оплачивайте товары и услуги с помощью ..."),
            (3, "https://www.express-bank.ru/moscow/private/cards/debit", u"Дебетовые карты - Восточный экспресс банк", u"Предлагаем дебетовые банковские карты Visa. ... С помощью карты вы можете оплачивать необходимые покупки, осуществлять накопления, снимать ..."),
            (4, "https://www.express-bank.ru/moscow/private/terminals", u"Терминалы оплаты | Восточный экспресс банк", u"Терминалы оплаты ... Процесс оплаты простой и занимает всего несколько минут. Деньги на нужный счет ... (карты сторонних банков отключены)."),
            (5, "https://www.express-bank.ru/moscow/private/payments/credit", u"Погашение кредитов | Восточный экспресс банк", u"3. В отделении Восточного экспресс банка. При наличии карты Восточного экспресс банка можно оплатить кредит кассе отделения, что существенно ..."),
            (6, "https://www.express-bank.ru/moscow/private/credits/repayment", u"Как оплачивать кредит | Восточный экспресс банк", u"1. В отделении Восточного экспресс банка. Обслуживание в кассе осуществляется только при наличии пластиковой карты. Наличие карты значительно ..."),
            (7, "https://www.express-bank.ru/moscow/faq/credit-card", u"Часто задаваемые вопросы о картах | Восточный экспресс банк", u"В случае оплаты покупки в долларах США или евро «рублевой» картой, конвертация происходит по курсу банка на момент списания средств со счёта ..."),
            (8, "https://www.express-bank.ru/moscow/private/payments/automts", u"Автоплатежи МТС | Восточный экспресс банк", u"Восточный экспресс банк ... Если вы не являетесь держателем карты Восточного экспресс банка, обратитесь в ближайшее ... Оплата товаров и услуг."),
            (9, "https://www.express-bank.ru/moscow/private/online/internet/posibilities", u"Возможности интернет-банка | Восточный экспресс банк", u"Совершайте банковские операции по своим счетам дистанционно. ... денежных средств, оплачивать покупки и услуги в режиме реального времени. ... кредиту;; по кредитной карте, которая включает сумму минимального платежа, ..."),
            (10, "https://www.express-bank.ru/moscow/faq/credit-price", u"Обслуживание кредита, кредитной карты | Восточный экспресс ...", u"Наиболее частые вопросы по обслуживанию кредита, кредитной карты. ... ли я оплатить задолженность по кредиту/кредитной карте в филиале Банка в ..."),
        ]
        html = self.get_data('google.html')
        founded = GoogleParser(html).get_snippets()

        self.assertEqual(len(founded), 10)
        self.check(snippets, founded)

    def test_ftp(self):
        snippets = [
            (1, "ftp://os2.fannet.ru/Boating/books/kija-new/2009-06%20(222).pdf", u"техника", u"в «базе» нет удобного раскладывающегося сто- лика – он ..... РИБа « Кальмар» с мотором от. «Волги», не ..... если выполнить ее складной и снабдить .... гое время на одной и той же лодке «SkyBoat 440» (сегодня ...... остойчивости на дно укладывают бал- ласт. ...... (ее составили «Олимп» и « Люкс» из."),
        ]

        html = self.get_data('google-ftp.html')
        founded = GoogleParser(html).get_snippets()

        self.assertEqual(len(founded), 1)
        self.check(snippets, founded)

    def test1(self):
        u""""
            Проверяем на наличие капчи
        """
        html = self.get_data('google-captcha.html')
        g = GoogleParser(html)
        captcha = g.get_captcha_data()
        self.assertEqual(captcha['url'], 'https://www.google.com/sorry/image?id=10009568273031142024&hl=en')
        self.assertEqual(captcha['captcha_coninue'], 'https://www.google.ru/search?num=10&hl=ru&start=0&q=yandex&as_dt=e')
        self.assertEqual(captcha['captcha_id'], '10009568273031142024')

    def test2(self):
        u""""
            Капчи быть не должно
        """
        html = self.get_data('google.html')
        g = GoogleParser(html)
        captcha = g.get_captcha_data()
        self.assertEqual(captcha, None)

    def test3(self):
        u""""
            Не заблокировано
        """
        html = self.get_data('google.html')
        g = GoogleParser(html)
        blocked = g.is_blocked()
        self.assertEqual(blocked, False)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test4(self):
        u""""
            Ничего не найдено есть
        """
        html = self.get_data('not-found.html')
        g = GoogleParser(html)
        self.assertEqual(g.is_not_found(), True)

        pe = GoogleParser.pagination_exists(html)
        self.assertFalse(pe)

    def test6(self):
        u""""
            Ничего не найдено есть
        """
        html = self.get_data('google_not_found.html')
        g = GoogleParser(html)
        self.assertEqual(g.is_not_found(), True)

    def test7(self):
        u""""
            Ничего не найдено есть
        """
        html = self.get_data('not_found4.html')
        g = GoogleParser(html)
        self.assertEqual(g.is_not_found(), True)

    def test5(self):
        u""""
            Ничего не найдено нет
        """
        html = self.get_data('google.html')
        g = GoogleParser(html)
        self.assertEqual(g.is_not_found(), False)

    def test8(self):
        u""""
            Ничего не найдено есть
        """
        html = self.get_data('not_found4.html')
        g = GoogleParser(html)
        self.assertEqual(g.is_not_found(), True)

    def test9(self):
        u""""
            Парсинг новой выдачи
        """

        html = self.get_data('google1-2015-07-23.html')
        g = GoogleParser(html)
        res = g.get_serp()

        etalon = json.loads(self.get_data('google1-2015-07-23.json'))
        self.assertEqual(res['pc'], etalon['pc'])
        self.assertEqual(len(res['sn']), len(etalon['sn']))
        self.check2(etalon['sn'], res['sn'])

    def test10(self):
        u""""
            Парсинг новой выдачи
        """

        html = self.get_data('google-2015-07-24.html')
        g = GoogleParser(html)
        res = g.get_serp()

        etalon = json.loads(self.get_data('google-2015-07-24.json'))
        self.assertEqual(res['pc'], etalon['pc'])
        self.assertEqual(len(res['sn']), len(etalon['sn']))
        self.check2(etalon['sn'], res['sn'])

    def test11(self):
        u""""
            Парсинг новой выдачи
        """

        html = self.get_data('google1-2015-07-24.html')
        g = GoogleParser(html)
        res = g.get_serp()

        #на самом деле тут 150000, но из-за того что кэш битый 0
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 99)

    def test12(self):
        u""""
            Парсинг новой выдачи
        """

        html = self.get_data('google2-2015-07-24.html')
        g = GoogleParser(html)
        res = g.get_serp()

        #на самом деле тут 150000, но из-за того что кэш битый 0
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 100)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test13(self):
        u""""
            Парсинг новой выдачи
        """

        html = self.get_data('google-2015-07-27.html')
        g = GoogleParser(html)
        res = g.get_serp()

        self.assertEqual(res['pc'], 571000000)
        self.assertEqual(len(res['sn']), 9)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test14(self):
        u""""
            Парсинг новой выдачи
        """

        html = self.get_data('google1-2015-07-27.html')
        g = GoogleParser(html)
        res = g.get_serp()

        self.assertEqual(res['pc'], 13300)
        self.assertEqual(len(res['sn']), 10)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test15(self):
        u""""
            Парсинг новой выдачи
        """

        html = self.get_data('google2-2015-07-27.html')
        g = GoogleParser(html)
        res = g.get_serp()

        self.assertEqual(res['pc'], 1)
        self.assertEqual(len(res['sn']), 1)

        pe = GoogleParser.pagination_exists(html)
        self.assertFalse(pe)

    def test16(self):
        u""""
            Парсинг новой выдачи
        """

        html = self.get_data('2015-08-11.html')
        g = GoogleParser(html)
        res = g.get_serp()

        self.assertEqual(res['pc'], 923000)
        self.assertEqual(len(res['sn']), 9)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test17(self):
        u""""
            Парсинг новой выдачи
        """

        html = self.get_data('2015-08-11-1.html')
        g = GoogleParser(html)
        res = g.get_serp()

        self.assertEqual(res['pc'], 416000)
        self.assertEqual(len(res['sn']), 10)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test18(self):
        u""""
            Проверка корректности форматирования ссылки
        """
        g = SnippetsParserDefault([])

        result = SnippetsParserDefault.format_link('/interstitial?url=http://podokon.ru/podokonniki-rehau/')
        self.assertEqual(result, 'http://podokon.ru/podokonniki-rehau/')

        result = SnippetsParserDefault.format_link('/interstitial?url=http://podokon.ru/podokonniki-rehau/&a=')
        self.assertEqual(result, 'http://podokon.ru/podokonniki-rehau/')

    def test19(self):
        u""""
            Парсинг новой выдачи
        """

        html = self.get_data('2015-08-21.html')
        g = GoogleParser(html)
        res = g.get_serp()

        self.assertEqual(res['pc'], 245000)
        self.assertEqual(len(res['sn']), 10)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test20(self):
        u""""
            Парсинг новой выдачи
        """
        html = self.get_data('2015-09-04.html')
        g = GoogleParser(html)
        res = g.get_serp()

        self.assertEqual(res['pc'], 59300000)
        self.assertEqual(len(res['sn']), 9)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test21(self):
        u""""
            Парсинг новой выдачи
        """
        html = self.get_data('2015-09-08.html')
        g = GoogleParser(html)
        res = g.get_serp()

        self.assertEqual(res['pc'], 258000)
        self.assertEqual(len(res['sn']), 100)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test22(self):
        u""""
            Парсинг новой выдачи
        """
        html = self.get_data('2015-09-09.html')
        g = GoogleParser(html)
        res = g.get_serp()

        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 0)

        pe = GoogleParser.pagination_exists(html)
        self.assertFalse(pe)

    def test23(self):
        u""""
            Парсинг новой выдачи
        """
        html = self.get_data('2015-09-10-not-found.html')
        g = GoogleParser(html)
        res = g.get_serp()

        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 0)

        pe = GoogleParser.pagination_exists(html)
        self.assertFalse(pe)

    def test24(self):
        u""""
            Парсинг новой выдачи
        """
        html = self.get_data('2015-09-10.html')
        g = GoogleParser(html)
        res = g.get_serp()

        self.assertEqual(res['pc'], 1)
        self.assertEqual(len(res['sn']), 1)

        pe = GoogleParser.pagination_exists(html)
        self.assertFalse(pe)

    def test25(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('suspicious-traffic.html')
        g = GoogleParser(html)
        self.assertTrue(g.is_suspicious_traffic())

    def test26(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2015-09-10.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

    def test27(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2015-09-17.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 7820)
        self.assertEqual(len(res['sn']), 100)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test28(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2015-12-17.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 11)
        self.assertEqual(len(res['sn']), 1)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test29(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2016-01-11.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 275000)
        self.assertEqual(len(res['sn']), 100)
        # self.print_sn(res)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test30(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2016-03-10.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 457000)
        self.assertEqual(len(res['sn']), 10)
        # self.print_sn(res)

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test31(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2016-03-10-1.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 28)
        self.assertEqual(len(res['sn']), 28)
        self.assertEqual(res['sn'][0]['u'], 'http://www.korbis-to.ru/')
        self.assertEqual(res['sn'][27]['u'], 'http://www.isolux.ru/tovary-dlya-dachi-i-sada/tovary-dlya-bani/pechi-dlya-bani/drovyanyye-pechi.html')
        # self.print_sn(res)

        pe = GoogleParser.pagination_exists(html)
        self.assertFalse(pe)

    def test32(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2016-03-10-2.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 352000)
        self.assertEqual(len(res['sn']), 49)
        self.assertEqual(res['sn'][0]['u'], 'http://laennec.ru/')
        self.assertEqual(res['sn'][48]['u'], 'http://www.hindustantimes.com/tech/google-doodle-celebrates-stethoscope-inventor-rene-laennec-s-235th-birthday/story-NG3wmj3WNHL9g9lX7zthuO.html')

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test33(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2016-05-11.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 91)
        self.assertEqual(len(res['sn']), 91)
        self.assertEqual(res['sn'][0]['u'], 'http://gibsonshop.ru/kawai/3597-kawai-ca97w.html')
        self.assertEqual(res['sn'][90]['u'], 'https://www.abcelectronique.com/comparateur/instrument-de-musique/instrument-de-musique/clavier-musique-/piano/index-6-prix_asc.html')

        pe = GoogleParser.pagination_exists(html)
        self.assertFalse(pe)

    def test34(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2016-05-20.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 4)
        self.assertEqual(len(res['sn']), 4)
        self.assertEqual(res['sn'][0]['u'], u'http://www.venturewizard.ru/ecompanyg5p13fpricey0.php')
        self.assertEqual(res['sn'][3]['u'], u'http://www.venturewizard.ru/ecatg83p1fgidy0.php')

        pe = GoogleParser.pagination_exists(html)
        self.assertFalse(pe)

    def test35(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2016-09-12.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'Велосипеды Stels на Каширке - купить велосипед в Москве')
        self.assertEqual(res['sn'][0]['u'], u'http://stelsvelo.ru/')
        self.assertEqual(res['sn'][0]['d'], 'stelsvelo.ru')

        self.assertEqual(res['sn'][98]['t'], u'Велосипеды STELS (СТEЛС), CUBE, MERIDA в Рязани. Купить ...')
        self.assertEqual(res['sn'][98]['u'], u'http://www.velomir-pro.ru/')
        self.assertEqual(res['sn'][98]['d'], 'velomir-pro.ru')

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test36(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2016-09-12-1.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 461000)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'Расписание поездов: Новосибирск - Капчагай, стоимость билета ...')
        self.assertEqual(res['sn'][0]['u'], u'http://www.tutu.ru/poezda/rasp_d.php?nnst1=2044000&nnst2=2700804')
        self.assertEqual(res['sn'][0]['d'], 'tutu.ru')

        self.assertEqual(res['sn'][99]['t'], u'Форум туристов Сибири • Просмотр темы - RUS -&gt; KZ -&gt; KGZ: туда и ...')
        self.assertEqual(res['sn'][99]['u'], u'http://egiki.ru/forum/viewtopic.php?t=2971')
        self.assertEqual(res['sn'][99]['d'], 'egiki.ru')

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test37(self):
        u""""
            Проверяем на наличие капчи. captcha_id стал необязательным
        """

        html = self.get_data('google-captcha-2016-09-29.html')
        g = GoogleParser(html)
        captcha = g.get_captcha_data()
        self.assertTrue(bool(captcha))

    def test38(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2016-11-10.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 560000)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'ПАО «СОЛЬ РУСИ»')
        self.assertEqual(res['sn'][0]['u'], u'http://www.solrusi.ru/')
        self.assertEqual(res['sn'][0]['d'], 'solrusi.ru')

        self.assertEqual(res['sn'][99]['t'], u'Сохранение и приумножение денежных средств в период кризиса ...')
        self.assertEqual(res['sn'][99]['u'], u'http://investtalk.ru/forum/topic/19806-sokhranenie-i-priumnozhenie-denezhnykh-sredstv-v-p/')
        self.assertEqual(res['sn'][99]['d'], 'investtalk.ru')

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test39(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('context-2016-11-22.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_context_serp()

        self.assertEqual(res['pc'], 7)

        self.assertEqual(res['sn'][0]['t'], u'Столешницы из настоящего камня - Элегантные и надежные‎')
        self.assertEqual(res['sn'][0]['u'], u'http://www.kamentorg.ru/stones/natural_stone_products/countertops/')
        self.assertEqual(res['sn'][0]['vu'], u'www.kamentorg.ru/')

        self.assertEqual(res['sn'][1]['t'], u'Кухонные столешницы ИКЕА - IKEA.com‎')
        self.assertEqual(res['sn'][1]['u'], u'http://www.ikea.com/ru/ru/catalog/categories/departments/kitchen/24264/?cid=ps%257Cru%257Ckitchen_furniture%257C201607211330081986_3249')
        self.assertEqual(res['sn'][1]['vu'], u'www.ikea.com/ru/столешницы_икеа')

        self.assertEqual(res['sn'][6]['t'], u'Гранитные подоконники‎')
        self.assertEqual(res['sn'][6]['u'], u'https://www.fabrikaokon.ru/podokonniki.html?utm_campaign=Podokonniki_google&utm_medium=cpc&utm_source=google&utm_content=Granitnye_podokonniki&utm_term=Granitnye_podokonniki')
        self.assertEqual(res['sn'][6]['vu'], u'www.fabrikaokon.ru/подоконники')

    def test40(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('context-no-2016-11-22.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_context_serp()

        self.assertEqual(res['pc'], 0)
        self.assertEqual(res['sn'], [])

    def test41(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('context-only-bottom-2016-11-22.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_context_serp()

        self.assertEqual(res['pc'], 3)

        self.assertEqual(res['sn'][0]['t'], u'Продать Машину дорого - Продать выгодно на CarPrice.ru‎')
        self.assertEqual(res['sn'][0]['u'], u'https://www.carprice.ru/?utm_source=google&utm_medium=dm_cpc_sell&utm_campaign=%5B%D0%B0%D0%B2%D1%82%D0%BE%5D%7Bb%7D%3ARussia&utm_adgroup=%5B%D0%B0%D0%B2%D1%82%D0%BE%7C%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C%7C%D1%81%D0%B0%D0%BB%D0%BE%D0%BD%7C%D0%BF%D1%80%D0%BE%D0%B1%D0%B5%D0%B3%D0%BE%D0%BC%7C%D0%BA%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C%5D%7Bb%7D%3ARussia&utm_content=12_cat.12_cat.23_shop.31_used.41_region&utm_term=%2B%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B8%20%2B%D1%81%20%2B%D0%BF%D1%80%D0%BE%D0%B1%D0%B5%D0%B3%D0%BE%D0%BC%20%2B%D0%BA%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C%20%2B%D0%B0%D0%B2%D1%82%D0%BE%D1%81%D0%B0%D0%BB%D0%BE%D0%BD')
        self.assertEqual(res['sn'][0]['vu'], u'www.carprice.ru/Акция/Получить-10000р')

        self.assertEqual(res['sn'][1]['t'], u'Ищете автомобиль с пробегом? - Взгляните на автомобили Nissan‎')
        self.assertEqual(res['sn'][1]['u'], u'http://www.used.nissan.ru/ru.RU/homepage.htm?cid=psnsnusdcrsofnsvRU_runaomdlocruggppcsrch&utm_source=google_network&utm_medium=cpc&utm_campaign=used_cars&utm_content=offensive&utm_term=%D0%BA%D1%83%D0%BF%D0%B8%D1%82%D1%8C%20%D0%BC%D0%B0%D1%88%D0%B8%D0%BD%D1%83%20%D1%81%D0%BF%D0%B1%20%D0%BF%D0%BE%D0%B4%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D0%BD%D1%83%D1%8E&s_kwcid=AL!84!3!101927968856!b!!g!!%D0%BA%D1%83%D0%BF%D0%B8%D1%82%D1%8C%20%D0%BC%D0%B0%D1%88%D0%B8%D0%BD%D1%83%20%D1%81%D0%BF%D0%B1%20%D0%BF%D0%BE%D0%B4%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D0%BD%D1%83%D1%8E')
        self.assertEqual(res['sn'][1]['vu'], u'used.nissan.ru/Ниссан_с_пробегом')

        self.assertEqual(res['sn'][2]['t'], u'Продажа Новых и Б/У Авто. - Тысячи Авто по Низкой Цене.‎')
        self.assertEqual(res['sn'][2]['u'], u'https://www.google.ru/aclk?sa=l&ai=DChcSEwjU-vahrrzQAhXiC3MKHYBpC7UYABAJ&sig=AOD64_3NG_BERrn-lMcUBxKvVXtAnrguUA&adurl=&q=')
        self.assertEqual(res['sn'][2]['vu'], u'www.avtopoisk.ru/')

    def test42(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2016-12-05.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 355000)
        self.assertEqual(len(res['sn']), 6)

        self.assertEqual(res['sn'][0]['t'], u'Лизинг для юридических и физических лиц - Европлан лизинговая ...')
        self.assertEqual(res['sn'][0]['u'], u'https://europlan.ru/')
        self.assertEqual(res['sn'][0]['d'], 'europlan.ru')

        self.assertEqual(res['sn'][5]['t'], u'Вакансии компании Европлан - работа в Москве, Нижнем ... - HH.ru')
        self.assertEqual(res['sn'][5]['u'], u'https://hh.ru/employer/1329')
        self.assertEqual(res['sn'][5]['d'], 'hh.ru')

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test43(self):
        u""""
            Проверяем на наличие капчи
        """
        html = self.get_data('google-captcha-2016-12-06.html')
        g = GoogleParser(html)
        captcha = g.get_captcha_data()
        self.assertEqual(captcha['url'], 'https://www.google.com/sorry/image?id=14827882021952570767&q=EgQfuMqHGKadm8IFIhkA8aeDSy6Evqypj5j85OIT5nrl-YB2Nl3HMgFj&hl=ru&continue=https://www.google.ru/search%3Fnewwindow%3D1%26espv%3D2%26q%3D%25D0%25B2%25D0%25B8%25D0%25BD%25D0%25B4%25D0%25B7%25D0%25BE%25D1%2580%2520%25D1%2581%25D0%25BF%25D0%25B1%26oq%3D%25D0%25BA%25D1%2583%25D0%25BF%25D0%25B8%25D1%2582%25D1%258C%2520%25D0%25BA%25D0%25B0%25D0%25BF%25D0%25BA%25D0%25B5%25D0%25B9%25D0%25BA%25D0%25B8%25208cQQRlUX%26gs_l%3Dserp.3.o..32.58329.0.98603.55.8.0.0.0.0.0.0..0.0....0...1c.1.64.serp..55.0.0.jDrNJUKQ')
        self.assertEqual(captcha['captcha_coninue'], 'https://www.google.ru/search?newwindow=1&espv=2&q=%D0%B2%D0%B8%D0%BD%D0%B4%D0%B7%D0%BE%D1%80%20%D1%81%D0%BF%D0%B1&oq=%D0%BA%D1%83%D0%BF%D0%B8%D1%82%D1%8C%20%D0%BA%D0%B0%D0%BF%D0%BA%D0%B5%D0%B9%D0%BA%D0%B8%208cQQRlUX&gs_l=serp.3.o..32.58329.0.98603.55.8.0.0.0.0.0.0..0.0....0...1c.1.64.serp..55.0.0.jDrNJUKQ')
        self.assertEqual(captcha['captcha_id'], '')
        self.assertEqual(captcha['q'], u'EgQfuMqHGKadm8IFIhkA8aeDSy6Evqypj5j85OIT5nrl-YB2Nl3HMgFj')

    def test44(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2016-12-15.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 927000)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'ПАО Соль Руси: отзывы сотрудников о работодателе, компания ...')
        self.assertEqual(res['sn'][0]['u'], u'http://pravda-sotrudnikov.ru/company/pao-sol-rusi')
        self.assertEqual(res['sn'][0]['d'], 'pravda-sotrudnikov.ru')

        self.assertEqual(res['sn'][99]['t'], u'Заработать денег. альфа брокер отзывы - Заработок в сети')
        self.assertEqual(res['sn'][99]['u'], u'http://xwebo.ru/search?q=%D0%B0%D0%BB%D1%8C%D1%84%D0%B0+%D0%B1%D1%80%D0%BE%D0%BA%D0%B5%D1%80+%D0%BE%D1%82%D0%B7%D1%8B%D0%B2%D1%8B')
        self.assertEqual(res['sn'][99]['d'], 'xwebo.ru')

        pe = GoogleParser.pagination_exists(html)
        self.assertTrue(pe)

    def test45(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-17.html')
        g = GoogleParser(html)
        self.assertTrue(g.is_recaptcha_suspicious_traffic())


        html = self.get_data('2016-12-15.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_recaptcha_suspicious_traffic())

        html = self.get_data('google-captcha-2016-12-06.html')
        g = GoogleParser(html)
        self.assertFalse(g.is_recaptcha_suspicious_traffic())

    def test46(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-24-5470000000.txt')
        g = GoogleJsonParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 5460000000)
        self.assertEqual(len(res['sn']), 49)

        self.assertEqual(res['sn'][0]['t'], u'Добро пожаловать | ВКонтакте')
        self.assertEqual(res['sn'][0]['u'], u'https://vk.com/')
        self.assertEqual(res['sn'][0]['d'], 'vk.com')

        self.assertEqual(res['sn'][48]['t'], u'Пора выбирать — Алексей Навальный')
        self.assertEqual(res['sn'][48]['u'], u'https://2018.navalny.com/')
        self.assertEqual(res['sn'][48]['d'], '2018.navalny.com')

        pe = GoogleParser.pagination_exists(g.content)
        self.assertTrue(pe)

    def test47(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-24-60100.txt')
        g = GoogleJsonParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 60000)
        self.assertEqual(len(res['sn']), 49)

        self.assertEqual(res['sn'][0]['t'], u'ываыва - YouTube')
        self.assertEqual(res['sn'][0]['u'], u'https://www.youtube.com/watch?v=mnXrfQ559NY')
        self.assertEqual(res['sn'][0]['d'], 'youtube.com')

        self.assertEqual(res['sn'][48]['t'], u'ываываыва ываыва - EuroShop')
        self.assertEqual(res['sn'][48]['u'], u'http://euroshop.kiev.ua/bytovaya-himiya')
        self.assertEqual(res['sn'][48]['d'], 'euroshop.kiev.ua')

        pe = GoogleParser.pagination_exists(g.content)
        self.assertTrue(pe)

    def test48(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-24-1600.txt')
        g = GoogleJsonParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 1600)
        self.assertEqual(len(res['sn']), 50)

        self.assertEqual(res['sn'][0]['t'], u'выаываыв - YouTube')
        self.assertEqual(res['sn'][0]['u'], u'https://www.youtube.com/watch?v=sDthlTYB1lA')
        self.assertEqual(res['sn'][0]['d'], 'youtube.com')

        self.assertEqual(res['sn'][49]['t'], u'выаываыв, Родионово-Несветайская / rusbody.com')
        self.assertEqual(res['sn'][49]['u'], u'http://rusbody.com/id12593')
        self.assertEqual(res['sn'][49]['d'], 'rusbody.com')

        pe = GoogleParser.pagination_exists(g.content)
        self.assertTrue(pe)

    def test49(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-24-820.txt')
        g = GoogleJsonParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 812)
        self.assertEqual(len(res['sn']), 50)

        self.assertEqual(res['sn'][0]['t'], u'Выаываыв Ываыва | ВКонтакте')
        self.assertEqual(res['sn'][0]['u'], u'https://vk.com/id79486428')
        self.assertEqual(res['sn'][0]['d'], 'vk.com')

        self.assertEqual(res['sn'][49]['t'], u'Все писатели и поэты - Вам сюда! - 31 страница » Ниндзя ...')
        self.assertEqual(res['sn'][49]['u'], u'https://jut.su/forum/dninjas/topic-31050-page-31.html')
        self.assertEqual(res['sn'][49]['d'], 'jut.su')

        pe = GoogleParser.pagination_exists(g.content)
        self.assertTrue(pe)

    def test50(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-24-50.txt')
        g = GoogleJsonParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 2870000)
        self.assertEqual(len(res['sn']), 50)

        self.assertEqual(res['sn'][0]['t'], u'Такси Владивосток | Заказать такси | Дешевое такси |Приложение ...')
        self.assertEqual(res['sn'][0]['u'], u'http://vlad.vostok-taxi.ru/')
        self.assertEqual(res['sn'][0]['d'], 'vlad.vostok-taxi.ru')

        self.assertEqual(res['sn'][49]['t'], u'Такси 2412 — Заказ такси через мобильное приложение или ...')
        self.assertEqual(res['sn'][49]['u'], u'http://taxi2412.ru/')
        self.assertEqual(res['sn'][49]['d'], 'taxi2412.ru')

        pe = GoogleParser.pagination_exists(g.content)
        self.assertTrue(pe)

    def test51(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-24-8.txt')
        g = GoogleJsonParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 8)
        self.assertEqual(len(res['sn']), 8)

        self.assertEqual(res['sn'][0]['t'], u'Главная - Инструмент Сервис')
        self.assertEqual(res['sn'][0]['u'], u'http://service124.ru/')
        self.assertEqual(res['sn'][0]['d'], 'service124.ru')

        self.assertEqual(res['sn'][7]['t'], u'Sibnet • Чат знакомств, онлайн общение')
        self.assertEqual(res['sn'][7]['u'], u'http://chat.sibnet.ru/?history&date=2007-10-30&all=1')
        self.assertEqual(res['sn'][7]['d'], 'chat.sibnet.ru')

        pe = GoogleParser.pagination_exists(g.content)
        self.assertFalse(pe)

    def test52(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-24-1.txt')
        g = GoogleJsonParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 1)
        self.assertEqual(len(res['sn']), 1)

        self.assertEqual(res['sn'][0]['t'], u'Продам все это! - BeOn')
        self.assertEqual(res['sn'][0]['u'], u'http://beon.ru/buy-sell/7664-873-prodam-vse-jeto-read.shtml')
        self.assertEqual(res['sn'][0]['d'], 'beon.ru')

        pe = GoogleParser.pagination_exists(g.content)
        self.assertFalse(pe)

    def test53(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-24-0.txt')
        g = GoogleJsonParser(html)
        self.assertFalse(g.is_suspicious_traffic())
        self.assertTrue(g.is_not_found())

        pe = GoogleParser.pagination_exists(g.content)
        self.assertFalse(pe)

    def test54(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-24-unicodeerror.txt')
        g = GoogleJsonParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 16100)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'UPVEL UR-315BN: Wi-Fi роутер стандарта 802.11n 150 Мбит/с с ...')
        self.assertEqual(res['sn'][0]['u'], u'http://upvel.ru/items/ur-315bn.html')
        self.assertEqual(res['sn'][0]['d'], 'upvel.ru')

        self.assertEqual(res['sn'][99]['t'], u'WiFi РОУТЕРЫ РОСТЕЛЕКОМ + Лучший провайдер WiFi Интернет ...')
        self.assertEqual(res['sn'][99]['u'], u'http://tv1.moscow/%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B5%D1%82-%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD/')
        self.assertEqual(res['sn'][99]['d'], 'tv1.moscow')

        pe = GoogleParser.pagination_exists(g.content)
        self.assertTrue(pe)

    def test55(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-27.txt')
        g = GoogleJsonParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 444000)
        self.assertEqual(len(res['sn']), 10)

        self.assertEqual(res['sn'][0]['t'], u'Автобусы Ульяновск - Нижний Новгород (от 1122 руб.)')
        self.assertEqual(res['sn'][0]['u'], u'https://www.avtovokzaly.ru/avtobus/ulyanovsk-nizhnij')
        self.assertEqual(res['sn'][0]['d'], 'avtovokzaly.ru')

        self.assertEqual(res['sn'][9]['t'], u'Расписание автобусов Ульяновск - Нижний Новгород - TMzilla.com')
        self.assertEqual(res['sn'][9]['u'], u'http://www.tmzilla.com/bus/destination-from-19-to-4.html')
        self.assertEqual(res['sn'][9]['d'], 'tmzilla.com')

        pe = GoogleParser.pagination_exists(g.content)
        self.assertTrue(pe)

    def test56(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-28.txt')
        g = GoogleJsonParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 595000)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'ПАО «СОЛЬ РУСИ»')
        self.assertEqual(res['sn'][0]['u'], u'http://solrusi.ru/')
        self.assertEqual(res['sn'][0]['d'], 'solrusi.ru')

        self.assertEqual(res['sn'][99]['t'], u'История соли - Соль: история и факты')
        self.assertEqual(res['sn'][99]['u'], u'http://www.o-soli.ru/istoriya-soli/')
        self.assertEqual(res['sn'][99]['d'], 'o-soli.ru')

        pe = GoogleParser.pagination_exists(g.content)
        self.assertTrue(pe)

    def test57(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-03-28.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm', 'h'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 595000)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'ПАО «СОЛЬ РУСИ»')
        self.assertEqual(res['sn'][0]['u'], u'http://solrusi.ru/')
        self.assertEqual(res['sn'][0]['d'], 'solrusi.ru')
        self.assertEqual(res['sn'][0]['vu'], u'solrusi.ru/')
        self.assertTrue('h' in res['sn'][0] and res['sn'][0]['h'])

        self.assertEqual(res['sn'][99]['t'], u'История соли - Соль: история и факты')
        self.assertEqual(res['sn'][99]['u'], u'http://www.o-soli.ru/istoriya-soli/')
        self.assertEqual(res['sn'][99]['d'], 'o-soli.ru')
        self.assertEqual(res['sn'][99]['vu'], u'www.o-soli.ru/istoriya-soli/')
        self.assertTrue('h' in res['sn'][99] and res['sn'][99]['h'])

        pe = GoogleParser.pagination_exists(g.content)
        self.assertTrue(pe)

    def test58(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('mobile-2017-06-01.html')
        g = GoogleMobileParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], None)
        self.assertEqual(len(res['sn']), 50)

        self.assertEqual(res['sn'][0]['t'], u'Обеденные столы для кухни - купить обеденный стол от ...')
        self.assertEqual(res['sn'][0]['s'], u'Mebelvia.ru предлагает обеденные столы от производителя в Москве. Вы можете купить обеденный стол с ...')
        self.assertEqual(res['sn'][0]['u'], u'http://mebelvia.ru/katalog/kuhni_i_stolovye_gruppy/obedennie_stoli/')
        self.assertEqual(res['sn'][0]['d'], 'mebelvia.ru')
        self.assertEqual(res['sn'][0]['vu'], u'mebelvia.ru › katalog › obedennie_stoli')

        self.assertEqual(res['sn'][49]['t'], u'куплю стол. Мебель. Столы и стулья. Южно-Сахалинск. Объявления Сахалина')
        self.assertEqual(res['sn'][49]['s'], u'8 февр. 2017 г. - куплю маникюрный стол или стол подходящий для работы с клиентом, обязательно со шкафчиками в пределах 3000 тысяч предложение писать в ватсап ...')
        self.assertEqual(res['sn'][49]['u'], u'https://market.sakh.com/1698962.html')
        self.assertEqual(res['sn'][49]['d'], 'market.sakh.com')
        self.assertEqual(res['sn'][49]['vu'], u'https://market.sakh.com › ...')

        pe = GoogleMobileParser.pagination_exists(html)
        self.assertTrue(pe)

    def test59(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('mobile-2017-06-01-1.html')
        g = GoogleMobileParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], None)
        self.assertEqual(len(res['sn']), 5)

        self.assertEqual(res['sn'][0]['t'], u'Обеденные столы. Купить стол обеденный в Москве - MKS-shop.ru')
        self.assertEqual(res['sn'][0]['s'], u'Магазин MKS-shop предлагает большой выбор обеденных столов по выгодным ценам. Тел: 8 (800) 555- 75-12.')
        self.assertEqual(res['sn'][0]['u'], u'http://www.mks-shop.ru/catalog/obedennye_stoly/')
        self.assertEqual(res['sn'][0]['d'], 'mks-shop.ru')

        self.assertEqual(res['sn'][4]['t'], u'Каталог обеденных столов за массива дерева от компании &quot;Стелла&quot; - Spbmebel.ru')
        self.assertEqual(res['sn'][4]['s'], u'Обеденные столы из массива для дома, бара, ресторана и кафе от мебельной фабрики Стелла! ..... Вы можете выбрать понравившуюся модель из каталога или заказать уникальный стол, сделанный в ...')
        self.assertEqual(res['sn'][4]['u'], u'http://www.spbmebel.ru/catalog/obed')
        self.assertEqual(res['sn'][4]['d'], 'spbmebel.ru')

        self.assertFalse(GoogleMobileParser.pagination_exists(html))

    def test60(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('mobile-2017-06-01-2.html')
        g = GoogleMobileParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 0)
        self.assertFalse(GoogleMobileParser.pagination_exists(html))

    def test61(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('mobile-2017-06-01-3.html')
        g = GoogleMobileParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], None)
        self.assertEqual(len(res['sn']), 8)

        self.assertEqual(res['sn'][0]['t'], u'фывафыва фывафыва - Одноклассники')
        self.assertEqual(res['sn'][0]['s'], u'8 июл. 2016 г. - фывафыва фывафыва. 20 лет. Место проживания - Москва, Россия.')
        self.assertEqual(res['sn'][0]['u'], u'https://m.ok.ru/profile/559406806336')
        self.assertEqual(res['sn'][0]['d'], 'm.ok.ru')

        self.assertEqual(res['sn'][1]['t'], u'Фывафыва Фывафыва | ВКонтакте')
        self.assertEqual(res['sn'][1]['s'], u'Фывафыва Фывафыва, Harare, Зимбабве. Окончил школу Школа изучения системы игры в Counter-strike 1.6 в 2010, Harare. Войдите на сайт или зарегистрируйтесь, чтобы связаться с Фывафывой ...')
        self.assertEqual(res['sn'][1]['u'], u'https://m.vk.com/0x00dec0de')
        self.assertEqual(res['sn'][1]['d'], 'm.vk.com')

        self.assertEqual(res['sn'][2]['t'], u'Необычное слово «фывафыва»')
        self.assertEqual(res['sn'][2]['s'], u'Боимся, что слова фывафыва не существует. Если фывафыва существует, то мы Вам скорее всего ничем не поможем в поиске фывафыва. Но мы позволим себе предположить, что вы искали не ...')
        self.assertEqual(res['sn'][2]['u'], u'http://bird-phoenix.ru/ru/fyvafyva.html')
        self.assertEqual(res['sn'][2]['d'], 'bird-phoenix.ru')

        self.assertEqual(res['sn'][7]['t'], u'фывафыва - Pikabu')
        self.assertEqual(res['sn'][7]['s'], u'фывафыва. добавить тег. Любые посты за всё время, сначала свежее, с рейтингом больше 25. Текст. Картинки. Видео. Тег [Моё]. Свежее. Лучшие. Найти посты. сбросить. загрузка... ... Посты не найдены.')
        self.assertEqual(res['sn'][7]['u'], u'http://m.pikabu.ru/tag/%F4%FB%E2%E0%F4%FB%E2%E0/hot')
        self.assertEqual(res['sn'][7]['d'], 'm.pikabu.ru')

        self.assertTrue(GoogleMobileParser.pagination_exists(html))

    def test62(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('mobile-2017-06-01-4.html')
        g = GoogleMobileParser(html)
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], None)
        self.assertEqual(len(res['sn']), 1)

        self.assertEqual(res['sn'][0]['t'], u'Купить стол — Только хорошая мебель')
        self.assertEqual(res['sn'][0]['s'], u'5 дек. 2016 г. - Mebelvia.ru предлагает обеденные столы от производителя в Москве. Вы можете купить ...')
        self.assertEqual(res['sn'][0]['u'], u'http://vyborkreslodoma.byethost7.com/2016/12/05/kupit-stol/')
        self.assertEqual(res['sn'][0]['d'], 'vyborkreslodoma.byethost7.com')

        self.assertFalse(GoogleMobileParser.pagination_exists(html))

    def test63(self):
        u""""
            Парсинг html-описания
        """
        html = self.get_data('snippet-2017-06-30.html')
        html_descr = SnippetsParserDefault.get_html_descr(html)
        self.assertEqual(html_descr, '<span class="st">Mebelvia.ru предлагает обеденные столы от производителя в Москве. Вы можете купить обеденный <em>стол</em> с доставкой и заказать сборку. Самые низкие&nbsp;...</span>')

    def test64(self):
        u""""
            Парсинг html-описания
        """
        html = self.get_data('snippet-2017-06-30-1.html')
        html_descr = SnippetsParserDefault.get_html_descr(html)
        self.assertEqual(html_descr, '<span class="st"><span class="f">12 дек. 2011 г. - </span><em>Фотографии</em> из частного альбомы <em>Леди Гага</em>, такая милая девушка превратилась не пойми в кого.</span>')

    def test65(self):
        u""""
            Парсинг html-описания
        """
        html = self.get_data('snippet-2017-06-30-2.html')
        html_descr = SnippetsParserDefault.get_html_descr(html)
        self.assertEqual(html_descr, '<span class="st"><em>Детские комнаты</em> в разных странах мира (43 <em>фото</em>). Автор: Fuchsia. 04 марта 2015 12:24. Метки: дети комната мир. 9528. 43. Миллионы детей в разных&nbsp;...</span>')

    def test66(self):
        u""""
            Проверка подозрительной выдачи
        """
        html = self.get_data('2017-07-06.html')
        g = GoogleParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm', 'h'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 79500)
        self.assertEqual(len(res['sn']), 50)

        self.assertEqual(res['sn'][0]['t'], u'Домашние блендеры BORK для смузи и коктейлей - купить ...')
        self.assertEqual(res['sn'][0]['s'], u'Главной особенностью домашних блендеров BORK является высокая мощность и удобство приготовления коктейле, смузи и других полезных напитков.')
        self.assertEqual(res['sn'][0]['u'], u'http://www.bork.ru/eShop/Blenders/')
        self.assertEqual(res['sn'][0]['d'], 'bork.ru')
        self.assertEqual(res['sn'][0]['vu'], u'www.bork.ru/eShop/Blenders/')
        self.assertTrue('h' in res['sn'][0] and res['sn'][0]['h'])

        self.assertEqual(res['sn'][49]['t'], u'Блендер Bork (Борк) - цена в интернет-магазине, отзывы ...')
        self.assertEqual(res['sn'][49]['s'], u'Идеальное измельчение и смешивание за считанные секунды - легко. Блендер B780 от Bork поможет добиться нежнейшей консистенции супов-пюре, ...')
        self.assertEqual(res['sn'][49]['u'], u'http://blender.tkat.ru/vendor/BORK/')
        self.assertEqual(res['sn'][49]['d'], 'blender.tkat.ru')
        self.assertEqual(res['sn'][49]['vu'], u'blender.tkat.ru/vendor/BORK/')
        self.assertTrue('h' in res['sn'][49] and res['sn'][49]['h'])

        pe = GoogleParser.pagination_exists(g.content)
        self.assertTrue(pe)

    def test67(self):
        u""""
            Пустая выдача info:stekswood.ru/product/banketka-chippendejl-bejs/
        """
        html = self.get_data('2017-11-20.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm', 'h'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 0)

    def test68(self):
        u""""
            Выдача из одного результата info:bdbd.ru
        """
        html = self.get_data('2017-11-20-1.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm', 'h'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 1)

        self.assertEqual(res['sn'][0]['t'], u'Продвижение сайтов в поисковых системах, seo раскрутка сайтов ...')
        self.assertEqual(res['sn'][0]['s'], u'Продвижение сайтов в поисковых системах Яндекс и Google. Эффективное увеличение продаж и продвижение сайта от bdbd.ru с оплатой за ...')
        self.assertEqual(res['sn'][0]['u'], u'http://www.bdbd.ru/')
        self.assertEqual(res['sn'][0]['d'], 'bdbd.ru')
        self.assertEqual(res['sn'][0]['vu'], u'www.bdbd.ru/')

    def test69(self):
        u""""
            Убираем порт из домена
        """
        html = self.get_data('2017-11-22.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm', 'h'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 404000)

        self.assertEqual(res['sn'][0]['t'], u'Керамическая брусчатка Керамейя. Низкая цена от завода ...')
        self.assertEqual(res['sn'][0]['s'], u'В ТД Кирпичный Двор вы можете купить керамическую брусчатку завода Керамейя с доставкой. Низкая цена от завода производителя!')
        self.assertEqual(res['sn'][0]['u'], u'http://kirpdvor.ru/katalog_produktsii/klinkernaya_bruschatka/kerameyya/bruschatka_kerameyya_brukkeram_oniks_234/')
        self.assertEqual(res['sn'][0]['d'], 'kirpdvor.ru')
        self.assertEqual(res['sn'][0]['vu'], u'kirpdvor.ru/katalog_produktsii/.../bruschatka_kerameyya_brukkeram_oniks_234/')

        self.assertEqual(res['sn'][23]['t'], u'Кирпич и Кровля . Керамические блоки, клинкерная плитка ...')
        self.assertEqual(res['sn'][23]['s'], u'Кирпич и Кровля. Керамические блоки, клинкерная плитка, керамическая черепица, брусчатка, клинкерный, облицовочный кирпич, тротуарная плитка, ...')
        self.assertEqual(res['sn'][23]['u'], u'http://xn--e1aicmebjeik.xn--p1ai:8080/')
        self.assertEqual(res['sn'][23]['d'], 'xn--e1aicmebjeik.xn--p1ai')
        self.assertEqual(res['sn'][23]['vu'], u'реконстрой.рф:8080/')

        self.assertEqual(res['sn'][98]['t'], u'Немецкий клинкер Фелдхаус Клинкер :: Feldhaus Klinker ...')
        self.assertEqual(res['sn'][98]['s'], u'По сравнению с обычными изделиями из группы строительной грубой керамики (обыкновенная керамическая плитка, кирпич и т.д.) брусчатка клинкер ...')
        self.assertEqual(res['sn'][98]['u'], u'http://www.feldhaus-kama.ru/')
        self.assertEqual(res['sn'][98]['d'], 'feldhaus-kama.ru')
        self.assertEqual(res['sn'][98]['vu'], u'www.feldhaus-kama.ru/')

    def test70(self):
        u""""
            Ошибка парсинга от 2018-08-01
        """
        html = self.get_data('2018-08-01.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 9290)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'Массаж на Новослободской:(495)786-97-98, ул ... - Целлюлайт')
        self.assertEqual(res['sn'][0]['s'], u'9 мая 2018 г. - Массаж на Новослободской. Адрес клиники косметологии которая поможет Вам привести Вашу фигуру к идеальным формам.')
        self.assertEqual(res['sn'][0]['u'], u'https://www.cellulait.ru/contacts/')
        self.assertEqual(res['sn'][0]['d'], 'cellulait.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.cellulait.ru/contacts/')

        self.assertEqual(res['sn'][99]['t'], u'Целлюлайт: Москва Новослободская улица 61с1 - RusMap.net')
        self.assertEqual(res['sn'][99]['s'], u'Салоны красоты: Целлюлайт находится по адресу Москва Новослободская улица 61с1, время работы: пн-сб 09:00-21:00; вс 10:00-19:00.')
        self.assertEqual(res['sn'][99]['u'], u'https://rusmap.net/%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0/%D0%A4%D0%B8%D1%80%D0%BC%D0%B0/53922')
        self.assertEqual(res['sn'][99]['d'], 'rusmap.net')
        self.assertEqual(res['sn'][99]['vu'], u'https://rusmap.net › Москва › Фирмы › Салоны красоты')

    def test71(self):
        u""""
            Ошибка парсинга от 2018-08-01
        """
        html = self.get_data('2018-11-06.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 1160000)
        self.assertEqual(len(res['sn']), 48)

        self.assertEqual(res['sn'][0]['t'], u'Посуда Fissler – купить посуду Фисслер в Москве, цены в ...')
        self.assertEqual(res['sn'][0]['s'], u'В интернет-магазине компании Сандер в Москве представлен ассортимент немецкой посуды для индукционных плит Fissler. Она удовлетворит вкусы ...')
        self.assertEqual(res['sn'][0]['u'], u'http://www.fissler-shop.ru/')
        self.assertEqual(res['sn'][0]['d'], 'fissler-shop.ru')
        self.assertEqual(res['sn'][0]['vu'], u'www.fissler-shop.ru/')

        self.assertEqual(res['sn'][47]['t'], u'Наборы посуды для готовки — купить на Яндекс.Маркете')
        self.assertEqual(res['sn'][47]['s'], u'FISSLER Набор посуды из 5-ти предметов: три кастрюли, сотейник и ковшик без ... наборы посуды и кастрюль Fissler Набор кастрюль, 5 предметов, ...')
        self.assertEqual(res['sn'][47]['u'], u'https://market.yandex.ru/catalog--nabory-posudy-dlia-gotovki/61640/list?glfilter=7893318%3A10713559')
        self.assertEqual(res['sn'][47]['d'], 'market.yandex.ru')
        self.assertEqual(res['sn'][47]['vu'], u'https://market.yandex.ru/catalog--nabory-posudy-dlia-gotovki/61640/list?glfilter...')

    def test72(self):
        u""""
            Ошибка парсинга от 2018-08-01
        """
        html = self.get_data('2018-12-05.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 4180)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'Флавитал инструкция по применению, Флавитал цена, Флавитал ...')
        self.assertEqual(res['sn'][0]['s'], u'Цены на Флавитал, подробная инструкция по применению, противопоказания, побочные действия, состав на сайте интернет-аптеки www.piluli.ru.')
        self.assertEqual(res['sn'][0]['u'], u'https://www.piluli.ru/product/flavital')
        self.assertEqual(res['sn'][0]['d'], 'piluli.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.piluli.ru › ... › Лечение онкологических заболеваний')

        self.assertEqual(res['sn'][98]['t'], u'Flavital - Profile - Roblox')
        self.assertEqual(res['sn'][98]['s'], u'Flavital is one of the millions playing, creating and exploring the endless possibilities of Roblox. Join Flavital on Roblox and explore together!')
        self.assertEqual(res['sn'][98]['u'], u'https://www.roblox.com/users/529521610/profile')
        self.assertEqual(res['sn'][98]['d'], 'roblox.com')
        self.assertEqual(res['sn'][98]['vu'], u'https://www.roblox.com/users/529521610/profile')

    def test73(self):
        u""""
            Ошибка парсинга от 2018-12-06
        """
        html = self.get_data('2018-12-06.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 606000)
        self.assertEqual(len(res['sn']), 97)

        self.assertEqual(res['sn'][0]['t'], u'ВТБ Капитал Управление активами. Искусство инвестиций ...')
        self.assertEqual(res['sn'][0]['s'], u'Управление активами, паевые инвестиционные фонды, индивидуальное доверительное управление, портфельные инвестиции -управляющая ...')
        self.assertEqual(res['sn'][0]['u'], u'https://www.vtbcapital-am.ru/')
        self.assertEqual(res['sn'][0]['d'], 'vtbcapital-am.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.vtbcapital-am.ru/')

        self.assertEqual(res['sn'][95]['t'], u'КоммерсантЪ 18 - Страница 8 - Результат из Google Книги')
        self.assertEqual(res['sn'][95]['s'], u'6% 24 2,36% 10,5 20,5 Процентное изменение за торговый день Диапазон ... с фиксированной доходностью «Ренессанс управление активами» Елены ... капитала «ВТБ Капитал» Андрей Соловьев. Как отмечает руководитель ...')
        self.assertEqual(res['sn'][95]['u'], u'https://books.google.ru/books?id=oPeyCQAAQBAJ&pg=PA8&lpg=PA8&dq=%D0%B2%D1%82%D0%B1-24+%D0%BA%D0%B0%D0%BF%D0%B8%D1%82%D0%B0%D0%BB+%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5+%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D0%B0%D0%BC%D0%B8&source=bl&ots=08cc8Bm0T-&sig=H2tYDs_jv7Oycye-SNmhptY4eS8&hl=ru&sa=X&sqi=2&ved=2ahUKEwj16OX8jYvfAhV-AxAIHc-NBO4Q6AEwaHoECGsQAQ')
        self.assertEqual(res['sn'][95]['d'], 'books.google.ru')
        self.assertEqual(res['sn'][95]['vu'], u'https://books.google.ru/books?isbn=5457804208')

        self.assertEqual(res['sn'][96]['t'], u'Отставки и назначения — Bankir.Ru - Банкир.ру')
        self.assertEqual(res['sn'][96]['s'], u'24, 25, 26, 27, 28, 29, 30. 31, 1, 2, 3, 4, 5, 6 ... В компании «Сбербанк Управление активами» произошли новые назначения ... Лариса Жигирева назначена управляющим розничного бизнеса ВТБ в Псковской области ... Геннадий Ходарин занял пост гендиректора Группы «КапиталЪ Управление активами».')
        self.assertEqual(res['sn'][96]['u'], u'https://bankir.ru/novosti/otstavki-i-naznacheniya/?p=96')
        self.assertEqual(res['sn'][96]['d'], 'bankir.ru')
        self.assertEqual(res['sn'][96]['vu'], u'https://bankir.ru/novosti/otstavki-i-naznacheniya/?p=96')

    def test74(self):
        u""""
            Ошибка парсинга от 2019-08-19
        """
        html = self.get_data('2019-08-19.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()
        self.assertEqual(res['pc'], 3460000)
        self.assertEqual(len(res['sn']), 50)

        self.assertEqual(res['sn'][0]['t'], u'Диваны – купить диван от производителя в Москве с доставкой на ...')
        self.assertEqual(res['sn'][0]['s'], u'Диваны - 402 модели от 6420₽. Гарантия лучшей цены. Дешевая доставка по Москве и области. Бесплатный подъем на лифте.')
        self.assertEqual(res['sn'][0]['u'], u'https://mebelvia.ru/katalog/myagkaya_mebel/divany/')
        self.assertEqual(res['sn'][0]['d'], 'mebelvia.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://mebelvia.ru/katalog/myagkaya_mebel/divany/')

        self.assertEqual(res['sn'][49]['t'], u'Угловой диван Сиэтл 8 Марта | Купить угловой диван Сиэтл с ...')
        self.assertEqual(res['sn'][49]['s'], u'Продажа угловой диван Сиэтл - цена от производителя 8 Марта. Интернет-магазин мебели: угловые диваны на заказ и большой выбор готовых ...')
        self.assertEqual(res['sn'][49]['u'], u'https://www.8marta.ru/catalog/8marta/divany-uglovye/sietl.htm')
        self.assertEqual(res['sn'][49]['d'], '8marta.ru')
        self.assertEqual(res['sn'][49]['vu'], u'https://www.8marta.ru › Основная коллекция › Угловые диваны')

    def test75(self):
        u""""
            Ошибка парсинга от 2019-08-29
        """
        html = self.get_data('mobile-2019-08-29.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже не общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'Плюсы и минусы открытого и закрытого синус-лифтинга')
        self.assertEqual(res['sn'][0]['s'], u"""Когда применяется открытый синус-лифтинг, а когда закрытый? Какие костные материалы 
используются? Можно ли проводить имплантацию сразу после синус-лифтинга?""")
        self.assertEqual(res['sn'][0]['u'], u'https://akademstom.ru/articles/sinus-lifting/')
        self.assertEqual(res['sn'][0]['d'], 'akademstom.ru')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][8]['t'], u'открытый синус-лифтинг Импро - YouTube')
        self.assertEqual(res['sn'][8]['s'], None)
        self.assertEqual(res['sn'][8]['u'], u'https://m.youtube.com/watch?v=6NWtKBe77JA')
        self.assertEqual(res['sn'][8]['d'], 'm.youtube.com')
        self.assertEqual(res['sn'][8]['vu'], None)

        self.assertEqual(res['sn'][98]['t'], u'Синус лифтинг открытый и закрытый - Стеллит')
        self.assertEqual(res['sn'][98]['s'], u"""Синус лифтинг, открытый или закрытый – это операция, которая проводится на верхней челюсти для 
того, чтобы подготовить альвеолярный отросток к установке имплантата. Верхнечелюстная кость внутри
 ...""")
        self.assertEqual(res['sn'][98]['u'], u'https://www.stellit-spb.com/sinus-lifting-otkrytyj-i-zakrytyj')
        self.assertEqual(res['sn'][98]['d'], 'stellit-spb.com')
        self.assertEqual(res['sn'][98]['vu'], None)

    def test76(self):
        u""""
            Ошибка парсинга от 2019-08-29
        """
        html = self.get_data('mobile-2019-08-29-1.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'Связь-Банк > «Военная ипотека»')
        self.assertEqual(res['sn'][0]['s'], u'«Военная ипотека» – специальная программа, разработанная в соответствии с Федеральным ... НИС ( накопительно-ипотечной системы) может приобрести недвижимость с использованием ипотечного ...')
        self.assertEqual(res['sn'][0]['u'], 'https://www.sviaz-bank.ru/service/hypotec-new/military/')
        self.assertEqual(res['sn'][0]['d'], 'sviaz-bank.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.sviaz-bank.ru › military')

        self.assertEqual(res['sn'][1]['t'], u'Связь-Банк > Калькулятор. Военная ипотека')
        self.assertEqual(res['sn'][1]['s'], u'Военная ипотека. Расчет ипотечного калькулятора является предварительным. Чтобы выбрать наиболее подходящий Вам вариант получения денежных средств и узнать точный размер Вашего кредита ...')
        self.assertEqual(res['sn'][1]['u'], 'https://www.sviaz-bank.ru/service/hypotec-new/calc-mil-credit/')
        self.assertEqual(res['sn'][1]['d'], 'sviaz-bank.ru')
        self.assertEqual(res['sn'][1]['vu'], 'https://www.sviaz-bank.ru')

        self.assertEqual(res['sn'][2]['t'], u'Связь банк: военная ипотека и её условия в 2019 году')
        self.assertEqual(res['sn'][2]['s'], u'20 авг. 2018 г. · Военная ипотека Связь-банка 2019: Размер максимальной суммы ипотечного кредита военнослужащему, процентная ставка, условия, калькулятор и отзывы клиентов.')
        self.assertEqual(res['sn'][2]['u'], 'https://ipotekaved.ru/voennaya/ipoteka-svyaz-bank.html')
        self.assertEqual(res['sn'][2]['d'], 'ipotekaved.ru')
        self.assertEqual(res['sn'][2]['vu'], u'https://ipotekaved.ru › voennaya › i...')

        self.assertEqual(res['sn'][3]['t'], u'Военная ипотека от Связь-Банка - Молодострой')
        self.assertEqual(res['sn'][3]['s'], u'Аккредитованные новостройки Связь-Банка по военной ипотеке. Скидки участникам Молодостроя.')
        self.assertEqual(res['sn'][3]['u'], 'https://www.molodostroy24.ru/voennaya-ipoteka-novostroyki/svyazbank/')
        self.assertEqual(res['sn'][3]['d'], 'molodostroy24.ru')
        self.assertEqual(res['sn'][3]['vu'], u'https://www.molodostroy24.ru › svy...')

        self.assertEqual(res['sn'][4]['t'], u'Список банков работающих по военной ипотеке - условия, дополнительный кредит военнослужащим, сумма, проценты - Молодострой')
        self.assertEqual(res['sn'][4]['s'], u'Условия Военной ипотеки (по состоянию на 1 августа 2019 года) .... ставка от 11,9%. Максимальная сумма по военной ипотеке - 3 100 000 рублей. Возможно рефинансирование. СвязьБанк. от 9.4%. 2,70 ...')
        self.assertEqual(res['sn'][4]['u'], 'https://www.molodostroy24.ru/voennaya_ipoteka/banki/')
        self.assertEqual(res['sn'][4]['d'], 'molodostroy24.ru')
        self.assertEqual(res['sn'][4]['vu'], 'https://www.molodostroy24.ru')

        self.assertEqual(res['sn'][99]['t'], u'Купить квартиру по программе военной ипотеки в Санкт-Петербурге можно по ставке от 9% годовых - Novostroy-Spb.ru')
        self.assertEqual(res['sn'][99]['s'], u'11 июл. 2018 г. · Для получения предложения по военной ипотеке можно обратиться напрямую в банк или к ... по развитию розничного бизнеса Санкт-Петербургского филиала ПАО АКБ «Связь-Банк».')
        self.assertEqual(res['sn'][99]['u'], 'https://www.novostroy-spb.ru/statyi/voennaya_ipoteka_v_novostroykah')
        self.assertEqual(res['sn'][99]['d'], 'novostroy-spb.ru')
        self.assertEqual(res['sn'][99]['vu'], u'https://www.novostroy-spb.ru › statyi')

    def test77(self):
        u""""
            Ошибка парсинга от 2019-09-02
        """
        html = self.get_data('mobile-2019-09-02.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 0)

    def test78(self):
        u""""
            Ошибка парсинга от 2019-09-02
        """
        html = self.get_data('mobile-2019-09-02-1.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'Метро Автозаводская - Москва - Карты метро')
        self.assertEqual(res['sn'][0]['s'], u'Карты и станции метро - быстрый поиск станций на карте. ... карта метро Москва расположение станции ^ Станция "Автозаводская" на карте метро, Москва ^ карта станции метро Автозаводская ^ Карта ...')
        self.assertEqual(res['sn'][0]['u'], 'http://metro.umka.org/map-moscow/2-zamoskvoreckaya-liniya/avtozavodskaya.html')
        self.assertEqual(res['sn'][0]['d'], 'metro.umka.org')
        self.assertEqual(res['sn'][0]['vu'], u'metro.umka.org › avtozavodskaya')

        self.assertEqual(res['sn'][98]['t'], u'Росреестр')
        self.assertEqual(res['sn'][98]['s'], u'Москва. Личный кабинет. единый справочный телефон: 8 (800) 100-34-34. Звонок из регионов России бесплатный. Телефон доверия: (495) 917-38-25 ... Публичная кадастровая карта · Планы и результаты ...')
        self.assertEqual(res['sn'][98]['u'], 'https://rosreestr.ru/site/')
        self.assertEqual(res['sn'][98]['d'], 'rosreestr.ru')
        self.assertEqual(res['sn'][98]['vu'], u'https://rosreestr.ru › site')

    def test79(self):
        u""""
            Ошибка парсинга от 2019-09-02
        """
        html = self.get_data('mobile-2019-09-02-2.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 1)

        self.assertEqual(res['sn'][0]['t'], u'Ну вот и мой блог!: «Зелёный Марафон» продлится 10 часов')
        self.assertEqual(res['sn'][0]['s'], u'ЯРОСЛАВЛЬ, 30 мая — РИА Новости. Ярославский священник Алексей Кириллов попросил мэрию Ярославля отказаться от проведения праздника, где ...')
        self.assertEqual(res['sn'][0]['u'], 'http://voronkingoepesos.blogspot.com/2019/05/10_30.html')
        self.assertEqual(res['sn'][0]['d'], 'voronkingoepesos.blogspot.com')
        self.assertEqual(res['sn'][0]['vu'], u'voronkingoepesos.blogspot.com › 2...')

    def test80(self):
        u""""
            Ошибка парсинга от 2019-09-02
        """
        html = self.get_data('mobile-2019-09-02-3.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 94)

        self.assertEqual(res['sn'][0]['t'], u'График USD TRY – Investing.com')
        self.assertEqual(res['sn'][0]['s'], u'Получите мгновенный доступ к бесплатному потоковому графику USD TRY. Этот уникальный график Доллар США Турецкая лира позволяет четко наблюдать за поведением этой пары.')
        self.assertEqual(res['sn'][0]['u'], 'https://m.ru.investing.com/currencies/usd-try-chart')
        self.assertEqual(res['sn'][0]['d'], 'm.ru.investing.com')
        self.assertEqual(res['sn'][0]['vu'], u'https://m.ru.investing.com › usd-try-...')

        self.assertEqual(res['sn'][93]['t'], u'[Beaches] курс доллара к турецкой лире график за год')
        self.assertEqual(res['sn'][93]['s'], u'курс доллара к турецкой лире график за год album. USD TRY – Курс и график Доллар Лира — TradingView pic. USD TRY – Курс и график Доллар Лира — TradingView pic. Курс Доллара США к Турецкой лире ...')
        self.assertEqual(res['sn'][93]['u'], 'https://chekol.info/photos/%D0%BA%D1%83%D1%80%D1%81-%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0-%D0%BA-%D1%82%D1%83%D1%80%D0%B5%D1%86%D0%BA%D0%BE%D0%B9-%D0%BB%D0%B8%D1%80%D0%B5-%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA-%D0%B7%D0%B0-%D0%B3%D0%BE%D0%B4')
        self.assertEqual(res['sn'][93]['d'], 'chekol.info')
        self.assertEqual(res['sn'][93]['vu'], u'https://chekol.info › photos › курс-...')

    def test81(self):
        u""""
            Ошибка парсинга от 2019-09-02
        """
        html = self.get_data('mobile-2019-09-02-4.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], 'Convert SGD/JPY. Singapore Dollar to Japan Yen - XE')
        self.assertEqual(res['sn'][0]['s'], u'22 авг. 2019 г. · Convert 1 Singapore Dollar to Japanese Yen. Get live exchange rates, historical rates & charts for SGD to JPY with XE\'s free currency calculator.')
        self.assertEqual(res['sn'][0]['u'], 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=SGD&To=JPY')
        self.assertEqual(res['sn'][0]['d'], 'xe.com')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.xe.com › convert › To=...')

        self.assertEqual(res['sn'][98]['t'], 'The Foreign Exchange and Money Markets Guide')
        self.assertEqual(res['sn'][98]['s'], u'If in the preceding case it had been Singapore that had been on holiday on the 8th, the USD/SGD rate would ... We therefore have: USD/JPY 131.25/131.30 (May 9) 120/100 (May 9–June 10) USD/SGD 1.8770/1.8780 ...')
        self.assertEqual(res['sn'][98]['u'], 'https://books.google.ru/books?id=KS_5pRVfH_EC&pg=PA215&lpg=PA215&dq=sgd+jpy&source=bl&ots=JEYIPqqDrl&sig=ACfU3U0vkKkAP0zeykJw_vmgiGdbbRKcKg&hl=ru&sa=X&sqi=2&ved=2ahUKEwjDldqTt7LkAhWJiVwKHbi4BoIQ6AEwbXoECEoQAQ')
        self.assertEqual(res['sn'][98]['d'], 'books.google.ru')
        self.assertEqual(res['sn'][98]['vu'], u'https://books.google.ru › books')

    def test82(self):
        u""""
            Ошибка парсинга от 2019-09-02
        """
        html = self.get_data('mobile-2019-09-02-5.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 98)

        self.assertEqual(res['sn'][0]['t'], u'FB | Акции Facebook - Investing.com')
        self.assertEqual(res['sn'][0]['s'], u'Получите подробную информацию о акциях Facebook Inc (FB) включая Цену, Графики, Теханализ, Исторические данные, Отчеты и др. Facebook.')
        self.assertEqual(res['sn'][0]['u'], 'https://m.ru.investing.com/equities/facebook-inc')
        self.assertEqual(res['sn'][0]['d'], 'm.ru.investing.com')
        self.assertEqual(res['sn'][0]['vu'], u'https://m.ru.investing.com › equities')

        self.assertEqual(res['sn'][97]['t'], u'Обвал акций Facebook на 26% - в чем причина - Страна')
        self.assertEqual(res['sn'][97]['s'], u'26 июл. 2018 г. · Facebook не выполнил показателей ни по прибыли, ни по пользователям, поэтому его акции обвалились.')
        self.assertEqual(res['sn'][97]['u'], 'https://amp.strana.ua/news/153046-aktsii-facebook-rekordno-upali-posle-razhromnoho-otcheta-o-sostojanii-kompanii.html')
        self.assertEqual(res['sn'][97]['d'], 'amp.strana.ua')
        self.assertEqual(res['sn'][97]['vu'], u'https://strana.ua › news › 15304...')

    def test83(self):
        u""""
            Ошибка парсинга от 2019-09-02
        """
        html = self.get_data('mobile-2019-09-02-6.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'Платформа MetaTrader 4 для анализа котировок и торговли на Форексе')
        self.assertEqual(res['sn'][0]['s'], u'MetaTrader 4 — это бесплатная торговая платформа, предназначенная для торговли на рынке Форекс. Широкие аналитические возможности, гибкая торговая система, алгоритмический и мобильный ...')
        self.assertEqual(res['sn'][0]['u'], 'https://www.metatrader4.com/ru')
        self.assertEqual(res['sn'][0]['d'], 'metatrader4.com')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.metatrader4.com › ...')

        self.assertEqual(res['sn'][95]['t'], u'Язык программирования MQL5: Продвинутое использование ...')
        self.assertEqual(res['sn'][95]['s'], None)
        self.assertEqual(res['sn'][95]['u'], 'https://books.google.ru/books?id=ROSYDwAAQBAJ&pg=PT171&lpg=PT171&dq=%D0%BC%D0%B5%D1%82%D0%B0%D1%82%D1%80%D0%B5%D0%B9%D0%B4%D0%B5%D1%80&source=bl&ots=EtMdmWWB9c&sig=ACfU3U2barZH6UJb8CzQPz6v4u7YTo-Qww&hl=ru&sa=X&sqi=2&ved=2ahUKEwijkYbRv7LkAhWDnVwKHfK_CygQ6AEwfHoECGAQAQ')
        self.assertEqual(res['sn'][95]['d'], 'books.google.ru')
        self.assertEqual(res['sn'][95]['vu'], u'https://books.google.ru › books')

        self.assertEqual(res['sn'][98]['t'], 'Hma metatrader - morghparvar')
        self.assertEqual(res['sn'][98]['s'], u'It emphasizes recent prices over older ones, resulting in a fast-acting yet smooth moving average HMA Trend Indicator for MetaTrader 4. . The diagram below shows moving averages HMA and SMA with the same ...')
        self.assertEqual(res['sn'][98]['u'], 'http://morghparvar.ir/hod/hma-metatrader.html')
        self.assertEqual(res['sn'][98]['d'], 'morghparvar.ir')
        self.assertEqual(res['sn'][98]['vu'], u'morghparvar.ir › hod › hma-metatr...')

    def test85(self):
        u""""
            Ошибка парсинга от 2019-09-02
        """
        html = self.get_data('mobile-2019-09-03-1.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'Отдых в Новосибирской области (НСО): санатории, пансионаты, базы отдыха 2019 - Сибирь-Алтай')
        self.assertEqual(res['sn'][0]['s'], u'Новосибирская область с каждым годом привлекает все больше туристов и отдыхающих, ведь здесь есть все необходимые условия для отличного отпуска. В последнее время даже бывалые любители ...')
        self.assertEqual(res['sn'][0]['u'], 'https://www.sibalt.ru/nso')
        self.assertEqual(res['sn'][0]['d'], 'sibalt.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.sibalt.ru › nso')

        self.assertEqual(res['sn'][98]['t'], u'Пичугово - База для семейного и корпоративного отдыха')
        self.assertEqual(res['sn'][98]['s'], u'База отдыха – это территория где можно забыть о внешнем мире и полностью посвятить время своей семье и друзьям. Устройте незабываемые ... Новосибирская область, с.Новопичугово, б/о «Пичугово».')
        self.assertEqual(res['sn'][98]['u'], 'https://xn--b1abozbb3a5a.xn--p1ai/')
        self.assertEqual(res['sn'][98]['d'], 'xn--b1abozbb3a5a.xn--p1ai')
        self.assertEqual(res['sn'][98]['vu'], u'https://пичугово.рф')

    def test86(self):
        u""""
            Ошибка парсинга от 2019-09-02
        """
        html = self.get_data('mobile-2019-09-03-2.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 96)

        self.assertEqual(res['sn'][0]['t'], u'Курорты Калининградской области | Loratravels - Путешествия и туризм')
        self.assertEqual(res['sn'][0]['s'], u'Курорты Калининградской области: Светлогорск, Зеленоградск, Куршская коса, посёлок Янтарный и другие.')
        self.assertEqual(res['sn'][0]['u'], 'https://loratravels.ru/glavnaya/rossiya-i-strany-sng/kurorty-kaliningradskoj-oblasti-kakoj-vybrat')
        self.assertEqual(res['sn'][0]['d'], 'loratravels.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://loratravels.ru › glavnaya › ku...')

        self.assertEqual(res['sn'][95]['t'], u'Белинцева И.В. Архитектура морских курортов Калининградской области. – М.-СПб.: Нестор-История, 2018. – 216 с. - НИИТИАГ')
        self.assertEqual(res['sn'][95]['s'], u'Монография посвящена длительной истории формирования архитектурно-градостроительной среды наиболее известных морских курортов Самбии в Восточной Пруссии (совр. Калининградский полуостров  ...')
        self.assertEqual(res['sn'][95]['u'], 'http://www.niitiag.ru/pub/pub_cat/belintseva_arkhitektura_morskikh_kurortov_kaliningradskoy_oblasti')
        self.assertEqual(res['sn'][95]['d'], 'niitiag.ru')
        self.assertEqual(res['sn'][95]['vu'], u'www.niitiag.ru › pub › pub_cat › b...')

    def test87(self):
        u""""
            Ошибка парсинга от 2019-09-03
        """
        html = self.get_data('mobile-2019-09-03-3.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 98)

        self.assertEqual(res['sn'][0]['t'],u'Отдых в Бахчисарае 2019 и 2020 летом, цены на гостиницы, квартиры и дома - Tvil.ru')
        self.assertEqual(res['sn'][0]['s'], u'Отдых в Бахчисарае 2019 и 2020 летом и зимой, цены, жилье без посредников.')
        self.assertEqual(res['sn'][0]['u'], 'https://tvil.ru/city/bahchisarai/')
        self.assertEqual(res['sn'][0]['d'], 'tvil.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://tvil.ru › city › bahchisarai')

        self.assertEqual(res['sn'][97]['t'], u'Отдых в Бахчисарае 2019: частный сектор у моря, бронирование — Kvartirka.com')
        self.assertEqual(res['sn'][97]['s'], u'Хотите снять жильё для отдыха в частном секторе Бахчисарая? Сервис для поиска жилья «Квартирка» поможет Вам!')
        self.assertEqual(res['sn'][97]['u'], 'https://m.kvartirka.com/russia/bahchisaray/')
        self.assertEqual(res['sn'][97]['d'], 'm.kvartirka.com')
        self.assertEqual(res['sn'][97]['vu'], u'https://m.kvartirka.com › bahchisaray')

    def test88(self):
        u""""
            Ошибка парсинга от 2019-09-03
        """
        html = self.get_data('mobile-2019-09-03-4.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'Путевки в Крым 2019 цены: купить путевку в Крым - пансионат Береговой')
        self.assertEqual(res['sn'][0]['s'], u'Путевки в Крым 2019 - ваш вариант отдыха на полуострове! Стоимость путевок, подробное описание, программы, направления - на сайте, по тел. +7 978 709 14 32, скайп: beregovoy-alushta.')
        self.assertEqual(res['sn'][0]['u'], 'https://beregovoy-alushta.com/actions/pytevki-krym')
        self.assertEqual(res['sn'][0]['d'], 'beregovoy-alushta.com')
        self.assertEqual(res['sn'][0]['vu'], u'https://beregovoy-alushta.com › pyt...')

        self.assertEqual(res['sn'][99]['t'], u'Путевка в санаторий Крыма – купить путевку в санаторий «Киев», Алушта - Санаторий Киев Алушта 2019')
        self.assertEqual(res['sn'][99]['s'], u'Отдых и лечение в Крыму в 2019 году: цены в санатории Алушты, купить путевку в Крым на 2019 год в ... В стоимость путевки в санаторий Алушты «Киев» по лечению заболеваний органов дыхания входят:.')
        self.assertEqual(res['sn'][99]['u'], 'https://kiev-alushta.com/putevki-sanatorij')
        self.assertEqual(res['sn'][99]['d'], 'kiev-alushta.com')
        self.assertEqual(res['sn'][99]['vu'], u'https://kiev-alushta.com › putevki-sa...')

    def test89(self):
        u""""
            Ошибка парсинга от 2019-09-04
        """
        html = self.get_data('mobile-2019-09-04.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 96)

        self.assertEqual(res['sn'][0]['t'], 'Xiaomi')
        self.assertEqual(res['sn'][0]['s'], u'Миссия Xiaomi – сделать инновации доступными каждому. Приобретайте смартфоны, ноутбуки, умные устройства и аксессуары Xiaomi с официальной гарантией.')
        self.assertEqual(res['sn'][0]['u'], 'https://www.mi.com/ru/')
        self.assertEqual(res['sn'][0]['d'], 'mi.com')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.mi.com › ...')

        self.assertEqual(res['sn'][95]['t'], 'Smartphone maker Xiaomi plans $1.5b buyback [Video] - Yahoo Finance')
        self.assertEqual(res['sn'][95]['s'], None)
        self.assertEqual(res['sn'][95]['u'], 'https://finance.yahoo.com/video/smartphone-maker-xiaomi-plans-1-150245874.html')
        self.assertEqual(res['sn'][95]['d'], 'finance.yahoo.com')
        self.assertEqual(res['sn'][95]['vu'], u'https://finance.yahoo.com › video')

    def test91(self):
        u""""
            Ошибка парсинга от 2019-09-04
        """
        html = self.get_data('mobile-2019-09-04-2.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 95)

        self.assertEqual(res['sn'][0]['t'], 'S7 Airlines')
        self.assertEqual(res['sn'][0]['s'], u'Расписания и маршруты. Более 900 направлений по всему миру — все рейсы S7 Airlines и авиакомпаний -партнёров альянса oneworld в нашей маршрутной сети. ... Блог S7 Airlines. Все статьи ...')
        self.assertEqual(res['sn'][0]['u'], 'https://www.s7.ru/mobile/')
        self.assertEqual(res['sn'][0]['d'], 's7.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.s7.ru › mobile')

        self.assertEqual(res['sn'][94]['t'], u'«Ведомости» узнали об отказе России от выпуска «укороченных» суперджетов. Минпромторг это отрицает — Meduza')
        self.assertEqual(res['sn'][94]['s'], u'1 день назад · S7, напоминают «Ведомости», в 2018 году подписала предварительное соглашение о покупке ... а «Аэрофлот» решил не отказываться от планов купить еще 100 таких самолетов.')
        self.assertEqual(res['sn'][94]['u'], 'https://meduza.io/amp/news/2019/09/03/vedomosti-uznali-ob-otkaze-rossii-ot-vypuska-ukorochennyh-superdzhetov-minpromtorg-eto-otritsaet')
        self.assertEqual(res['sn'][94]['d'], 'meduza.io')
        self.assertEqual(res['sn'][94]['vu'], u'https://meduza.io › 2019/09/03')

    def test92(self):
        u""""
            Ошибка парсинга от 2019-09-04
        """
        html = self.get_data('2019-09-18.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 19)
        self.assertEqual(len(res['sn']), 19)

        self.assertEqual(res['sn'][0]['t'], u'Круглый канальный вентилятор: для вытяжки; для притока')
        self.assertEqual(res['sn'][0]['s'], u'Канальные вентиляторы марки TD Вы можете без проблем выбрать и заказать в ... Типы товаров: ... CFk 125 MAX Shuft круглый канальный вентилятор.')
        self.assertEqual(res['sn'][0]['u'], u'https://www.roomklimat.ru/section/5/62-kanalnye-ventilyatory-dlya-kruglykh-kanalov/')
        self.assertEqual(res['sn'][0]['d'], 'roomklimat.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.roomklimat.ru › Каталог › Вентиляция › Вентиляторы')

        self.assertEqual(res['sn'][18]['t'], u'Вентиляционные каналы в Перми от 74 рублей')
        self.assertEqual(res['sn'][18]['s'], u'Где недорого купить вентиляционные каналы в Перми. Самые выгодные предложения, цены, магазины. ... Канальный вентилятор VENTS ТТ 100 · 4.5.')
        self.assertEqual(res['sn'][18]['u'], u'https://perm.bestprice.su/promyshlennost/ventiljacionnye-kanaly/')
        self.assertEqual(res['sn'][18]['d'], 'perm.bestprice.su')
        self.assertEqual(res['sn'][18]['vu'], u'https://perm.bestprice.su › promyshlennost › ventiljacionnye-kanaly')

    def test93(self):
        u""""
            Ошибка парсинга от 2019-09-04
        """
        html = self.get_data('2019-09-18-1.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 408000)
        self.assertEqual(len(res['sn']), 98)

        self.assertEqual(res['sn'][0]['t'], u'Купить кварцевые обогреватели в Москве – доступная ...')
        self.assertEqual(res['sn'][0]['s'], u'В магазине БУРАН Вы можете купить кварцевые обогреватели недорого с удобной доставкой по Москве. Характеристики, отзывы, описание, ...')
        self.assertEqual(res['sn'][0]['u'], u'https://buranrussia.ru/catalog/infrakrasnye-obogrevateli/kvarcevye/')
        self.assertEqual(res['sn'][0]['d'], 'buranrussia.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://buranrussia.ru › catalog › infrakrasnye-obogrevateli › kvarcevye')

        self.assertEqual(res['sn'][1]['t'], u'Обогреватели в Москве - Tepleko.ru')
        self.assertEqual(res['sn'][1]['s'], u'Купить обогреватель МКТЭН в любом городе России можно, связавшись с нами по телефонам в ... Что значит качественный кварцевый обогреватель?')
        self.assertEqual(res['sn'][1]['u'], u'http://tepleko.ru/moscow.html')
        self.assertEqual(res['sn'][1]['d'], 'tepleko.ru')
        self.assertEqual(res['sn'][1]['vu'], u'tepleko.ru › Контакты')

        self.assertEqual(res['sn'][97]['t'], u'Обогреватели кварцевые купить в Иркутске (от 539 руб.) 🥇')
        self.assertEqual(res['sn'][97]['s'], u'1046 товаров в наличии! В категории: Обогреватели кварцевые - купить по выгодной цене, доставка: Иркутск, скидки!')
        self.assertEqual(res['sn'][97]['u'], u'https://irkutsk.regmarkets.ru/obogrevateli-kvartsevye-62036/')
        self.assertEqual(res['sn'][97]['d'], 'irkutsk.regmarkets.ru')
        self.assertEqual(res['sn'][97]['vu'], u'https://irkutsk.regmarkets.ru › obogrevateli-kvartsevye-62036')

    def test94(self):
        u""""
            Ошибка парсинга от 2019-09-19
        """
        html = self.get_data('2019-09-19.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 297000000)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'Планшет на Windows 10 - купить на E-katalog.ru > цены ...')
        self.assertEqual(res['sn'][0]['s'], '')
        self.assertEqual(res['sn'][0]['u'], u'https://www.e-katalog.ru/list/30/pr-19371/')
        self.assertEqual(res['sn'][0]['d'], 'e-katalog.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.e-katalog.ru › list')

        self.assertEqual(res['sn'][99]['t'], u'Планшеты на Windows 10 с клавиатурой')
        self.assertEqual(res['sn'][99]['s'], u'В последнее время популярностью стали пользоваться планшеты на базе ОС Windows 10 с клавиатурой. Это неудивительно, ведь пользователям они ...')
        self.assertEqual(res['sn'][99]['u'], u'https://androidnik.ru/planshet-s-klaviaturoj-windows-10-kupit/')
        self.assertEqual(res['sn'][99]['d'], 'androidnik.ru')
        self.assertEqual(res['sn'][99]['vu'], u'https://androidnik.ru › planshet-s-klaviaturoj-windows-10-kupit')

    def test95(self):
        u""""
            Ошибка парсинга от 2019-10-03
        """
        html = self.get_data('2019-10-03.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 15500000)
        self.assertEqual(len(res['sn']), 98)

        self.assertEqual(res['sn'][0]['t'], u'Гарнитур — Википедия')
        self.assertEqual(res['sn'][0]['s'], u'Гарнитур — комплект каких-либо предметов, выполненный в едином стиле (обычно о мебели или одежде). Гарнитура женская, гарнитур мужской (от ...')
        self.assertEqual(res['sn'][0]['u'], u'https://ru.wikipedia.org/wiki/%D0%93%D0%B0%D1%80%D0%BD%D0%B8%D1%82%D1%83%D1%80')
        self.assertEqual(res['sn'][0]['d'], 'ru.wikipedia.org')
        self.assertEqual(res['sn'][0]['vu'], u'https://ru.wikipedia.org › wiki › Гарнитур')

        self.assertEqual(res['sn'][97]['t'], u'Кухонные гарнитуры: каталог, фото, цены | Скидка + ...')
        self.assertEqual(res['sn'][97]['s'], u'Кухонные гарнитуры - купить кухонный гарнитур в Москве с бесплатной доставкой | Рассрочка без % | Льготная доставка в Северные и отдалённые ...')
        self.assertEqual(res['sn'][97]['u'], u'https://davita-mebel.ru/category/kukhni/kukhonnye-garnitury/')
        self.assertEqual(res['sn'][97]['d'], 'davita-mebel.ru')
        self.assertEqual(res['sn'][97]['vu'], u'https://davita-mebel.ru › category › kukhni › kukhonnye-garnitury')

    def test96(self):
        u""""
            Ошибка парсинга от 2019-10-03
        """
        html = self.get_data('2019-11-25.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 35)
        self.assertEqual(len(res['sn']), 35)

        self.assertEqual(res['sn'][0]['t'], u'DentaLab - стоматологическая клиника нового поколения')
        self.assertEqual(res['sn'][0]['s'], u'... вас способом и сделайте первый шаг к лучшей версии своей улыбки. +7 (812) 903-42-03 priem@dentalab.ru м. Новочеркасская, Большеохтинский пр.')
        self.assertEqual(res['sn'][0]['u'], u'https://dentalab.ru/')
        self.assertEqual(res['sn'][0]['d'], 'dentalab.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://dentalab.ru')

        self.assertEqual(res['sn'][6]['t'], u'“ МедСоюз ”')
        self.assertEqual(res['sn'][6]['s'], u'Новочеркасский пр.д.33 к.3, лит А, пом 21-Н. 16. "Дента Лаб". ст. м. «Новочеркасская». Большеохтинский пр. 10, пом. 1-Н. 17. «Семейная Стоматология».')
        self.assertEqual(res['sn'][6]['u'], u'https://guideh.com/wp-content/uploads/2017/11/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA%20%D0%BA%D0%BB%D0%B8%D0%BD%D0%B8%D0%BA%20%D0%9C%D0%B5%D0%B4%D0%A1%D0%BE%D1%8E%D0%B7.doc')
        self.assertEqual(res['sn'][6]['d'], 'guideh.com')
        self.assertEqual(res['sn'][6]['vu'], u'https://guideh.com › wp-content › uploads › 2017/11')

        self.assertEqual(res['sn'][34]['t'], u'челюстно-лицевая хирургия в Санкт-Петербурге ...')
        self.assertEqual(res['sn'][34]['s'], u'м; медицинская лаборатория · медицинский центр ..... Большеохтинский проспект, 37, 1 этаж; вход с торца. пн.-вс. ... Медицинский центр Дента L.')
        self.assertEqual(res['sn'][34]['u'], u'https://spb.kliniki.ru/med-chelyustno-litsevaya-hirurgiya')
        self.assertEqual(res['sn'][34]['d'], 'spb.kliniki.ru')
        self.assertEqual(res['sn'][34]['vu'], u'https://spb.kliniki.ru › med-chelyustno-litsevaya-hirurgiya')

    def test97(self):
        u""""
            Ошибка парсинга от 2019-12-12
        """
        html = self.get_data('mobile-2019-12-12.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 9)

        self.assertEqual(res['sn'][0]['t'], u'Глянцевые кухни - купить от 5 977 руб в Москве | Интерент-магазин гарнитуров Мебель 169 - Mebel169.ru')
        self.assertEqual(res['sn'][0]['s'], u'Продажа и изготовление глянцевых кухонь от ⭐ 5 977 руб ⭐ за комплект со скидкой до 30%. Онлайн- конструктор готовых кухонь на ... Белый глянец/Салатовый глянец. 17 420 р. Цена за всю кухню · -30%.')
        self.assertEqual(res['sn'][0]['u'], 'https://mebel169.ru/kukhni/glyancevye/')
        self.assertEqual(res['sn'][0]['d'], 'mebel169.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://mebel169.ru › glyancevye')

        self.assertEqual(res['sn'][4]['t'], u'Купить глянцевую кухню недорого в Москве: каталог прямых и угловых кухонь с фото, цветами, ценами - Антарес Мебель')
        self.assertEqual(res['sn'][4]['s'], u'Кухня Валерия-М 2,4 метра. Длина 2392. Ширина 1692. Высота 2140. Глубина 480. 43930руб. 43930 45564Купить. Доставка бесплатно. 1 день. Цвета: Белый глянец (СуМ); Лайм глянец (СуМ); Венге (СуМ) ...')
        self.assertEqual(res['sn'][4]['u'], 'https://www.antarescompany.ru/shop/kuhni/glyancevye/')
        self.assertEqual(res['sn'][4]['d'], 'antarescompany.ru')
        self.assertEqual(res['sn'][4]['vu'], u'https://www.antarescompany.ru › gl...')

        self.assertEqual(res['sn'][5]['t'], u'Купить белую кухню - глянцевые и матовые кухонные гарнитуры белого цвета с фото и ценами - Антарес Мебель')
        self.assertEqual(res['sn'][5]['s'], u'Каталог кухонной мебели с белыми фасадами от российских производителей в интернет-магазине. Мы предлагаем онлайн расчет и бесплатную доставку кухонь белого цвета по Москве.')
        self.assertEqual(res['sn'][5]['u'], 'https://www.antarescompany.ru/shop/kuhni/belye/')
        self.assertEqual(res['sn'][5]['d'], 'antarescompany.ru')
        self.assertEqual(res['sn'][5]['vu'], u'https://www.antarescompany.ru › be...')

        self.assertEqual(res['sn'][8]['t'], u'Глянцевые кухни в стиле модерн купить недорого в Москве - San09')
        self.assertEqual(res['sn'][8]['s'], u'Недорогие кухни Модерн от производителя. Выбор цвета, конфигурации, размеров. ... Кухонный набор « Модерн», цвет «белый глянец», 2 предмета, общая длина 1м. Глубина: 600 мм; Длина: 1000 мм ...')
        self.assertEqual(res['sn'][8]['u'], 'https://san09.ru/mebel_dlya_kuhni/kuhni_komplekty_modern/')
        self.assertEqual(res['sn'][8]['d'], 'san09.ru')
        self.assertEqual(res['sn'][8]['vu'], u'https://san09.ru › mebel_dlya_kuhni')

    def test98(self):
        u""""
            Ошибка парсинга от 2019-12-13
        """
        html = self.get_data('mobile-2019-12-13.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 9)

        self.assertEqual(res['sn'][0]['t'], u'Купить Воздухоувлажнитель Electrolux EHU-3510D в каталоге интернет магазина М.Видео по выгодной цене с доставкой, отзывы, фотографии - Москва')
        self.assertEqual(res['sn'][0]['s'], u'Купить Воздухоувлажнитель Electrolux EHU-3510D по доступной цене в интернет-магазине М.Видео или в розничной сети магазинов М.Видео города Москвы. Electrolux EHU-3510D - аксессуары, отзывы, ...')
        self.assertEqual(res['sn'][0]['u'], 'https://www.mvideo.ru/products/vozduhouvlazhnitel-electrolux-ehu-3510d-20026855')
        self.assertEqual(res['sn'][0]['d'], 'mvideo.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.mvideo.ru › products')

        self.assertEqual(res['sn'][5]['t'], u'Отзывы о Увлажнитель воздуха Electrolux EHU 3510D - Отзовик')
        self.assertEqual(res['sn'][5]['s'], u'Увлажнитель воздуха Electrolux EHU 3510D - отзывы. Рекомендуют 70%. Отзыв о Увлажнитель воздуха Electrolux EHU 3510D. Качество. Надежность. Внешний вид. Удобство. Добавить отзыв Всего отзывов: ...')
        self.assertEqual(res['sn'][5]['u'], 'https://otzovik.com/reviews/uvlazhnitel_vozduha_electrolux_ehu_3510d/')
        self.assertEqual(res['sn'][5]['d'], 'otzovik.com')
        self.assertEqual(res['sn'][5]['vu'], u'https://otzovik.com › reviews › uvla...')

        self.assertEqual(res['sn'][8]['t'], u'Увлажнитель воздуха Electrolux EHU 3510D в Москве, цена по запросу - отзывы инструкции и схемы, официальная гарантия - купить очиститель воздуха Электролюкс ...')
        self.assertEqual(res['sn'][8]['s'], u'Увлажнитель воздуха Electrolux EHU 3510D в Москве с официальной гарантией, цена по запросу - купить очиститель воздуха Электролюкс EHU 3510D в интернет-магазине - Доставка, сравните отзывы и ...')
        self.assertEqual(res['sn'][8]['u'], 'https://elux-ru.ru/electrolux/ochistiteli-i-uvlajniteli-vozduha/Uvlazhnitel_vozduha_Electrolux_EHU_3510D.php')
        self.assertEqual(res['sn'][8]['d'], 'elux-ru.ru')
        self.assertEqual(res['sn'][8]['vu'], u'https://elux-ru.ru › electrolux › Uvla...')

    def test99(self):
        u""""
            Ошибка парсинга от 2019-12-13
        """
        html = self.get_data('mobile-2019-12-13-1.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 9)

        self.assertEqual(res['sn'][0]['t'], u'Делитесь гигабайтами Tele2 - описание и как воспользоваться Москва и Московская область - Теле2')
        self.assertEqual(res['sn'][0]['s'], u'Подробное описание и как воспользоваться услугой Делитесь гигабайтами Tele2. Стоимость подключения Делитесь гигабайтами.')
        self.assertEqual(res['sn'][0]['u'], 'https://msk.tele2.ru/option/share-gb')
        self.assertEqual(res['sn'][0]['d'], 'msk.tele2.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://msk.tele2.ru › share-gb')

        self.assertEqual(res['sn'][1]['t'], u'Как делиться гигабайтами - Теле2')
        self.assertEqual(res['sn'][1]['s'], u'24 окт. 2018 г. · Рассказываем, как поделиться гигабайтами с другими абонентами Теле2. ... С новой услугой «Делитесь гигабайтами» вы можете легко делиться интернет-трафиком с другими абонентами ...')
        self.assertEqual(res['sn'][1]['u'], 'https://msk.tele2.ru/journal/article/gb-share')
        self.assertEqual(res['sn'][1]['d'], 'msk.tele2.ru')
        self.assertEqual(res['sn'][1]['vu'], u'https://msk.tele2.ru › gb-share')

        self.assertEqual(res['sn'][5]['t'], u'«Как поделиться гигабайтами теле2 с тарифом классическим и мой разговор?» – Яндекс.Знатоки')
        self.assertEqual(res['sn'][5]['s'], u'8 ответов')
        self.assertEqual(res['sn'][5]['u'], 'https://yandex.ru/znatoki/question/computers/kak_podelitsia_gigabaitami_tele2_s_adb7db8a/')
        self.assertEqual(res['sn'][5]['d'], 'yandex.ru')
        self.assertEqual(res['sn'][5]['vu'], u'https://yandex.ru › computers › kak...')

        self.assertEqual(res['sn'][8]['t'], u'Как поделиться гигабайтами на Теле2 - Личный кабинет Теле2')
        self.assertEqual(res['sn'][8]['s'], u'25 дек. 2018 г. · Кому доступна услуга “Делись Гигабайтами” от Теле2? Как поделиться трафиком интернета на ... настроить необходимые пакеты – это легко сделать с помощью Личного кабинета Теле2 .')
        self.assertEqual(res['sn'][8]['u'], 'https://www.tele2expert.ru/novaya-usluga-tele2-delites-gigabajtami/')
        self.assertEqual(res['sn'][8]['d'], 'tele2expert.ru')
        self.assertEqual(res['sn'][8]['vu'], u'https://www.tele2expert.ru › novaya...')

    def test100(self):
        u""""
            Ошибка парсинга от 2019-12-16
        """
        html = self.get_data('mobile-2019-12-16.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 98)

        self.assertEqual(res['sn'][0]['t'], u'Бамбуковое постельное белье — Купить комплект белья из БАМБУКА недорого в Москве — Скидка 50% - Spim.ru')
        self.assertEqual(res['sn'][0]['s'], u'Распродажа комплектов из бамбука. Arya - Asabella - US Polo - KingSilk - Issimo. Бесплатная доставка от 3000р. Тысячи пунктов выдачи по всей России.')
        self.assertEqual(res['sn'][0]['u'], 'https://m.spim.ru/shop/postel/bamboo/')
        self.assertEqual(res['sn'][0]['d'], 'm.spim.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://m.spim.ru › postel › bamboo')

        self.assertEqual(res['sn'][2]['t'], u'Постельное белье из бамбука, купить в интернет-магазине недорого - Эко Бамбук')
        self.assertEqual(res['sn'][2]['s'], u'Купив постельное бамбуковое белье в интернет-магазине «Эко бамбук», вы можете быть уверены в его прочности, стойкости окраски и мягкости. Мы предлагаем постельные комплекты из бамбука турецкого ...')
        self.assertEqual(res['sn'][2]['u'], 'https://ekobambuk.ru/products/category/bambukovoe-postelnoe-bele')
        self.assertEqual(res['sn'][2]['d'], 'ekobambuk.ru')
        self.assertEqual(res['sn'][2]['vu'], u'https://ekobambuk.ru › category › b...')

        self.assertEqual(res['sn'][5]['t'], u'Постельное белье из бамбука, цена, доставка в Москве | Togas')
        self.assertEqual(res['sn'][5]['s'], u'Полезные свойства бамбука можно оценить, купив постельное белье из этого прекрасного материала от Togas. Заказав комплект эксклюзивного белья из бамбукового волокна в нашем интернет-магазине, ...')
        self.assertEqual(res['sn'][5]['u'], 'https://www.togas.com/ru/postelnoe-belyo/bambukovoe-volokno/')
        self.assertEqual(res['sn'][5]['d'], 'togas.com')
        self.assertEqual(res['sn'][5]['vu'], u'https://www.togas.com › bambukov...')

        self.assertEqual(res['sn'][97]['t'], u'Элитное бамбуковое постельное белье, сатин бамбук, белое, Kingsilk (Кингсилк), арт. bc-4. Отделка вышивка, листья. Размеры, описание, х… | queenanna.ru | Посте…')
        self.assertEqual(res['sn'][97]['s'], u'Элитное бамбуковое постельное белье, сатин бамбук, белое, Kingsilk (Кингсилк), арт. bc-4. Отделка вышивка, листья. Размеры, описание, характеристики, низкие цены, скидки, доставка.')
        self.assertEqual(res['sn'][97]['u'], 'https://www.pinterest.ru/amp/pin/147352219037218265/')
        self.assertEqual(res['sn'][97]['d'], 'pinterest.ru')
        self.assertEqual(res['sn'][97]['vu'], u'https://www.pinterest.ru › pin')

    def test101(self):
        u""""
            Ошибка парсинга от 2019-12-16
        """
        html = self.get_data('mobile-2019-12-16-1.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 71)

        self.assertEqual(res['sn'][0]['t'], u'Работа в сфере Контент в Москве (мобильная версия) - HH.ru')
        self.assertEqual(res['sn'][0]['s'], u'Огромное количество вакансий в сфере Контент в вашем мобильном устройстве! Поиск работы ... Менеджер по дистанционному обучению. Москва. Всероссийский Банк Развития Регионов (ВБРР). вчера.')
        self.assertEqual(res['sn'][0]['u'], 'https://m.hh.ru/catalog/Informacionnye-tehnologii-Internet-Telekom/Kontent')
        self.assertEqual(res['sn'][0]['d'], 'm.hh.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://m.hh.ru › catalog › Kontent')

        self.assertEqual(res['sn'][2]['t'], u'Контент-менеджер, работа контент-менеджером, вакансии контент-менеджер в Москве - SuperJob')
        self.assertEqual(res['sn'][2]['s'], u'Поиск работы контент-менеджером в Москве. 26 вакансий Контент-менеджера с зарплатой до 75000 рублей.')
        self.assertEqual(res['sn'][2]['u'], 'https://www.superjob.ru/vakansii/kontent-menedzher.html')
        self.assertEqual(res['sn'][2]['d'], 'superjob.ru')
        self.assertEqual(res['sn'][2]['vu'], u'https://www.superjob.ru › vakansii')

        self.assertEqual(res['sn'][5]['t'], u'Работа — Удаленно Контент Менеджер, Москва | Indeed.com')
        self.assertEqual(res['sn'][5]['s'], u'30 открытых вакансий по запросу Удаленно Контент Менеджер, Москва на Indeed.com. Один поиск. Все вакансии.')
        self.assertEqual(res['sn'][5]['u'], 'https://ru.indeed.com/m/jobs?q=%D0%A3%D0%B4%D0%B0%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE+%D0%9A%D0%BE%D0%BD%D1%82%D0%B5%D0%BD%D1%82+%D0%9C%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80&l=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0')
        self.assertEqual(res['sn'][5]['d'], 'ru.indeed.com')
        self.assertEqual(res['sn'][5]['vu'], u'https://ru.indeed.com › jobs › l=Мо...')

        self.assertEqual(res['sn'][70]['t'], u'В Москве прошёл второй, завершающий день «Недели Российского интернета - Экспресс-Новости')
        self.assertEqual(res['sn'][70]['s'], u'3 дня назад · В Москве прошёл второй, завершающий день «Недели Российского интернета» ... внутренних механиках распространения контента, какой контент снимать для привлечения подписчиков,  ...')
        self.assertEqual(res['sn'][70]['u'], 'https://express-novosti.ru/technology/2147508187-v-moskve-proshel-vtoroj-zavershayushchij-den-nedeli-rossijskogo-interneta.html')
        self.assertEqual(res['sn'][70]['d'], 'express-novosti.ru')
        self.assertEqual(res['sn'][70]['vu'], u'https://express-novosti.ru › 2147508...')

    def test102(self):
        u""""
            Ошибка парсинга от 2019-12-16
        """
        html = self.get_data('mobile-2019-12-16-2.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'Топперы круглые купить в магазине ULTRAPARTY.RU')
        self.assertEqual(res['sn'][0]['s'], u'Топперы круглые в магазине праздников ☀ Детские праздники ☀ Аксессуары для вечеринок ☀ Доставка по РФ!')
        self.assertEqual(res['sn'][0]['u'], 'https://ultraparty.ru/category/toppery-kruglye/')
        self.assertEqual(res['sn'][0]['d'], 'ultraparty.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://ultraparty.ru › toppery-kruglye')

        self.assertEqual(res['sn'][2]['t'], u'02__Топперы круглые__Кэнди бар Лунтик. На полянке(© Устроим Праздник).pdf | картинки | Праздник, Кэндо и Картинки - Pinterest')
        self.assertEqual(res['sn'][2]['s'], u'02__Топперы круглые__Кэнди бар Лунтик. На полянке(© Устроим Праздник).pdf. Декоративные ... топперы для кексов "Лунтик" 4 Й День Рождения, Шаблоны Для Печати, Печенье. Подробнее..')
        self.assertEqual(res['sn'][2]['u'], 'https://www.pinterest.com/amp/pin/760263980818064009/')
        self.assertEqual(res['sn'][2]['d'], 'pinterest.com')
        self.assertEqual(res['sn'][2]['vu'], u'https://www.pinterest.com › pin')

        self.assertEqual(res['sn'][5]['t'], u'Топперы круглые "Алиса" 6 шт. купить с доставкой')
        self.assertEqual(res['sn'][5]['s'], u'Главная страница; •; Каталог товаров; •; Готовый декор; •; Топперы для тортов и капкейков; •; Картонные топперы для капкейков; •; Топперы круглые "Алиса" 6 шт.')
        self.assertEqual(res['sn'][5]['u'], 'https://vkustvorchestva.com/catalog/gotovyy_dekor/toppery_dlya_tortov_i_kapkeykov/kartonnye_toppery_dlya_kapkeykov/toppery_kruglye_alisa_6_sht.html')
        self.assertEqual(res['sn'][5]['d'], 'vkustvorchestva.com')
        self.assertEqual(res['sn'][5]['vu'], u'https://vkustvorchestva.com › catalog')

        self.assertEqual(res['sn'][98]['t'], u'Топпер для торта с днем рождения поставки для вечеринок украшения для кексов украшения для дня рождения детский душ с днем рождения топперы... купить товары ...')
        self.assertEqual(res['sn'][98]['s'], u'Купить дешево Топпер для торта с днем рождения поставки для вечеринок ◤украшения◥ для кексов ... 1 пара шнурков Unsiex без галстука запирающиеся круглые шнурки эластичные шнурки Sneaks обувь ...')
        self.assertEqual(res['sn'][98]['u'], 'http://store-aliexpress.ru/ali_good.php?id=32966792113.html')
        self.assertEqual(res['sn'][98]['d'], 'store-aliexpress.ru')
        self.assertEqual(res['sn'][98]['vu'], u'store-aliexpress.ru › ali_good')

    def test103(self):
        u""""
            Ошибка парсинга от 2019-12-16
        """
        html = self.get_data('mobile-2019-12-16-3.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 90)

        self.assertEqual(res['sn'][0]['t'], u'Смартфоны Samsung Galaxy S10, S10+ и S10e цена в кредит, купить телефон Самсунг Галакси С10, С10 плюс и С10е в Москве недорого в интернет-магазине Связной')
        self.assertEqual(res['sn'][0]['s'], u'Смартфоны Samsung Galaxy S10, S10+ и S10e в Москве: выгодные цены, кредит, рассрочка, гарантия! Купить Самсунг Галакси С10, С10 плюс и С10е по тел.: 8 (800) 700-43-43. Быстрая доставка по всей ...')
        self.assertEqual(res['sn'][0]['u'], 'https://www.svyaznoy.ru/catalog/phone/225/samsung/galaxy-s10-s10plus-s10e')
        self.assertEqual(res['sn'][0]['d'], 'svyaznoy.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.svyaznoy.ru › samsung')

        self.assertEqual(res['sn'][2]['t'], u'Купить Samsung Galaxy S10e, S10 и S10+ цена | Samsung RU')
        self.assertEqual(res['sn'][2]['s'], u'Онлайн Trade-In. Сдайте ваше старое устройство по программе Trade-In. Получите выгоду до 58 000Р в корзине до 9 декабря 2019 г. Программа действует в Москве, Московской области, Санкт-Петербурге, ...')
        self.assertEqual(res['sn'][2]['u'], 'https://www.samsung.com/ru/smartphones/galaxy-s10/buy/')
        self.assertEqual(res['sn'][2]['d'], 'samsung.com')
        self.assertEqual(res['sn'][2]['vu'], u'https://www.samsung.com › buy')

        self.assertEqual(res['sn'][89]['t'], u'Samsung Galaxy S10 plus цена в москве')
        self.assertEqual(res['sn'][89]['s'], u'Заказать Samsung Galaxy S10 plus цена в москве Samsung Galaxy S10 мтс.')
        self.assertEqual(res['sn'][89]['u'], 'https://www.myanimalhousevets.com/userfiles/samsung-galaxy-s10-plus-tsena-v-moskve-2043.xml')
        self.assertEqual(res['sn'][89]['d'], 'myanimalhousevets.com')
        self.assertEqual(res['sn'][89]['vu'], u'https://www.myanimalhousevets.com › ...')

    def test104(self):
        u""""
            Ошибка парсинга от 2019-12-19
        """
        html = self.get_data('mobile-2019-12-19.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'Лазерная эпиляция -> EPILAS - Москва')
        self.assertEqual(res['sn'][0]['s'], u'Самые низкие цены на лазерную эпиляцию: Подмышки - 1000 руб., Глубокое бикини - 1500 руб., Ноги полностью - 2500 руб., Руки полностью - 1300 руб. Тел.: 8 (800) 22-000-22.')
        self.assertEqual(res['sn'][0]['u'], 'https://epilas.ru/')
        self.assertEqual(res['sn'][0]['d'], 'epilas.ru')
        self.assertEqual(res['sn'][0]['vu'], 'https://epilas.ru')

        self.assertEqual(res['sn'][1]['t'], u'Лазерная эпиляция для женщин -> EPILAS')
        self.assertEqual(res['sn'][1]['s'], u'Самые низкие цены на женскую лазерную эпиляцию! Подмышки - 1000 руб., Глубокое бикини - 1500 руб., Ноги полностью - 2500 руб., Руки полностью - 1300 руб.')
        self.assertEqual(res['sn'][1]['u'], 'https://epilas.ru/services/epilation/lady')
        self.assertEqual(res['sn'][1]['d'], 'epilas.ru')
        self.assertEqual(res['sn'][1]['vu'], u'https://epilas.ru › Услуги')

        self.assertEqual(res['sn'][2]['t'], u'Приводит ли лазерная эпиляция к раку? - Афиша Daily')
        self.assertEqual(res['sn'][2]['s'], u'17 янв. 2019 г. · Во время лазерной эпиляции свет от прибора поглощается меланином — пигментом волос. Пигмент нагревается и начинает разрушать соседние клетки, отвечающие за рост, или ...')
        self.assertEqual(res['sn'][2]['u'], 'https://daily.afisha.ru/entry/amp/10503/')
        self.assertEqual(res['sn'][2]['d'], 'daily.afisha.ru')
        self.assertEqual(res['sn'][2]['vu'], u'https://daily.afisha.ru › beauty')

        self.assertEqual(res['sn'][98]['t'], u'Лазерная эпиляция в Самаре цены - Дорожная клиническая больница')
        self.assertEqual(res['sn'][98]['s'], u'Лазерная эпиляция лица, зоны бикини и других участков тела. Стоимость лазерной эпиляции в Самаре.')
        self.assertEqual(res['sn'][98]['u'], 'https://dkb63.ru/services/beauty/')
        self.assertEqual(res['sn'][98]['d'], 'dkb63.ru')
        self.assertEqual(res['sn'][98]['vu'], u'https://dkb63.ru › services › beauty')

    def test105(self):
        u""""
            Ошибка парсинга от 2019-12-19
        """
        html = self.get_data('mobile-2019-12-19-1.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 98)

        self.assertEqual(res['sn'][0]['t'], u'EUR USD | Евро Доллар | Курс Евро Доллар - Investing.com')
        self.assertEqual(res['sn'][0]['s'], u'Самые актуальные статистика, аналитика и экономические события, связанные с валютной парой Евро Доллар. Только у нас!')
        self.assertEqual(res['sn'][0]['u'], 'https://m.ru.investing.com/currencies/eur-usd')
        self.assertEqual(res['sn'][0]['d'], 'm.ru.investing.com')
        self.assertEqual(res['sn'][0]['vu'], u'https://m.ru.investing.com › eur-usd')

        self.assertEqual(res['sn'][1]['t'], u'График Евро Доллар | График EUR USD | График Евро Доллар в реальном времени - Investing.com')
        self.assertEqual(res['sn'][1]['s'], u'Посмотрите график Евро Доллар , чтобы быть в курсе последних изменений пары.')
        self.assertEqual(res['sn'][1]['u'], 'https://m.ru.investing.com/currencies/eur-usd-chart')
        self.assertEqual(res['sn'][1]['d'], 'm.ru.investing.com')
        self.assertEqual(res['sn'][1]['vu'], u'https://m.ru.investing.com › eur-usd...')

        self.assertEqual(res['sn'][4]['t'], u'График EUR/USD Forex - ProFinance.Ru')
        self.assertEqual(res['sn'][4]['s'], u'Курс доллара растет, так как данные в США делают маловероятным снижение ставок ФРС. 15:27 ... Курсы валют ЦБ РФ: курс рубля к доллару, евро, гривне, лире, тенге, юаню. 12:42. Квантовые фонды не ...')
        self.assertEqual(res['sn'][4]['u'], 'http://www.profinance.ru/chart/eurusd/')
        self.assertEqual(res['sn'][4]['d'], 'profinance.ru')
        self.assertEqual(res['sn'][4]['vu'], u'www.profinance.ru › chart › eurusd')

        self.assertEqual(res['sn'][97]['t'], u'Доллар с евро подорожали | Экономика и Жизнь')
        self.assertEqual(res['sn'][97]['s'], u'24 часа назад · 18.12.2019 - Центральный банк Российской Федерации на 19 декабря увеличил официальный курс доллара на 5,05 коп., евро – на 1,24 коп.')
        self.assertEqual(res['sn'][97]['u'], 'https://www.eg-online.ru/news/413021/')
        self.assertEqual(res['sn'][97]['d'], 'eg-online.ru')
        self.assertEqual(res['sn'][97]['vu'], u'https://www.eg-online.ru › news')

    def test106(self):
        u""""
            Ошибка парсинга от 2019-12-20
        """
        html = self.get_data('mobile-2019-12-20.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 98)

        self.assertEqual(res['sn'][0]['t'], u'Пластиковые окна: цены в Москве, стоимость по типу дома, цена за м2 - от 3 714 руб. - ОКНА СТРИТ г. Москва')
        self.assertEqual(res['sn'][0]['s'], u'Предлагаем пластиковые окна, цены от производителя! Самая низкая стоимость на окна ПВХ в Москве и в Московской области!')
        self.assertEqual(res['sn'][0]['u'], 'https://www.oknastreet.ru/stoimost-new/plastikovye-okna-ceny.html')
        self.assertEqual(res['sn'][0]['d'], 'oknastreet.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.oknastreet.ru › plastiko...')

        self.assertEqual(res['sn'][1]['t'], u'Пластиковые окна: цены с установкой в Москве, стоимость окон ПВХ - Фабрика Окон')
        self.assertEqual(res['sn'][1]['s'], u'Цены на пластиковые окна от производителя. Стоимость окон ПВХ с установкой в Москве и МО. ✔️Под ключ от 4760 руб. ✔️БЕСПРОЦЕНТНАЯ рассрочка ✔️Гарантия до 30лет ☎️+7(499)112-19-93.')
        self.assertEqual(res['sn'][1]['u'], 'https://www.fabrikaokon.ru/price-b.html')
        self.assertEqual(res['sn'][1]['d'], 'fabrikaokon.ru')
        self.assertEqual(res['sn'][1]['vu'], u'https://www.fabrikaokon.ru › price-b')

        self.assertEqual(res['sn'][4]['t'], u'Цены на пластиковые окна: сколько стоят окна ПВХ в Москве и от чего зависит стоимость? - Комсомольская правда')
        self.assertEqual(res['sn'][4]['s'], u'Около 30 000 руб. можно отдать за пластиковые окна и их установку в однокомнатной квартире с балконом. Это не самая высокая цена за уют в доме, ведь ПВХ окна не нуждаются в покраске и ...')
        self.assertEqual(res['sn'][4]['u'], 'https://www.kp.ru/guide/tseny-na-plastikovye-okna.html')
        self.assertEqual(res['sn'][4]['d'], 'kp.ru')
        self.assertEqual(res['sn'][4]['vu'], u'https://www.kp.ru › guide › tseny-n...')

        self.assertEqual(res['sn'][97]['t'], u'виды, размеры и цены. Оконный калькулятор. - Пластиковые окна')
        self.assertEqual(res['sn'][97]['s'], u'Узнайте стоимость окон удобным способом: 1) посмотреть стандартные размеры окон и цены на них 2) online расчет цен оконным калькулятором 3) посмотреть стоимость окон пластиковых по сериям ...')
        self.assertEqual(res['sn'][97]['u'], 'https://m.okna-trust.ru/ceny')
        self.assertEqual(res['sn'][97]['d'], 'm.okna-trust.ru')
        self.assertEqual(res['sn'][97]['vu'], u'https://m.okna-trust.ru › ceny')

    def test107(self):
        u""""
            Ошибка парсинга от 2019-12-21
        """
        html = self.get_data('mobile-2019-12-21.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 98)

        self.assertEqual(res['sn'][0]['t'], u'Угловые кожаные диваны | Купить мягкую мебель в Москве в интернет-магазине Heggi - Хегги')
        self.assertEqual(res['sn'][0]['s'], u'В интернет-магазине Heggi вы можете купить угловые кожаные диваны с доставкой по Москве. Выгодные цены благодаря собственному производству и отсутствию посредников, огромный ассортимент ...')
        self.assertEqual(res['sn'][0]['u'], 'https://www.divano.ru/catalog/kozhanaya-mebel/divany-uglovye-kozha/')
        self.assertEqual(res['sn'][0]['d'], 'divano.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.divano.ru › catalog › di...')

        self.assertEqual(res['sn'][1]['t'], u'Угловые диваны из натуральной кожи - купить недорогой кожаный диван в Москве по цене распродажи от производителя - HomeMe')
        self.assertEqual(res['sn'][1]['s'], u'Купить недорогие Угловые кожаные диваны в Москве, дешевые цены от 52990 руб на Угловые кожаные диваны, сезонные распродажи и акции. Мы производитель, поэтому в каталоге сотни моделей и ...')
        self.assertEqual(res['sn'][1]['u'], 'https://www.homeme.ru/cat/uglovye-divany/kozhanye/')
        self.assertEqual(res['sn'][1]['d'], 'homeme.ru')
        self.assertEqual(res['sn'][1]['vu'], u'https://www.homeme.ru › kozhanye')

        self.assertEqual(res['sn'][4]['t'], u'Угловые кожаные диваны - купить в Москве недорого, низкие цены на угловой кожаный диван от производителя в интернет-магазине MnogoMeb.Ru')
        self.assertEqual(res['sn'][4]['s'], u'Каталог угловых кожаных диванов в интернет-магазине мебели MnogoMeb.ru: большой выбор самых разных моделей, огромное разнообразие тканей и расцветок и все это по доступной стоимости. Купить  ...')
        self.assertEqual(res['sn'][4]['u'], 'https://mnogomeb.ru/divany/uglovye/kojanye/')
        self.assertEqual(res['sn'][4]['d'], 'mnogomeb.ru')
        self.assertEqual(res['sn'][4]['vu'], u'https://mnogomeb.ru › kojanye')

        self.assertEqual(res['sn'][97]['t'], u'BoConcept: Современная мебель – Актуальный дизайн')
        self.assertEqual(res['sn'][97]['s'], u'Наши мебельные магазины предлагают любую мебель современного дизайна, начиная от дизайнерских ... Анилиновая кожа, фетр, бархат, дуб, орех, хром и сталь – мы сочетаем материалы и ...')
        self.assertEqual(res['sn'][97]['u'], 'https://www.boconcept.com/ru-ru/')
        self.assertEqual(res['sn'][97]['d'], 'boconcept.com')
        self.assertEqual(res['sn'][97]['vu'], u'https://www.boconcept.com › ru-ru')

    def test108(self):
        u""""
            Ошибка парсинга от 2020-11-26
        """
        html = self.get_data('2020-11-26.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 168000)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'Велоодежда для мужчин купить в Москве - цена в интернет ...')
        self.assertEqual(res['sn'][0]['s'], u'Предлагаем качественную велоодежду от знаменитых итальянских брендов: ALE, Biemme, Castelli, Giordana, Marcello Bergamo, MOA Sport, Nalini, Santini, ...')
        self.assertEqual(res['sn'][0]['u'], u'http://velo-forma.ru/veloodezhda-muzhskaya')
        self.assertEqual(res['sn'][0]['d'], 'velo-forma.ru')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][6]['t'], u'Велоодежда купить в Москве - Цены на велосипедную ...')
        self.assertEqual(res['sn'][6]['s'], u'Купить одежду для велоспорта в интернет-магазине Provelo. Описание ... Велоодежда. Веломайки (124) ... Мужской гидрокостюм Sailfish Vibrant Men ...')
        self.assertEqual(res['sn'][6]['u'], u'https://www.provelo.ru/models-odezhda/')
        self.assertEqual(res['sn'][6]['d'], 'provelo.ru')
        self.assertEqual(res['sn'][6]['vu'], None)

        self.assertEqual(res['sn'][34]['t'], u'Мужскую велоодежду купить в Санкт-Петербурге, цены ...')
        self.assertEqual(res['sn'][34]['s'], u'Купить мужскую велоодежду в интернет-магазине ВелоДрайв. Каталог велоодежды для мужчин. Доставка! Гарантия на всю продукцию. Каталог ...')
        self.assertEqual(res['sn'][34]['u'], u'https://www.velodrive.ru/accessories/type/veloodezhda_muzhskaya/')
        self.assertEqual(res['sn'][34]['d'], 'velodrive.ru')
        self.assertEqual(res['sn'][34]['vu'], None)

    def test109(self):
        u""""
            Ошибка парсинга от 2020-11-26
        """
        html = self.get_data('2020-11-26-1.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 0)

    def test110(self):
        u""""
            Ошибка парсинга от 2020-11-26
        """
        html = self.get_data('2020-11-27.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 134000000)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'CST - точное время')
        self.assertEqual(res['sn'][0]['s'], u'Точное время, часовой пояс, смещение от UTC/GMT и основные факты для Северноамериканское Центральное Стандартное Время (CST).')
        self.assertEqual(res['sn'][0]['u'], u'https://24timezones.com/chasovoy-poyas/cst')
        self.assertEqual(res['sn'][0]['d'], '24timezones.com')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][6]['t'], u'CST STUDIO SUITE 2020 - моделирование трехмерных ...')
        self.assertEqual(res['sn'][6]['s'], u'Ранее вычислительные модули были сгруппированы в программы, которые имели оригинальные названия: CST MICROWAVE STUDIO (CST MWS), CST ...')
        self.assertEqual(res['sn'][6]['u'], u'http://eurointech.ru/eda/microwave_design/cst/CST-STUDIO-SUITE.phtml')
        self.assertEqual(res['sn'][6]['d'], 'eurointech.ru')
        self.assertEqual(res['sn'][6]['vu'], None)

        self.assertEqual(res['sn'][34]['t'], u'CST - СпортЭк')
        self.assertEqual(res['sn'][34]['s'], u'Обратный звонок. 8 (922) 207-63-37 · 8 (343) 254-58-93 · Избранное. Ваша корзина пуста. Корзина. Каталог товаров. Велотовары · Велосипеды.')
        self.assertEqual(res['sn'][34]['u'], u'https://www.sportek.su/brands/cst.html')
        self.assertEqual(res['sn'][34]['d'], 'sportek.su')
        self.assertEqual(res['sn'][34]['vu'], None)

    def test111(self):
        u""""
            Ошибка парсинга от 2020-12-07
        """
        html = self.get_data('2020-12-07.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 11700)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'testo 815 - Шумомер - Тэсто Рус')
        self.assertEqual(res['sn'][0]['s'], u'testo 815 - Шумомер. Номер заказа. 0563 8155. testo 815 Product. testo 815. Класс точности 2 в соответствие с IEC 60651. Легкая настройка (отвертка ...')
        self.assertEqual(res['sn'][0]['u'], u'https://www.testo.ru/ru-RU/testo-815/p/0563-8155')
        self.assertEqual(res['sn'][0]['d'], 'testo.ru')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][6]['t'], u'Руководство пользователя рус Шумомер testo 815')
        self.assertEqual(res['sn'][6]['s'], u'testo 815 - это шумомер с поддержкой диапазонов 32-80 дБ, 50-100 дБ и. 80-130 дБ, двух типов временной коррекции, двух типов частотной коррек-.')
        self.assertEqual(res['sn'][6]['u'], u'https://plutongeo.ru/assets/files/manual/testo-815-ru.pdf')
        self.assertEqual(res['sn'][6]['d'], 'plutongeo.ru')
        self.assertEqual(res['sn'][6]['vu'], None)

        self.assertEqual(res['sn'][99]['t'], u'Заказать шумомер testo 815 - Шумомеры TESTO')
        self.assertEqual(res['sn'][99]['s'], u'Главная » Заказать шумомер testo 815. Заказать ... Шумомер, Принадлежности. 3 класс: testo 815, Калибратор для регулярной калибровки шумомера ...')
        self.assertEqual(res['sn'][99]['u'], u'http://soundlevel.ru/order-4.html')
        self.assertEqual(res['sn'][99]['d'], 'soundlevel.ru')
        self.assertEqual(res['sn'][99]['vu'], None)

    def test112(self):
        u""""
            Ошибка парсинга от 2021-01-29
        """
        html = self.get_data('2021-01-29.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 1670000)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'Угловые навесные настенные полки от 700 руб. — купить ...')
        self.assertEqual(res['sn'][0]['s'], u'В каталоге нашего интернет-магазина вы сможете подобрать, заказать и недорого купить угловую навесную настенную полку в Москве различных ...')
        self.assertEqual(res['sn'][0]['u'], u'https://pm.ru/category/mebel-dlya-doma/nastennie_polki/uglovye/')
        self.assertEqual(res['sn'][0]['d'], 'pm.ru')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][6]['t'], u'Настенные полки в прихожую - купить в Москве недорого ...')
        self.assertEqual(res['sn'][6]['s'], u'Полки для прихожей по низким ценам - от 520 рублей, купить недорого в интернет-магазине ... Полка угловая одинарная с эффектом старения.')
        self.assertEqual(res['sn'][6]['u'], u'https://bestmebelik.ru/polki-dlya-prihozhey.html')
        self.assertEqual(res['sn'][6]['d'], 'bestmebelik.ru')
        self.assertEqual(res['sn'][6]['vu'], None)

        self.assertEqual(res['sn'][98]['t'], u'Прихожая Машенька: полка угловая ПУ-201. Купить мебель ...')
        self.assertEqual(res['sn'][98]['s'], u'Прихожая Машенька: полка угловая ПУ-201. Купить мебель для прихожих в Екатеринбурге. Информация, цена и условия поставки. Тел. +7 950 191 1415 ...')
        self.assertEqual(res['sn'][98]['u'], u'https://nikaekb.com/p339458867-prihozhaya-mashenka-polka.html')
        self.assertEqual(res['sn'][98]['d'], 'nikaekb.com')
        self.assertEqual(res['sn'][98]['vu'], None)

    def test113(self):
        u""""
            Ошибка парсинга от 2021-01-29
        """
        html = self.get_data('2021-04-07.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 25000000)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'Аренда и заказ автобуса в Москве')
        self.assertEqual(res['sn'][0]['s'], u'Аренда автобусов в Москве. Свой автопарк из 26 автобусов и 28 микроавтобусов. Опытные водители. Транспорт 2020-2021 года выпуска от 8 до 74 ...')
        self.assertEqual(res['sn'][0]['u'], u'https://www.vash-perevozchik.ru/')
        self.assertEqual(res['sn'][0]['d'], 'vash-perevozchik.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.vash-perevozchik.ru')

        self.assertEqual(res['sn'][6]['t'], u'Заказ автобуса в Москве с водителем')
        self.assertEqual(res['sn'][6]['s'], u'Заказ автобуса в компании BusStar (Бас Стар): услуги проката автобусов и микроавтобусов в Москве с водителем. Мы имеем широкий парк ...')
        self.assertEqual(res['sn'][6]['u'], u'https://www.busstar.ru/')
        self.assertEqual(res['sn'][6]['d'], 'busstar.ru')
        self.assertEqual(res['sn'][6]['vu'], u'https://www.busstar.ru')

        self.assertEqual(res['sn'][99]['t'], u'Аренда автобуса | ТулаТранс')
        self.assertEqual(res['sn'][99]['s'], u'Аренда автобуса для различных мероприятий. Большой ... Оформление заказов онлайн. ... У нас вы можете заказать автобусдля любых случаев.')
        self.assertEqual(res['sn'][99]['u'], u'http://tulatransport.ru/')
        self.assertEqual(res['sn'][99]['d'], 'tulatransport.ru')
        self.assertEqual(res['sn'][99]['vu'], u'http://tulatransport.ru')

    def test115(self):
        u""""
            Ошибка парсинга
        """
        html = self.get_data('2021-05-31.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 337000000)
        self.assertEqual(len(res['sn']), 96)

        self.assertEqual(res['sn'][0]['t'], u'Coral Travel - туроператор по Турции, России, Греции ...')
        self.assertEqual(res['sn'][0]['s'], u'Coral Travel - ведущий туроператор по Турции, России, Греции, Испании, Тунису! Поиск туров и бронирование туров онлайн прямо на сайте. Полная ...')
        self.assertEqual(res['sn'][0]['u'], u'https://www.coral.ru/')
        self.assertEqual(res['sn'][0]['d'], 'coral.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.coral.ru')

        self.assertEqual(res['sn'][6]['t'], u'CORAL TRAVEL (@coraltravel) • Instagram photos and videos')
        self.assertEqual(res['sn'][6]['s'], u'422k Followers, 9 Following, 5177 Posts - See Instagram photos and videos from CORAL TRAVEL (@coraltravel)')
        self.assertEqual(res['sn'][6]['u'], u'https://www.instagram.com/coraltravel/?hl=ru')
        self.assertEqual(res['sn'][6]['d'], 'instagram.com')
        self.assertEqual(res['sn'][6]['vu'], None)

        self.assertEqual(res['sn'][95]['t'], u'"CoralTravel" - официальный сайт в Ростове-на-Дону')
        self.assertEqual(res['sn'][95]['s'], u'Официальный сайт турагентства "CoralTravel" в Ростове-на-Дону. Поиск горящих туров на сайте Anex во все страны мира. Онлайн бронирование!')
        self.assertEqual(res['sn'][95]['u'], u'https://poisk-travel.com/')
        self.assertEqual(res['sn'][95]['d'], 'poisk-travel.com')
        self.assertEqual(res['sn'][95]['vu'], u'https://poisk-travel.com')

    def test114(self):
        u""""
            Ошибка парсинга от 2021-01-29
        """
        html = self.get_data('2021-04-08.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)

    def test116(self):
        u""""
            Ошибка парсинга от 2021-06-02
        """
        html = self.get_data('2021-06-02.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 19500000)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'Базы отдыха в Смоленской области - турбазы, цены 2021 ...')
        self.assertEqual(res['sn'][0]['s'], u'Базы отдыха и турбазы в Смоленской области: фото территории, домиков, подробным описанием услуг, отзывами, координатами на карте, ценами, ...')
        self.assertEqual(res['sn'][0]['u'], u'https://101hotels.com/russia/region/smolenskaya_oblast/recreation_base')
        self.assertEqual(res['sn'][0]['d'], '101hotels.com')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][6]['t'], u'Турбазы и базы отдыха Смоленской области')
        self.assertEqual(res['sn'][6]['s'], u'База отдыха в деревне Бодровка Рославльского района Смоленской области. На территории базы есть своя ферма с животными, милой собакой- ...')
        self.assertEqual(res['sn'][6]['u'], u'https://katalogturbaz.ru/russia/smolenskaja-oblast')
        self.assertEqual(res['sn'][6]['d'], 'katalogturbaz.ru')
        self.assertEqual(res['sn'][6]['vu'], None)

        self.assertEqual(res['sn'][99]['t'], u'На каких пляжах в Смоленской области можно безопасно ...')
        self.assertEqual(res['sn'][99]['s'], u'13 ч. назад — Контроль за выполнением требований по охране жизни и безопасности людей на пляжах и других местах массового отдыха на водоемах ...')
        self.assertEqual(res['sn'][99]['u'], u'https://smolnarod.ru/sn/society/na-kakix-plyazhax-v-smolenskoj-oblasti-mozhno-bezopasno-otdyxat/')
        self.assertEqual(res['sn'][99]['d'], 'smolnarod.ru')
        self.assertEqual(res['sn'][99]['vu'], None)

    def test117(self):
        u""""
            Ошибка парсинга от 2021-06-02
        """
        html = self.get_data('2021-06-02-1.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 99)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'Что такое десима? Что такое десима - Ответы Mail.ru')
        self.assertEqual(res['sn'][0]['s'], u'Десима - это 10 побед в кубке/лиге чемпионов. У команды Реал Мадрид десима. Нравится.')
        self.assertEqual(res['sn'][0]['u'], u'https://otvet.mail.ru/question/180584498')
        self.assertEqual(res['sn'][0]['d'], 'otvet.mail.ru')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][6]['t'], u'Desima.com')
        self.assertEqual(res['sn'][6]['s'], u'Welcome to Desima,the German manufacturer of high-quality textile wallpapers established in 1984.We are very glad in your interest and in your good tastes!')
        self.assertEqual(res['sn'][6]['u'], u'https://www.desima.com/')
        self.assertEqual(res['sn'][6]['d'], 'desima.com')
        self.assertEqual(res['sn'][6]['vu'], u'https://www.desima.com')

        self.assertEqual(res['sn'][98]['t'], u'Soal-soal latihan pemrograman dasar - pemrograman web')
        self.assertEqual(res['sn'][98]['s'], u'20 окт. 2016 г. — Diketahui bahwa kantong P kosong. Kantong Q berisi 10 buah kelereng dan kantong R berisi 15 kelereng. Apabila yang terbawa hanya ...')
        self.assertEqual(res['sn'][98]['u'], u'http://astrikotaxtkj2menia.blogspot.com/2016/10/soal-dan-jawaban.html')
        self.assertEqual(res['sn'][98]['d'], 'astrikotaxtkj2menia.blogspot.com')
        self.assertEqual(res['sn'][98]['vu'], None)

    def test118(self):
        u""""
            Ошибка парсинга от 2021-06-02
        """
        html = self.get_data('2021-06-02-3.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 1890000)
        self.assertEqual(len(res['sn']), 98)

        self.assertEqual(res['sn'][0]['t'], u'Стадион Шахтёр | Центр спорта в Кемерово')
        self.assertEqual(res['sn'][0]['s'], u'г. Кемрово, ул. Рутгерса, 32; (384-2) 64-32-60, (384-2) 64-06-63; Напишите нам. Версия для слабовидящих. Стадион Шахтёр. Центр спорта в Кемерово.')
        self.assertEqual(res['sn'][0]['u'], u'http://stadium-shahter.ru/')
        self.assertEqual(res['sn'][0]['d'], 'stadium-shahter.ru')
        self.assertEqual(res['sn'][0]['vu'], u'http://stadium-shahter.ru')

        self.assertEqual(res['sn'][6]['t'], u'Информация о стадионе «Шахтёр», Кемерово - Реестр ...')
        self.assertEqual(res['sn'][6]['s'], u'Стадион Шахтёр. город: Кемерово, Россия адрес: 650040, Кемерово, ул. Рутгерса, 32 телефон: (3842) 64–06–63 год постройки: 1935 вместимость: 4 ...')
        self.assertEqual(res['sn'][6]['u'], u'http://www.rusbandy.ru/stadium/52/')
        self.assertEqual(res['sn'][6]['d'], 'rusbandy.ru')
        self.assertEqual(res['sn'][6]['vu'], None)

        self.assertEqual(res['sn'][97]['t'], u'Посмотрите, как выглядит стадион «Шахтёр» в ... - Kurjer.info')
        self.assertEqual(res['sn'][97]['s'], u'27 нояб. 2019 г. — В Солигорске продолжается реконструкция стадиона «Шахтёр». Планировалось, что уже осенью этого года спортивная арена ...')
        self.assertEqual(res['sn'][97]['u'], u'https://kurjer.info/2019/11/27/stadium-shakhter/')
        self.assertEqual(res['sn'][97]['d'], 'kurjer.info')
        self.assertEqual(res['sn'][97]['vu'], None)

    def test119(self):
        u""""
            Ошибка парсинга от 2021-06-03
        """
        html = self.get_data('2021-06-03.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 37500000)
        self.assertEqual(len(res['sn']), 99)

        self.assertEqual(res['sn'][0]['t'], u'Kia Rio седан 2021 - Цены и комплектации')
        self.assertEqual(res['sn'][0]['s'], u'Двигатели и трансмиссии, спроектированные с учетом российских условий, дадут Вам динамику, которую Вы ожидаете, и привнесут яркие эмоции в ...')
        self.assertEqual(res['sn'][0]['u'], u'https://www.kia.ru/models/rio/options/')
        self.assertEqual(res['sn'][0]['d'], 'kia.ru')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][6]['t'], u'KIA Rio 2021, купить новый КИА Рио в Москве ...')
        self.assertEqual(res['sn'][6]['s'], u'Автомобили KIA Rio седан от официального дилера АвтоГЕРМЕС, большое количество в наличии. Специальные цены, выгодные предложения на KIA ...')
        self.assertEqual(res['sn'][6]['u'], u'https://www.avtogermes.ru/sale/kia/rio/')
        self.assertEqual(res['sn'][6]['d'], 'avtogermes.ru')
        self.assertEqual(res['sn'][6]['vu'], None)

        self.assertEqual(res['sn'][98]['t'], u'Kia Rio 2021 Prices in UAE, Specs & Reviews for Dubai, Abu ...')
        self.assertEqual(res['sn'][98]['s'], u'Kia Rio 2021 prices in UAE starting at AED 49900, specs and reviews for Dubai, Abu Dhabi, ... Price When New In UAE ... 2018 Kia Rio Hatchback first drive ...')
        self.assertEqual(res['sn'][98]['u'], u'https://www.drivearabia.com/carprices/uae/kia/kia-rio/2021/')
        self.assertEqual(res['sn'][98]['d'], 'drivearabia.com')
        self.assertEqual(res['sn'][98]['vu'], None)

    def test120(self):
        u""""
            Некорректный html
        """
        html = 'asdfasdfa'
        with self.assertRaises(GoogleParserError) as e:
            g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
            g.get_serp()

    def test121(self):
        u""""
            Некорректный html
        """
        html = ''
        with self.assertRaises(GoogleParserError) as e:
            g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
            g.get_serp()

    def test122(self):
        u""""
            Ошибка парсинга от 2021-06-07
        """
        html = self.get_data('2021-06-07.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 4400000)
        self.assertEqual(len(res['sn']), 100)

        self.assertEqual(res['sn'][0]['t'], u'Погода в Греции в январе 2021 года, температура воздуха ...')
        self.assertEqual(res['sn'][0]['s'], u'Прогноз погоды в Греции в январе по российским меркам теплый, в среднем воздух прогревается до +8-10 градусов. В горах погода, конечно, намного ...')
        self.assertEqual(res['sn'][0]['u'], u'https://tonkosti.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%93%D1%80%D0%B5%D1%86%D0%B8%D0%B8_%D0%B2_%D1%8F%D0%BD%D0%B2%D0%B0%D1%80%D0%B5')
        self.assertEqual(res['sn'][0]['d'], 'tonkosti.ru')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][6]['t'], u'Отдых в Греции в январе - отзывы туристов на отели ...')
        self.assertEqual(res['sn'][6]['s'], u'52272 отзыва туристов об отдыхе в Греции в январе, отзывы ... Отдыхали в этом отеле в августе 2020 года, отель отличный, еда не плохая, номера ...')
        self.assertEqual(res['sn'][6]['u'], u'https://saletur.ru/%D0%93%D1%80%D0%B5%D1%86%D0%B8%D1%8F/otzyv/%D1%8F%D0%BD%D0%B2%D0%B0%D1%80%D1%8C/')
        self.assertEqual(res['sn'][6]['d'], 'saletur.ru')
        self.assertEqual(res['sn'][6]['vu'], None)

        self.assertEqual(res['sn'][99]['t'], u'Представитель МИД России рассказал об отдыхе за ...')
        self.assertEqual(res['sn'][99]['s'], u'5 дней назад — ... момент курортов можно включить Болгарию, Грецию, Хорватию и ... срок действия которой истек в период с 1 января 2020 года, могут ...')
        self.assertEqual(res['sn'][99]['u'], u'https://pravda-nn.ru/interview/sergej-malov-prezhde-chem-kupit-putevku-i-otpravitsya-v-puteshestvie-neobhodimo-vzvesit-vse-za-i-protiv-i-tolko-zatem-prinimat-reshenie/')
        self.assertEqual(res['sn'][99]['d'], 'pravda-nn.ru')
        self.assertEqual(res['sn'][99]['vu'], None)

    def test126(self):
        u""""
            Ошибка парсинга от 2021-10-26
        """
        html = self.get_data('2021-10-26.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 94)
        self.assertEqual(len(res['sn']), 96)

        self.assertEqual(res['sn'][0]['t'], u'Tele2 TV — как бесплатно пользоваться - GSMWIKI ...')
        self.assertEqual(res['sn'][0]['s'], u'Способы отключить подписку на Теле2 ТВ · в приложении в левом вертикальном меню кликнуть на номер телефона, выбрать раздел с нужной подпиской, нажать «Отключить» ...')
        self.assertEqual(res['sn'][0]['u'], u'https://gsmwiki.ru/tele2/tv-tele2/')
        self.assertEqual(res['sn'][0]['d'], 'gsmwiki.ru')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][6]['t'], u'Как отключить «Теле2 ТВ», установить, список каналов и ...')
        self.assertEqual(res['sn'][6]['s'], u'Как отключить Tele2 TV; Стоимость и условия пользования Теле2 ТВ ... Ведь из него можно выбрать программы, кино на любой вкус – от комедий и детских фильмов ...')
        self.assertEqual(res['sn'][6]['u'], u'https://ontele2.ru/uslugi/tele2-tv')
        self.assertEqual(res['sn'][6]['d'], 'ontele2.ru')
        self.assertEqual(res['sn'][6]['vu'], None)

        self.assertEqual(res['sn'][95]['t'], u'Отписка от платных услуг теле2. Платные подписки на Теле2')
        self.assertEqual(res['sn'][95]['s'], u'С помощью меню можно переключать режимы, входить в «Кинозал» (фильмы, сериалы, ... В Личном кабинете на сайте Теле2 подключение и отключение доступно в ...')
        self.assertEqual(res['sn'][95]['u'], u'https://mobilca.ru/an-extract-from-paid-tele2-services-paid-subscriptions-for-tele2.html')
        self.assertEqual(res['sn'][95]['d'], 'mobilca.ru')
        self.assertEqual(res['sn'][95]['vu'], None)

    def test128(self):
        u""""
            Ошибка парсинга от 2021-10-28
        """
        html = self.get_data('2021-10-28.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 25800000)
        self.assertEqual(len(res['sn']), 98)

        self.assertEqual(res['sn'][0]['t'], u'COVID-19 Map - Johns Hopkins Coronavirus Resource Center')
        self.assertEqual(res['sn'][0]['s'], u'Coronavirus COVID-19 Global Cases by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University (JHU)')
        self.assertEqual(res['sn'][0]['u'], u'https://coronavirus.jhu.edu/map.html')
        self.assertEqual(res['sn'][0]['d'], 'coronavirus.jhu.edu')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][6]['t'], u'The Johns Hopkins University School of Medicine')
        self.assertEqual(res['sn'][6]['s'], u'“Having people who looked like me as my doctors and as my mentors was a huge influence,” says Ubah Jimale Dimbil, a second year emergency medicine resident ...')
        self.assertEqual(res['sn'][6]['u'], u'https://www.hopkinsmedicine.org/som/')
        self.assertEqual(res['sn'][6]['d'], 'hopkinsmedicine.org')
        self.assertEqual(res['sn'][6]['vu'], None)

        self.assertEqual(res['sn'][97]['t'], u'Центр доктора Бубновского - официальный сайт')
        self.assertEqual(res['sn'][97]['s'], u'Центр доктора Бубновского предоставляет услуги по реабилитации опорно-двигательного аппарата в соответствии с высокими международными стандартами.')
        self.assertEqual(res['sn'][97]['u'], u'https://bubnovsky.org/')
        self.assertEqual(res['sn'][97]['d'], 'bubnovsky.org')
        self.assertEqual(res['sn'][97]['vu'], 'https://bubnovsky.org')

    def test129(self):
        u""""
            Ошибка парсинга от 2021-10-28
        """
        html = self.get_data('2021-10-28-1.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 1920000000)
        self.assertEqual(len(res['sn']), 97)

        self.assertEqual(res['sn'][0]['t'], u'SA.RU')
        self.assertEqual(res['sn'][0]['s'], u'Интернет-магазин SA.RU предлагает приобрести автомобильные шины и колесные диски с гарантией качества. В торгово-сервисных центрах SA.RU (г.')
        self.assertEqual(res['sn'][0]['u'], u'https://sa.ru/')
        self.assertEqual(res['sn'][0]['d'], u'sa.ru')
        self.assertEqual(res['sn'][0]['vu'], 'https://sa.ru')

        self.assertEqual(res['sn'][77]['t'], u'Instagram Ro-sa.ru - Япония Транзит')
        self.assertEqual(res['sn'][77]['s'], '')
        self.assertEqual(res['sn'][77]['u'], u'https://japantransit.ru/yapodbor/instwidget/index1.php')
        self.assertEqual(res['sn'][77]['d'], 'japantransit.ru')
        self.assertEqual(res['sn'][77]['vu'], None)

        self.assertEqual(res['sn'][96]['t'], u'Ru Kim Sa Ru | Facebook')
        self.assertEqual(res['sn'][96]['s'], u'Ru Kim Sa Ru is on Facebook. Join Facebook to connect with Ru Kim Sa Ru and others you may know. Facebook gives people the power to share and makes the...')
        self.assertEqual(res['sn'][96]['u'], u'https://www.facebook.com/ru.kimsaru')
        self.assertEqual(res['sn'][96]['d'], 'facebook.com')
        self.assertEqual(res['sn'][96]['vu'], None)

    def test130(self):
        u""""
            Ошибка парсинга от 2021-10-28
        """
        html = self.get_data('2021-10-28-2.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 139000)
        self.assertEqual(len(res['sn']), 98)

        self.assertEqual(res['sn'][0]['t'], u'Отзывы о препарате Ингавирин - Все аптеки')
        self.assertEqual(res['sn'][0]['s'], u'Очень хорошее средство против вирусов различных простуд и прочих осенних и зимних неприятностей. Лично мной было перепробовано многовсего, ...')
        self.assertEqual(res['sn'][0]['u'], u'https://vseapteki.ru/review/18282-ingavirin/')
        self.assertEqual(res['sn'][0]['d'], 'vseapteki.ru')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][67]['t'], u'Правда ли, что «Ингавирин» это запрещённое лекарство ...')
        self.assertEqual(res['sn'][67]['s'], u'Заявление: «Ингавирин» это запрещённое лекарство, которое вызывает рак')
        self.assertEqual(res['sn'][67]['u'], u'https://factcheck.kz/claim-checking/verdict/pravda-li-chto-ingavirin-eto-zapreshhyonnoe-lekarstvo-kotoroe-vyzyvaet-rak/')
        self.assertEqual(res['sn'][67]['d'], 'factcheck.kz')
        self.assertEqual(res['sn'][67]['vu'], None)

        self.assertEqual(res['sn'][97]['t'], u'Ингавирин при гв: можно ли кормящим мамам - ПростоГВ')
        self.assertEqual(res['sn'][97]['s'], u'Можно ли принимать Ингавирин при грудном вскармливании. Состав и показания к применению Ингавирина. Аналоги Ингавирина при гв.')
        self.assertEqual(res['sn'][97]['u'], u'https://prostogv.ru/healthandbeauty/medicaments/ingavirin-pri-gv')
        self.assertEqual(res['sn'][97]['d'], 'prostogv.ru')
        self.assertEqual(res['sn'][97]['vu'], None)

    def test123(self):
        u""""
            Ошибка парсинга от 2021-06-08
        """
        html = self.get_data('2021-06-08.html')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertTrue(g.is_suspicious_traffic())

    def test131(self):
        u""""
            Ошибка парсинга от 2021-11-22
        """
        html = self.get_data('2021-11-22.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 0)
        self.assertEqual(len(res['sn']), 98)

        self.assertEqual(res['sn'][0]['t'], u'Купить раскладной диван в классическом стиле в Москве - Цены от производителя в интернет-магазине MrDivanoff')
        self.assertEqual(res['sn'][0]['s'], u'Большой выбор раскладных диванов в классическом стиле - в каталоге более 1455 моделей различных размеров, расцветок, материалов. ⭐ Доставка и сборка!')
        self.assertEqual(res['sn'][0]['u'], 'https://mrdivanoff.ru/katalog/divany/raskladnye/klassicheskie-24')
        self.assertEqual(res['sn'][0]['d'], 'mrdivanoff.ru')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][67]['t'], u'Диваны в классическом стиле фото: угловые в гостиную, раскладные - VseMe.ru')
        self.assertEqual(res['sn'][67]['s'], u'Классика вне моды. Таковы и диваны в классическом стиле: они сочетают в себе надежность, функциональность, комфорт и красоту.')
        self.assertEqual(res['sn'][67]['u'], 'https://vseme.ru/gostinaya/divany-v-klassicheskom-stile')
        self.assertEqual(res['sn'][67]['d'], 'vseme.ru')
        self.assertEqual(res['sn'][67]['vu'], None)

        self.assertEqual(res['sn'][97]['t'], u'Прямые диваны раскладные на каждый день [75+ Моделей 2019] - HappyModern')
        self.assertEqual(res['sn'][97]['s'], u'26 сент. 2017 г. — Прямые раскладные диваны на каждый день производятся, как правило, в классическом стиле, однако, бывают и более оригинальные варианты.')
        self.assertEqual(res['sn'][97]['u'], 'https://happymodern.ru/pryamye-divany-raskladnye-na-kazhdyj-den/')
        self.assertEqual(res['sn'][97]['d'], 'happymodern.ru')
        self.assertEqual(res['sn'][97]['vu'], None)

    def test132(self):
        u""""
            Ошибка парсинга от 2022-01-13
        """
        html = self.get_data('2022-01-13.txt')
        g = GoogleJsonParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm'))
        self.assertFalse(g.is_suspicious_traffic())

        res = g.get_serp()

        # В мобильной выдаче похоже нет общего кол-ва результатов
        self.assertEqual(res['pc'], 30)
        self.assertEqual(len(res['sn']), 28)

        self.assertEqual(res['sn'][0]['t'], u'Отзывы о магазине ComTermo - Яндекс.Маркет')
        self.assertEqual(res['sn'][0]['s'], u'Интернет-магазин ComTermo: рейтинг — 5.0 из 5 на основании 6824 оценок. Отзывы покупателей, достоинства и недостатки. ... www.comtermo.ru.')
        self.assertEqual(res['sn'][0]['u'], u'https://market.yandex.ru/shop--comtermo-msk/89404/reviews')
        self.assertEqual(res['sn'][0]['d'], 'market.yandex.ru')
        self.assertEqual(res['sn'][0]['vu'], None)

        self.assertEqual(res['sn'][20]['t'], u'Котлы и котельное оборудование в Видном')
        self.assertEqual(res['sn'][20]['s'], u'Интернет-магазин Bosch-online.ru. Москва, Дорожная улица, 60 ... http://pressclass.ru. ГК Теплогазоснабжение. открыто. 1 отзыв ... https://www.comtermo.ru.')
        self.assertEqual(res['sn'][20]['u'], u'https://vidnoe.spravka.ru/stroitelstvo-i-remont/kotly-i-kotelnoe-oborudovanie')
        self.assertEqual(res['sn'][20]['d'], 'vidnoe.spravka.ru')
        self.assertEqual(res['sn'][20]['vu'], None)

        self.assertEqual(res['sn'][27]['t'], u'Все отзывы о товарах магазина Santehmoll')
        self.assertEqual(res['sn'][27]['s'], u'Отзывы о магазине сантехники SantehMoll. Купить аксессуары, сантехнику, мебель для ванной комнаты в Москве. Лучшие цены, скидки.')
        self.assertEqual(res['sn'][27]['u'], u'https://santehmoll.ru/all_reviews/')
        self.assertEqual(res['sn'][27]['d'], 'santehmoll.ru')
        self.assertEqual(res['sn'][27]['vu'], None)

    def print_sn(self, res):
        for i in res['sn']:
            print
            print i.get('p')
            print i.get('u')
            print i.get('t')
            print i.get('s')
            print i.get('h')


    def check2(self, snippets, founded):
        for i, founded_snippet in enumerate(founded):
            snippet = snippets[i]
            self.assertEqual(founded_snippet['p'], snippet['p'])
            self.assertEqual(founded_snippet['u'], snippet['u'])
            self.assertEqual(founded_snippet['t'], snippet['t'])
            self.assertEqual(founded_snippet['s'], snippet['s'])

    def check(self, snippets, founded):
        for i, founded_snippet in enumerate(founded):
            position, url, title, snippet = snippets[i]
            self.assertEqual(founded_snippet['p'], position)
            self.assertEqual(founded_snippet['u'], url)
            self.assertEqual(founded_snippet['t'], title)
            self.assertEqual(founded_snippet['s'], snippet)


if __name__ == '__main__':
    unittest.main()
