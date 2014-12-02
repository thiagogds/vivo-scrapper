from decouple import config
import requests

class Vivo(object):
    def __init__(self):
        self.login_url = "http://www.tvantagens.com.br/autenticar-participante.action"
        self.promotions_url = "http://www.tvantagens.com.br/listarEventos.action"
        self.cpf = config('LOGIN')
        self.password = config('PASSWORD')
        self.session = requests.Session()

    def _login(self):
        payload = {'caDoc': self.cpf, 'anSenha': self.password}
        response = self.session.post(self.login_url, data=payload)

    def _promotions_page(self):
        self._login()
        response = self.session.get(self.promotions_url)
        self.events_list_html = response.text
