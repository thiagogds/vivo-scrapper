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

if __name__ == '__main__':
    unittest.main()
