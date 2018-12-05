#! coding: utf-8
import json

import unittest
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
        self.assertEqual(len(res['sn']), 100)

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

        self.assertEqual(res['sn'][0]['t'], u'Массаж на Новослободской:(495)786-97-98, ул ... - Целлюлайтhttps://www.cellulait.ru/contacts/')
        self.assertEqual(res['sn'][0]['s'], u'9 мая 2018 г. - Массаж на Новослободской. Адрес клиники косметологии которая поможет Вам привести Вашу фигуру к идеальным формам.')
        self.assertEqual(res['sn'][0]['u'], u'https://www.cellulait.ru/contacts/')
        self.assertEqual(res['sn'][0]['d'], 'cellulait.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.cellulait.ru/contacts/')

        self.assertEqual(res['sn'][99]['t'], u'Целлюлайт: Москва Новослободская улица 61с1 - RusMap.nethttps://rusmap.net &rsaquo; Москва &rsaquo; Фирмы &rsaquo; Салоны красоты')
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

        self.assertEqual(res['sn'][0]['t'], u'Посуда Fissler – купить посуду Фисслер в Москве, цены в ...www.fissler-shop.ru/')
        self.assertEqual(res['sn'][0]['s'], u'В интернет-магазине компании Сандер в Москве представлен ассортимент немецкой посуды для индукционных плит Fissler. Она удовлетворит вкусы ...')
        self.assertEqual(res['sn'][0]['u'], u'http://www.fissler-shop.ru/')
        self.assertEqual(res['sn'][0]['d'], 'fissler-shop.ru')
        self.assertEqual(res['sn'][0]['vu'], u'www.fissler-shop.ru/')

        self.assertEqual(res['sn'][47]['t'], u'Наборы посуды для готовки — купить на Яндекс.Маркетеhttps://market.yandex.ru/catalog--nabory-posudy-dlia-gotovki/61640/list?glfilter...')
        self.assertEqual(res['sn'][47]['s'], u'FISSLER Набор посуды из 5-ти предметов: три кастрюли, сотейник и ковшик без ... наборы посуды и кастрюль Fissler Набор кастрюль, 5 предметов, ...')
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

        self.assertEqual(res['sn'][0]['t'], u'Флавитал инструкция по применению, Флавитал цена, Флавитал ...https://www.piluli.ru &rsaquo; ... &rsaquo; Лечение онкологических заболеваний')
        self.assertEqual(res['sn'][0]['s'], u'Цены на Флавитал, подробная инструкция по применению, противопоказания, побочные действия, состав на сайте интернет-аптеки www.piluli.ru.')
        self.assertEqual(res['sn'][0]['u'], u'https://www.piluli.ru/product/flavital')
        self.assertEqual(res['sn'][0]['d'], 'piluli.ru')
        self.assertEqual(res['sn'][0]['vu'], u'https://www.piluli.ru › ... › Лечение онкологических заболеваний')

        self.assertEqual(res['sn'][98]['t'], u'Flavital - Profile - Robloxhttps://www.roblox.com/users/529521610/profile')
        self.assertEqual(res['sn'][98]['s'], u'Flavital is one of the millions playing, creating and exploring the endless possibilities of Roblox. Join Flavital on Roblox and explore together!')
        self.assertEqual(res['sn'][98]['u'], u'https://www.roblox.com/users/529521610/profile')
        self.assertEqual(res['sn'][98]['d'], 'roblox.com')
        self.assertEqual(res['sn'][98]['vu'], u'https://www.roblox.com/users/529521610/profile')

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
