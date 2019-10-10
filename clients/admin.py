from django.contrib import admin

from .models import Client, ClientPhone


class ClientPhoneInline(admin.TabularInline):
    model = ClientPhone


class ClientAdmin(admin.ModelAdmin):

    fields = (
        'label',
        'raw_vcard',
    )
    inlines = [
        ClientPhoneInline,
    ]

    search_fields = ['label', 'raw_vcard']
    list_display = fields


class ClientPhoneAdmin(admin.ModelAdmin):

    fields = (
        'phone_number',
        'client',
    )

    list_display = fields
    search_fields = ['client__label']


admin.site.register(Client, ClientAdmin)
admin.site.register(ClientPhone, ClientPhoneAdmin)
