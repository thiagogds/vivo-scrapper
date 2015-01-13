import requests
from decouple import config
from pyquery import PyQuery as pq
from lxml import etree

CLOSED = u'reservas encerradas'
BOOK = u'reservar'
SOLD_OUT = u'Esgotado'

avaliabilty_choices = {
    CLOSED: 'CL',
    BOOK: 'BK',
    SOLD_OUT: 'SO'
}

class Vivo(object):
    def __init__(self):
        self.login_url = "http://www.tvantagens.com.br/autenticar-participante.action"
        self.promotions_url = "http://www.tvantagens.com.br/listarEventos.action"
        self.cpf = config('LOGIN')
        self.password = config('PASSWORD')
        self.session = requests.Session()
        self.tickets = []

    def _login(self):
        payload = {'caDoc': self.cpf, 'anSenha': self.password}
        response = self.session.post(self.login_url, data=payload)

    def _promotions_page(self):
        self._login()
        response = self.session.get(self.promotions_url)
        self.events_list_html = response.text

    def _parse(self):
        self._promotions_page()
        html = pq(self.events_list_html)
        trs = html("body > div.content_geral > div.universo_content > div > div.conteudoHome > div.port-row > div > div > table tr")

        for tr in trs.items():
            ticket = {}

            id = tr('.titulo a').attr['href']
            name = tr('.titulo').text()
            date = tr('.data').text()
            avaliabilty = tr('.disponibilidade').text()

            if u"\xbb" in avaliabilty:
                avaliabilty = avaliabilty[2:]

            if name and date and avaliabilty:
                ticket['id'] = id.split('&')[1][2:]
                ticket['name'] = name
                ticket['date'] = date
                ticket['avaliabilty'] = avaliabilty_choices[avaliabilty]
                self.tickets.append(ticket)
