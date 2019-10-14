from django.contrib import admin

from .models import Contact, ContactPhone


class ContactPhoneInline(admin.TabularInline):
    model = ContactPhone


class ContactAdmin(admin.ModelAdmin):

    fields = (
        'label',
        'raw_vcard',
    )
    inlines = [
        ContactPhoneInline,
    ]

    search_fields = ['label', 'raw_vcard']
    list_display = fields


class ContactPhoneAdmin(admin.ModelAdmin):
    list_filter = ['service']
    fields = (
        'phone_number',
        'contact',
        'service',
    )

    list_display = fields
    search_fields = ['contact__label']


admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactPhone, ContactPhoneAdmin)
