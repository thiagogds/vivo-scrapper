#coding: utf-8
import os
import shutil
import datetime

import unittest
import vcr
from django.test import TestCase
from unipath import Path
from decouple import config
from django.utils.timezone import make_aware, utc

from scrapper.scrapper import Vivo
from scrapper.models import Ticket

FILE_DIR = Path(__file__)
VCR_DIR = Path(FILE_DIR.parent, 'fixtures/vcr_cassettes')

class VivoScrapperTest(TestCase):
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
        html = client._get(config('PROMOTIONS_URL'))

        self.assertIn('Ingressos gr&aacute;tis', html)

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions.yaml'))
    def test_parse_html(self):
        client = Vivo()
        client._parse()

        expected_list = [
            {'name': 'OS CARAS DE PAUS', 'avaliability': 'CL', 'internal_id': "6146707aa13ca3946e60757349c0a9d6", 'link': 'detalharEvento.action?caMktEvtCod=PRE20018&k=6146707aa13ca3946e60757349c0a9d6'},
            {'name': 'QUERO MATAR MEU CHEFE 2', 'avaliability': 'BK', 'internal_id': "7efe1e063a6bfbaa5c865f31d0a57e46", 'link': 'detalharEvento.action?caMktEvtCod=PRE20002&k=7efe1e063a6bfbaa5c865f31d0a57e46'},
            {'name': u'CHUVA CONSTANTE - A FELICIDADE \xc9 FORA DA LEI', 'avaliability': 'SO', 'internal_id': "49d33f9135849ba4db71589662dcf1d3", 'link': 'detalharEvento.action?caMktEvtCod=PCT20032&k=49d33f9135849ba4db71589662dcf1d3'},
        ]

        for expected_item in expected_list:
            self.assertIn(expected_item, client.tickets)

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions.yaml'))
    def test_save_tickets(self):
        client = Vivo()
        client._parse()
        client._save_tickets()

        ticket = Ticket.objects.get(internal_id="7efe1e063a6bfbaa5c865f31d0a57e46")

        self.assertEqual('QUERO MATAR MEU CHEFE 2', ticket.name)
        self.assertEqual('BK', ticket.avaliability)
        self.assertEqual('7efe1e063a6bfbaa5c865f31d0a57e46', ticket.internal_id)

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions.yaml'))
    def test_dont_save_tickets_twice(self):
        client = Vivo()
        client._parse()
        client._save_tickets()
        client._save_tickets()

        count = Ticket.objects.count()
        self.assertEqual(10, count)

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions.yaml'))
    def test_return_avalaible_tickets_at_create(self):
        #Somehow django isn't cleaning test DB :(
        Ticket.objects.all().delete()
        client = Vivo()
        client._parse()

        availables = client._save_tickets()
        self.assertEqual(1, len(availables))
        self.assertEqual('QUERO MATAR MEU CHEFE 2', availables[0].name)

        availables = client._save_tickets()
        self.assertEqual(0, len(availables))

    def test_update_tickets(self):
        tickets = [
            {'name': 'OS CARAS DE PAUS', 'avaliability': 'CL', 'internal_id': "6146707aa13ca3946e60757349c0a9d6", 'link': 'detalharEvento.action?caMktEvtCod=PCT20672&k=ede5d5105c2098e56ef88fc0987765a4'},
        ]

        client = Vivo()
        client.tickets = tickets
        client._save_tickets()

        new_tickets = [
            {'name': 'OS CARAS DE PAUS', 'avaliability': 'BK', 'internal_id': "6146707aa13ca3946e60757349c0a9d6", 'link': 'detalharEvento.action?caMktEvtCod=PCT20672&k=ede5d5105c2098e56ef88fc0987765a4'},
        ]

        client.tickets = new_tickets
        availables = client._save_tickets()

        updated = Ticket.objects.get(internal_id="6146707aa13ca3946e60757349c0a9d6")
        self.assertEqual("BK", updated.avaliability)
        self.assertEqual(1, len(availables))

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions_with_cancel.yaml'))
    def test_cancel_in_avaliability(self):
        client = Vivo()
        client._parse()

        expected_list = [
            {'name': 'NOITE INFELIZ - A COMEDIA MUSICAL DAS MALDADES', 'avaliability': 'CA', 'internal_id': "ede5d5105c2098e56ef88fc0987765a4", 'link': 'detalharEvento.action?caMktEvtCod=PCT20672&k=ede5d5105c2098e56ef88fc0987765a4'},
        ]

        for expected_item in expected_list:
            self.assertIn(expected_item, client.tickets)

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotion_detail.yaml'))
    def test_get_promotion_page(self):
        page_url = u"detalharEvento.action?caMktEvtCod=PRE21706&k=d95dae5e0a1c5e343959cb76b1f94672"
        client = Vivo()
        html = client._get(page_url)

        self.assertIn("Detalhes do Evento", html)

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotion_detail.yaml'))
    def test_parse_promotion_page(self):
        page_url = u"detalharEvento.action?caMktEvtCod=PRE21706&k=d95dae5e0a1c5e343959cb76b1f94672"
        client = Vivo()
        detail = client._parse_detail(page_url)
        expected_detail = {
            'date': u'13/05/2015 às 21:00h',
            'location': u"CINEMARK BOTAFOGO",
            'address': u"R PRAIA DE BOTAFOGO, 400, BOTAFOGO - RIO DE JANEIRO - RJ, CEP: 22250-040",
            'description': u"Eduarda (Vanessa Giácomo) é uma ortopedista bem sucedida, casada com o produtor de eventos Marcos (Rafael Infante) há 10 anos. Devido ao desgaste do relacionamento, eles resolvem fazer uma terapia de casal. Só que, durante as sessões, eles decidem se separar. É quando Eduarda conhece Leo (Marcelo Serrado), por quem fica interessada",
        }

        self.assertEqual(detail, expected_detail)

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions_details.yaml'))
    def test_add_more_info_to_tickets(self):
        client = Vivo()
        client._get_ticket_info()

        expected_event = {
                'name': u'DIVÂ A 2',
                'avaliability': u'SO',
                'internal_id': "d95dae5e0a1c5e343959cb76b1f94672",
                'link': "detalharEvento.action?caMktEvtCod=PRE21706&k=d95dae5e0a1c5e343959cb76b1f94672",
                'date': u'13/05/2015 às 21:00h',
                'location': u"CINEMARK BOTAFOGO",
                'address': u"R PRAIA DE BOTAFOGO, 400, BOTAFOGO - RIO DE JANEIRO - RJ, CEP: 22250-040",
                'description': u"Eduarda (Vanessa Giácomo) é uma ortopedista bem sucedida, casada com o produtor de eventos Marcos (Rafael Infante) há 10 anos. Devido ao desgaste do relacionamento, eles resolvem fazer uma terapia de casal. Só que, durante as sessões, eles decidem se separar. É quando Eduarda conhece Leo (Marcelo Serrado), por quem fica interessada",
        }

        self.assertIn(expected_event, client.tickets)

    @vcr.use_cassette(Path(VCR_DIR, 'vivo_promotions_details.yaml'))
    def test_save_ticket_full_info(self):
        client = Vivo()
        client._get_ticket_info()
        client._save_tickets()

        ticket = Ticket.objects.get(internal_id="d95dae5e0a1c5e343959cb76b1f94672")

        self.assertEqual(u'DIVÂ A 2', ticket.name)
        self.assertEqual('SO', ticket.avaliability)
        self.assertEqual('d95dae5e0a1c5e343959cb76b1f94672', ticket.internal_id)
        self.assertEqual('detalharEvento.action?caMktEvtCod=PRE21706&k=d95dae5e0a1c5e343959cb76b1f94672', ticket.link)
        self.assertEqual(make_aware(datetime.datetime(2015, 5, 14, 0, 0), timezone=utc), ticket.date)
        self.assertEqual(u'CINEMARK BOTAFOGO', ticket.location)
        self.assertEqual(u'R PRAIA DE BOTAFOGO, 400, BOTAFOGO - RIO DE JANEIRO - RJ, CEP: 22250-040', ticket.address)
