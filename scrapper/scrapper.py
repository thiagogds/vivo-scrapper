#coding: utf-8
import requests
from datetime import datetime
from decouple import config
from pyquery import PyQuery as pq
from lxml import etree
from coopy.base import init_persistent_system
from django.utils.timezone import make_aware

from .models import Ticket

CLOSED = u'reservas encerradas'
BOOK = u'reservar'
SOLD_OUT = u'Esgotado'
CANCEL = u'cancelar a reserva'

avaliability_choices = {
    CLOSED: Ticket.CLOSED,
    BOOK: Ticket.BOOK,
    SOLD_OUT: Ticket.SOLD_OUT,
    CANCEL: Ticket.CANCEL,
}

def value(tr):
    return tr.xpath("normalize-space(td[2])")

class Vivo(object):
    def __init__(self):
        self.host = "http://www.tvantagens.com.br/"
        self.login_url = self.host + "autenticar-participante.action"
        self.promotions_url = config('PROMOTIONS_URL')
        self.cpf = config('LOGIN')
        self.password = config('PASSWORD')
        self.session = requests.Session()
        self.tickets = []

    def _login(self):
        payload = {'caDoc': self.cpf, 'anSenha': self.password}
        response = self.session.post(self.login_url, data=payload)

    def _get(self, page_url):
        self._login()
        response = self.session.get(self.host+page_url)
        return response.text

    def _parse(self):
        html = pq(self._get(self.promotions_url))
        trs = html("body > div.content_geral > div.universo_content > div > div.conteudoHome > div.port-row > div > div > table tr")

        for tr in trs.items():
            ticket = {}

            href = tr('.titulo a').attr['href']
            name = tr('.titulo').text()
            avaliability = tr('.disponibilidade').text()

            if u"\xbb" in avaliability:
                avaliability = avaliability[2:]

            if name and avaliability:
                ticket['internal_id'] = href.split('&')[1][2:]
                ticket['link'] = href
                ticket['name'] = name
                ticket['avaliability'] = avaliability_choices[avaliability]
                self.tickets.append(ticket)
    def _parse_datetime(self, str_datetime):
        return make_aware(datetime.strptime(str_datetime.encode('utf-8'), '%d/%m/%Y às %H:%Mh'))

    def _parse_detail(self, page_url):
        html = pq(self._get(page_url))
        trs = html(".tabela01 tr")

        detail = {}
        detail['date'] = value(trs[2])
        detail['location'] = value(trs[5])
        detail['address'] = value(trs[6])
        detail['description'] = html("#geral > div.txtRegulamento > p:nth-child(2)").text()

        return detail

    def _get_ticket_info(self):
        self._parse()
        for ticket in self.tickets:
            ticket.update(self._parse_detail(ticket['link']))

    def _save_tickets(self):
        availables = []
        for item in self.tickets:
            if item.get('date'):
                item['date'] = self._parse_datetime(item['date'])
            ticket = Ticket.objects.filter(internal_id=item['internal_id'])
            if len(ticket):
                was_available = ticket.first().avaliability == Ticket.BOOK
                ticket.update(**item)
                is_available = ticket.first().avaliability == Ticket.BOOK

                if not was_available and is_available:
                    availables.append(ticket)
            else:
                ticket = Ticket.objects.create(**item)
                is_available = ticket.avaliability == Ticket.BOOK

                if is_available:
                    availables.append(ticket)

        return availables
