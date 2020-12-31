import asyncio
class ExampleHandler:
  async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
    if not address.endswith('@gmail.com'):
        return '550 not relaying to that domain'
    envelope.rcpt_tos.append(address)
    return '250 OK'
async def handle_DATA(self, server, session, envelope):
    print('Message from %s' % envelope.mail_from)
    print('Message for %s' % envelope.rcpt_tos)
    print('Message data:\n')
    print(envelope.content.decode('utf8', errors='replace'))
    print('End of message')
    return '250 Message accepted for delivery'
from aiosmtpd.controller import Controller
controller = Controller(ExampleHandler())
controller.start()
from smtplib import SMTP as Client
client = Client(controller.hostname, controller.port)
r = client.sendmail('vednig12@gmail.com', ['vednig12@gmail.com'], """\
 From: VedNig <vednig12@gmail.com
 To: VedNig <vednig12@gmail.com>
 Subject: A test
 Message-ID: <ant>

 Hi Bart, this is Anne.
 """)
