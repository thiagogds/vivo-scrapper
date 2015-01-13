#coding: utf-8

import unittest
import vcr
from unittest import TestCase
from unipath import Path

from scrapper import Vivo

FILE_DIR = Path(__file__)
VCR_DIR = Path(FILE_DIR.parent, 'fixtures/vcr_cassettes')

class VivoScrapeerTest(TestCase):
    @vcr.use_cassette(Path(VCR_DIR, 'vivo_login.yaml'))
    def test_post_login(self):
        client = Vivo()
        client._login()

        self.assertEqual(
            'B8C895AD7923AC793062FA5DA5230FC3',
            client.session.cookies['JSESSIONID']
        )

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions.yaml'))
    def test_get_promotions_list(self):
        client = Vivo()
        client._promotions_page()

        self.assertIn('Ingressos gr&aacute;tis', client.events_list_html)

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions.yaml'))
    def test_parse_html(self):
        client = Vivo()
        client._parse()

        expected_list = [
            {'date': '02/12/2014', 'name': 'OS CARAS DE PAUS', 'avaliabilty': 'CL', 'id': "6146707aa13ca3946e60757349c0a9d6"},
            {'date': '03/12/2014', 'name': 'QUERO MATAR MEU CHEFE 2', 'avaliabilty': 'BK', 'id': "7efe1e063a6bfbaa5c865f31d0a57e46"},
            {'date': '04/12/2014', 'name': u'CHUVA CONSTANTE - A FELICIDADE \xc9 FORA DA LEI', 'avaliabilty': 'SO', 'id': "49d33f9135849ba4db71589662dcf1d3"}
        ]

        for expected_item in expected_list:
            self.assertIn(expected_item, client.tickets)


if __name__ == '__main__':
    unittest.main()
