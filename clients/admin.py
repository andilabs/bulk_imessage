# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Client, ClientPhone


class ClientAdmin(admin.ModelAdmin):

    fields = (
        'label',
    )

    search_fields = ('label', )
    list_display = fields


class ClientPhoneAdmin(admin.ModelAdmin):

    fields = (
        'phone_number',
        'client'
    )

    list_display = fields
    search_fields = ('client__label', 'phone_number')


admin.site.register(Client, ClientAdmin)
admin.site.register(ClientPhone, ClientPhoneAdmin)