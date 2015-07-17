from django.contrib import admin
from .models import Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'avaliability')
    list_filter = ('avaliability',)

admin.site.register(Ticket, TicketAdmin)

