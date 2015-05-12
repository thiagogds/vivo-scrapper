#coding: utf-8
import os
import shutil

import unittest
import vcr
import coopy.base
from unittest import TestCase
from unipath import Path

from src.scrapper import Vivo, Wallet

FILE_DIR = Path(__file__)
VCR_DIR = Path(FILE_DIR.parent, 'fixtures/vcr_cassettes')

TEST_DIR = 'coopy_test/'

class VivoScrapeerTest(TestCase):
    def setUp(self):
        os.mkdir(TEST_DIR)

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

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
        html = client._get("http://www.tvantagens.com.br/listarEventos.action")

        self.assertIn('Ingressos gr&aacute;tis', html)

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

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions.yaml'))
    def test_save_tickets(self):
        client = Vivo(TEST_DIR)
        client._parse()
        client._save_tickets()

        wallet = coopy.base.init_persistent_system(Wallet(), basedir=TEST_DIR)
        ticket = wallet.get_ticket("7efe1e063a6bfbaa5c865f31d0a57e46")

        self.assertEqual('QUERO MATAR MEU CHEFE 2', ticket.name)
        self.assertEqual('BK', ticket.avaliabilty)
        self.assertEqual('7efe1e063a6bfbaa5c865f31d0a57e46', ticket.id)
        self.assertEqual('03/12/2014', ticket.date)

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions.yaml'))
    def test_dont_save_tickets_twice(self):
        client = Vivo(TEST_DIR)
        client._parse()
        client._save_tickets()
        client._save_tickets()

        wallet = coopy.base.init_persistent_system(Wallet(), basedir=TEST_DIR)
        count = wallet.count_tickets()
        self.assertEqual(10, count)

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions.yaml'))
    def test_return_avalaible_tickets_at_create(self):
        client = Vivo(TEST_DIR)
        client._parse()
        availables = client._save_tickets()

        self.assertEqual(1, len(availables))
        self.assertEqual('QUERO MATAR MEU CHEFE 2', availables[0].name)

        availables = client._save_tickets()
        self.assertEqual(0, len(availables))

    def test_update_tickets(self):
        tickets = [
            {'date': '02/12/2014', 'name': 'OS CARAS DE PAUS', 'avaliabilty': 'CL', 'id': "6146707aa13ca3946e60757349c0a9d6"},
        ]

        client = Vivo(TEST_DIR)
        client.tickets = tickets
        client._save_tickets()

        new_tickets = [
            {'date': '02/12/2014', 'name': 'OS CARAS DE PAUS', 'avaliabilty': 'BK', 'id': "6146707aa13ca3946e60757349c0a9d6"},
        ]

        client.tickets = new_tickets
        availables = client._save_tickets()

        wallet = coopy.base.init_persistent_system(Wallet(), basedir=TEST_DIR)
        updated = wallet.get_ticket("6146707aa13ca3946e60757349c0a9d6")
        self.assertEqual("BK", updated.avaliabilty)
        self.assertEqual(1, len(availables))

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions_with_cancel.yaml'))
    def test_cancel_in_avaliability(self):
        client = Vivo()
        client._parse()

        expected_list = [
            {'date': '22/02/2015', 'name': 'NOITE INFELIZ - A COMEDIA MUSICAL DAS MALDADES', 'avaliabilty': 'CA', 'id': "ede5d5105c2098e56ef88fc0987765a4"},
        ]

        for expected_item in expected_list:
            self.assertIn(expected_item, client.tickets)

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotion_detail.yaml'))
    def test_get_promotion_page(self):
        page_url = u"http://www.tvantagens.com.br/detalharEvento.action?caMktEvtCod=PRE21706&k=d95dae5e0a1c5e343959cb76b1f94672"
        client = Vivo()
        html = client._get(page_url)

        self.assertIn("Detalhes do Evento", html)

