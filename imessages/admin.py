# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils import timezone

from clients.models import ClientPhone
from imessages.models import Message
from imessages.sending import send_imessage


class MessageAdmin(admin.ModelAdmin):

    fields = (
        'content',
        'phone'
    )

    list_display = fields + ('send_at', 'is_sent', 'phone')

    actions = [
        'send',
    ]

    def send(self, request, queryset):
        for msg in queryset.order_by('created_at'):
            if not msg.is_sent:
                send_imessage(msg.phone.phone_number, msg.content)
                msg.send_at = timezone.now()
                msg.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "phone":
            kwargs["queryset"] = ClientPhone.objects.order_by('client__label')
        return super(MessageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Message, MessageAdmin)
