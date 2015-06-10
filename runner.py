import mandrill
from decouple import config
from jinja2 import Environment, PackageLoader

from src.scrapper import Vivo
env = Environment(loader=PackageLoader('src', 'templates'))


def run():
    client = Vivo()
    client._get_ticket_info()
    availables = client._save_tickets()

    if len(availables) > 0:
        KEY = config('MANDRILL_KEY')
        template = env.get_template('mail.txt')
        html_template = env.get_template('mail.html')
        text = template.render(tickets=availables)
        html = html_template.render(tickets=availables)
        mandrill_client = mandrill.Mandrill(KEY)
        message = {
           'from_email': 'thiagogds14@gmail.com',
           'from_name': 'Vivo Scrapper',
           'subject': 'Tem evento novo!!!!',
           'html': html,
           'text': text,
           'to': [
                {
                    'email': 'thiagogds14@gmail.com',
                    'type': 'to',
                },
                {
                    'email': 'rodrigopqn@gmail.com',
                    'type': 'bcc',
                },
                {
                    'email': 'pedrojudo@gmail.com',
                    'type': 'bcc',
                },
                {
                    'email': 'nandaff@poli.ufrj.br',
                    'type': 'bcc',
                },
                {
                    'email': 'eduardooc.86@gmail.com',
                    'type': 'bcc',
                },
                {
                    'email': 'henrique@bastos.net',
                    'type': 'bcc',
                },
                {
                    'email': 'luciana.cassiano@gmail.com',
                    'type': 'bcc',
                },
                {
                    'email': 'soraia.araujo@gmail.com',
                    'type': 'bcc',
                },
            ],
        }

        mandrill_client.messages.send(message=message)

if __name__ == '__main__':
    run()
