#! coding: utf-8


import unittest
from google_parser.tests import GoogleParserTests
from google_parser.google import GoogleParser


class GoogleParserTestCase(GoogleParserTests):
    def test_http(self):
        snippets = [
            (1, "https://www.express-bank.ru/moscow/faq/cards", u"Часто задаваемые вопросы о банковских картах | Восточный ...", u"Карты Восточного экспресс банка  можно использовать за границей?  ...     экспресс  банком , можно использовать за рубежом:  оплачивать  товары и    услуги в  ..."),
            (2, "https://www.express-bank.ru/moscow/private/payments", u"Оплата товаров и услуг | Восточный экспресс банк", u"Банковская карта  Visa от  Восточного экспресс банка  принимается к  оплате     везде, где стоит знак Visa. Оплачивайте товары и услуги с помощью  ..."),
            (3, "https://www.express-bank.ru/moscow/private/cards/debit", u"Дебетовые карты - Восточный экспресс банк", u"Предлагаем дебетовые  банковские карты  Visa.  ...  С помощью карты вы    можете  оплачивать  необходимые покупки, осуществлять накопления,    снимать  ..."),
            (4, "https://www.express-bank.ru/moscow/private/terminals", u"Терминалы оплаты | Восточный экспресс банк", u"Терминалы  оплаты   ...  Процесс  оплаты  простой и занимает всего несколько    минут. Деньги на нужный счет  ...  ( карты  сторонних  банков  отключены)."),
            (5, "https://www.express-bank.ru/moscow/private/payments/credit", u"Погашение кредитов | Восточный экспресс банк", u"3. В отделении  Восточного экспресс банка . При наличии  карты Восточного   экспресс банка  можно  оплатить  кредит кассе отделения, что существенно  ..."),
            (6, "https://www.express-bank.ru/moscow/private/credits/repayment", u"Как оплачивать кредит | Восточный экспресс банк", u"1. В отделении  Восточного экспресс банка . Обслуживание в кассе    осуществляется только при наличии пластиковой  карты . Наличие  карты     значительно  ..."),
            (7, "https://www.express-bank.ru/moscow/faq/credit-card", u"Часто задаваемые вопросы о картах | Восточный экспресс банк", u"В случае  оплаты  покупки в долларах США или евро «рублевой»  картой ,    конвертация происходит по курсу  банка  на момент списания средств со    счёта  ..."),
            (8, "https://www.express-bank.ru/moscow/private/payments/automts", u"Автоплатежи МТС | Восточный экспресс банк", u"Восточный экспресс банк   ...  Если вы не являетесь держателем  карты   Восточного экспресс банка , обратитесь в ближайшее  ...   Оплата  товаров и    услуг."),
            (9, "https://www.express-bank.ru/moscow/private/online/internet/posibilities", u"Возможности интернет-банка | Восточный экспресс банк", u"Совершайте  банковские  операции по своим счетам дистанционно.  ...     денежных средств,  оплачивать  покупки и услуги в режиме реального    времени.  ...  кредиту;; по кредитной  карте , которая включает сумму    минимального платежа,  ..."),
            (10, "https://www.express-bank.ru/moscow/faq/credit-price", u"Обслуживание кредита, кредитной карты | Восточный экспресс ...", u"Наиболее частые вопросы по обслуживанию кредита, кредитной  карты .  ...  ли    я  оплатить  задолженность по кредиту/кредитной  карте  в филиале  Банка  в  ..."),
        ]
        html = self.get_data('google.html')
        founded = GoogleParser(html).get_snippets()
        self.check(snippets, founded)

    def test_ftp(self):
        snippets = [
            (1, "ftp://os2.fannet.ru/Boating/books/kija-new/2009-06%20(222).pdf", u"техника", u"в «базе»  нет  удобного раскладывающегося сто- лика – он  .....   РИБа  «   Кальмар» с мотором от. «Волги», не  .....  если выполнить ее  складной  и    снабдить  ....  гое время на одной и той же лодке «SkyBoat  440 » (сегодня  ......     остойчивости на  дно  укладывают бал- ласт.  ......  (ее составили «Олимп» и « Люкс » из."),
        ]

        html = self.get_data('google-ftp.html')
        founded = GoogleParser(html).get_snippets()
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

    def test4(self):
        u""""
            Ничего не найдено есть
        """
        html = self.get_data('not-found.html')
        g = GoogleParser(html)
        self.assertEqual(g.is_not_found(), True)

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
        html = self.get_data('not_found_2.html')
        g = GoogleParser(html)
        self.assertEqual(g.is_not_found(), True)

    def test8(self):
        u""""
            Ничего не найдено есть
        """
        html = self.get_data('not_found_3.html')
        g = GoogleParser(html)
        self.assertEqual(g.is_not_found(), True)

    def test5(self):
        u""""
            Ничего не найдено нет
        """
        html = self.get_data('google.html')
        g = GoogleParser(html)
        self.assertEqual(g.is_not_found(), False)

    def check(self, snippets, founded):
        for i, founded_snippet in enumerate(founded):
            position, url, title, snippet = snippets[i]
            self.assertEqual(founded_snippet['p'], position)
            self.assertEqual(founded_snippet['u'], url)
            self.assertEqual(founded_snippet['t'], title)
            self.assertEqual(founded_snippet['s'], snippet)


if __name__ == '__main__':
    unittest.main()
