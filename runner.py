from scrapper import Vivo
import mandrill

def run():
    client = Vivo()
    client._parse()
    availables = client._save_tickets()

    if len(availables) > 0:
        mandrill_client = mandrill.Mandrill('wmwohycS5Po67rg7gK0Xmw')
        message = {
           'from_email': 'thiagogds14@gmail.com',
           'from_name': 'Vivo Scrapper',
           'subject': 'Tem evento novo!!!!',
           'text': 'http://www.tvantagens.com.br/',
           'to': [{'email': 'thiagogds14@gmail.com',
                'type': 'to'}],
        }

        mandrill_client.messages.send(message=message)

if __name__ == '__main__':
    run()
