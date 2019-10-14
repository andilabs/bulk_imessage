from django import forms
from django.contrib import admin
from django.utils import timezone

from contacts.models import ContactPhone
from messaging.models import Message, DistributionList
from messaging.sending import send_message


class MessageAdmin(admin.ModelAdmin):

    fields = (
        'content',
        'phone',
        'distribution_list'
    )

    list_display = fields + ('send_at', 'is_sent', 'phone')

    actions = [
        'send',
    ]

    def send(self, request, queryset):
        for msg in queryset.order_by('created_at'):
            # if not msg.is_sent:
            send_message(
                msg.content,
                msg.phone,
                msg.distribution_list
            )
            msg.send_at = timezone.now()
            msg.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "phone":
            kwargs["queryset"] = ContactPhone.objects.order_by('contact__label')
        return super(MessageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(MessageAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'content':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


class DistributionListAdmin(admin.ModelAdmin):
    fields = (
        'label',
        'members',
    )
    autocomplete_fields = ('members', )


admin.site.register(Message, MessageAdmin)
admin.site.register(DistributionList, DistributionListAdmin)
