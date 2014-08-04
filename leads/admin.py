from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from django_mailbox.models import Message
from leads.models import LeadProperty, Lead, Customer, Property, Note


class AgencyModelAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('agency')
        return super(AgencyModelAdmin, self).get_form(request, obj, **kwargs)


class MessageInline(admin.StackedInline):
    model = Message
    extra = 0
    raw_id_fields = [
        'in_reply_to',
    ]
    exclude = (
        'mailbox',

    )


class LeadPropertyInline(admin.StackedInline):
    model = LeadProperty
    extra = 1
    raw_id_fields = ('property',)
    autocomplete_lookup_fields = {
        'fk': ['property'],
    }


class NoteInline(admin.StackedInline):
    model = Note
    extra = 1


class LeadAdmin(AgencyModelAdmin):
    list_display = (
        'source',
        'customer',
        'arrival',
        'departure',
        'lead_properties',
        'phone_call',
        'first_response',
        'second_response',
        'offer',
        'hot',
        'booked',
        'modified',
    )
    ordering = ['-created']
    list_filter = (
        'source',
        'first_response',
        'second_response',
        'offer',
        'hot',
        'booked',
        'modified',
    )
    search_fields = ['customer__first_name',
                     'customer__last_name',
                     'customer__email',
                     'properties__title',
                     'properties__address']
    date_hierarchy = 'modified'
    inlines = (LeadPropertyInline, MessageInline, NoteInline)


class CustomerAdmin(AgencyModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone',
    )
    search_fields = (
        'first_name',
        'last_name',
        'email',
    )
    list_filter = ['agency']


class PropertyAdminForm(forms.ModelForm):
    class Meta:
        model = Property
        # widgets = {
        #   'property_ids': SourceIdWidget(attrs={'class': 'TextField'}),
        # }


class PropertyAdmin(AgencyModelAdmin):
    #def get_form(self, request, obj=None, **kwargs):
    #
    #    form = super(PropertyAdmin, self).get_form(request, obj, **kwargs)
    #    for t, f in form.base_fields.items():
    #        if isinstance(f, DictionaryField):
    #            f.widget.attrs['class'] = 'TextField'
    #    return form

    form = PropertyAdminForm

    list_display = (
        'property_ids',
        'title',
        'address',
        'city',
        'approved'
    )
    search_fields = (
        'title',
        'address',
        'city__name',
        'state__name',
    )
    list_editable = [
        'title',
        'approved'

    ]
    list_filter = ['agency']


class MessageAdmin(admin.ModelAdmin):
    search_fields = ['body', 'subject', 'from_header', 'to_header']

    list_display = (
        'subject',
        'processed',
        'read',
        'outgoing',
        'lead',
        'is_lead_source',
    )
    ordering = ['-processed']
    list_filter = (
        'mailbox',
        'outgoing',
        'processed',
        'read',
        'is_lead_source',
    )
    raw_id_fields = [
        'in_reply_to',
    ]
    exclude = (
        'mailbox',
        'body',
    )

    list_select_related = True
    readonly_fields = (
            'plain_text',
        )

    def plain_text(self, obj):
        return '<pre style="display: table-cell;background-color: white;padding: ' \
               '5px;min-width: 692px;max-width: 692px;white-space: pre-wrap; ' \
               'overflow-x: scroll;" >\n{0}</pre>'.format(obj.get_text_body())

    plain_text.short_description = 'Text'
    plain_text.allow_tags = True


class NoteAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Message)
admin.site.register(Message, MessageAdmin)

admin.site.register(Lead, LeadAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Note, NoteAdmin)