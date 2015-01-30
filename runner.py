import mandrill
from decouple import config
from src.scrapper import Vivo

def run():
    client = Vivo()
    client._parse()
    availables = client._save_tickets()

    if len(availables) > 0:
        KEY = config('MANDRILL_KEY')
        mandrill_client = mandrill.Mandrill(KEY)
        message = {
           'from_email': 'thiagogds14@gmail.com',
           'from_name': 'Vivo Scrapper',
           'subject': 'Tem evento novo!!!!',
           'text': 'http://www.tvantagens.com.br/',
           'to': [
                {
                    'email': 'thiagogds14@gmail.com',
                    'type': 'to',
                },
                {
                    'email': 'rodrigopqn@gmail.com',
                    'type': 'to',
                },
                {
                    'email': 'pedrojudo@gmail.com',
                    'type': 'to',
                },
                {
                    'email': 'nandaff@poli.ufrj.br',
                    'type': 'to',
                },
                {
                    'email': 'eduardooc.86@gmail.com',
                    'type': 'to',
                },
            ],
        }

        mandrill_client.messages.send(message=message)

if __name__ == '__main__':
    run()
