from __future__ import unicode_literals
from codemirror.widgets import CodeMirrorTextarea
from django.contrib import admin
import re
from agencies.models import RegexRule, Agency, Agent, EmailTemplate, LeadSource, Notification, SpecialOfferTemplate, ConciergeTemplate, SecondEmailTemplate
from django.db import models
from fetchmyguest.utils.parse_email import match_rule

codemirror = CodeMirrorTextarea(mode="htmlmixed",
                                dependencies=("xml", "javascript", "css"),
                                theme="cobalt",
                                config={ 'fixedGutter': True, 'lineNumbers': True})

class SourceInline(admin.TabularInline):
    model = LeadSource
    extra = 0

class RegexRuleInline(admin.TabularInline):
    model = RegexRule
    extra = 1
    fields = [
        'source',
        'matching_group_name',
        'field',
        'target_field',
        'regex',
        'example_text',
        'matches',
    ]
    readonly_fields = ('matches',)

    def matches(self, obj):
        result = ''
        if obj.example_text and obj.regex:
            try:
                regex = re.compile(obj.regex)
                m = regex.search(obj.example_text)
                if m:
                    result = m.group(obj.matching_group_name)
            except Exception as e:
                result = repr(e)
        return result

class TemplateInline(admin.TabularInline):
    model = EmailTemplate
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': codemirror},
    }

class SecondEmailTemplateInline(admin.TabularInline):
    model = SecondEmailTemplate
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': codemirror},
    }

class SpecialOfferTemplateInline(admin.TabularInline):
    model = SpecialOfferTemplate
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': codemirror},
    }

class ConciergeTemplateInline(admin.TabularInline):
    model = ConciergeTemplate
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': codemirror},
    }


class LeadSourceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'agency',
        'active',
        'priority'
    ]
    list_filter = ['agency']
    inlines = [RegexRuleInline,]
    save_as = True

class RegexRuleAdmin(admin.ModelAdmin):
    list_display = [
        'source',
        'matching_group_name',
        'field',
        'target_field',
        'regex',

    ]
    list_filter = ['source']




class AgentInline(admin.StackedInline):
    model = Agent
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': codemirror},
    }

class AgencyAdmin(admin.ModelAdmin):
    inlines = [AgentInline, TemplateInline, SecondEmailTemplateInline, SpecialOfferTemplateInline, ConciergeTemplateInline, ]


class AgentAdmin(admin.ModelAdmin):
    pass

class NotificationAdmin(admin.ModelAdmin):
    pass

class EmailTemplateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Agency, AgencyAdmin)
admin.site.register(LeadSource, LeadSourceAdmin)
admin.site.register(RegexRule, RegexRuleAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(Notification, NotificationAdmin)
