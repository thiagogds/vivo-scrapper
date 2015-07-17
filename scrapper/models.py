#coding: utf-8
from django.db import models

class Ticket(models.Model):
    CLOSED = 'CL'
    BOOK = 'BK'
    SOLD_OUT = 'SO'
    CANCEL = 'CA'

    internal_id = models.CharField(u"ID na Vivo", max_length=255, null=True, blank=True)
    name = models.CharField(u"Nome", max_length=255, null=True, blank=True)
    avaliability = models.CharField(u"Disponibilidade", max_length=255, null=True, blank=True)
    date = models.DateTimeField(u"Data e hora", null=True, blank=True)
    link = models.CharField(u"Link", max_length=255, null=True, blank=True)
    location = models.CharField(u"Localização", max_length=255, null=True, blank=True)
    address = models.CharField(u"Endereço", max_length=255, null=True, blank=True)
    description = models.TextField(u"Descrição", null=True, blank=True)

    def add_ticket(self):
        already_available = False
        try:
            old_ticket = self.get_ticket(self.id)
            index = self.tickets.index(old_ticket)
            self.tickets.pop(index)
            if old_ticket.avaliabilty == avaliabilty_choices[BOOK]:
                already_available = True
        except:
            pass

        self.tickets.append(ticket)
        if not already_available and ticket.avaliabilty == avaliabilty_choices[BOOK]:
            return ticket

