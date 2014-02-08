from django import forms
from django.contrib import admin, messages
from django.db.models import ForeignKey

from cms.admin.placeholderadmin import PlaceholderAdmin

from widgetry import fk_lookup
from widgetry.tabs.placeholderadmin import ModelAdminWithTabsAndCMSPlaceholder

from arkestra_utilities.widgets.wym_editor import WYMEditor
from arkestra_utilities import admin_tabs_extension
from arkestra_utilities.admin_mixins import GenericModelAdmin, GenericModelForm, HostedByFilter, fieldsets

from links.admin import ExternalLinkForm, ObjectLinkInline

from models import Vacancy, Studentship, Lesson

class VacancyStudentshipForm(GenericModelForm):
    # a shared form for vacancies & studentships
    pass

class VacancyStudentshipAdmin(GenericModelAdmin, ModelAdminWithTabsAndCMSPlaceholder):
    # inlines = (ObjectLinkInline,)
    exclude = ('description', 'url',)
    search_fields = ['short_title','title','summary', 'slug','url']
    list_display = ('short_title', 'hosted_by', 'closing_date',)
    list_display = ('short_title', 'closing_date', 'hosted_by',)
    list_filter = ('closing_date', HostedByFilter)
    related_search_fields = [
        'hosted_by',
        'please_contact',
        'external_url',
        ]
    filter_horizontal = (
        'please_contact',
        'publish_to',
        )
    prepopulated_fields = {
        'slug': ('title',)
            }

    def _media(self):
        return super(ModelAdminWithTabsAndCMSPlaceholder, self).media
    media = property(_media)


class VacancyForm(VacancyStudentshipForm):
    class Meta(VacancyStudentshipForm.Meta):
        model = Vacancy

class VacancyAdmin(VacancyStudentshipAdmin):
    # def __init__(self):
    #     super(VacancyAdmin, self).__init__(self)
    #     search_fields.append('job_number')

    form = VacancyForm
    fieldset_vacancy = ('', {'fields': ('salary', 'job_number')})

    tabs = (
            ('Basic', {'fieldsets': (fieldsets["basic"], fieldsets["host"], fieldset_vacancy, fieldsets["image"], fieldsets["publishing_control"],)}),
            ('Date & significance', {'fieldsets': (fieldsets["closing_date"], fieldsets["importance"])}),
            ('Body', {'fieldsets': (fieldsets["body"],)}),
            ('Where to Publish', {'fieldsets': (fieldsets["where_to_publish"],),}),
            ('Please contact', {'fieldsets': (fieldsets["people"],)}),
            ('Links', {'inlines': (ObjectLinkInline,),}),
            ('Advanced Options', {'fieldsets': (fieldsets["url"], fieldsets["slug"],)}),
        )


class StudentshipForm(VacancyStudentshipForm):
    class Meta(VacancyStudentshipForm.Meta):
        model = Studentship


# class StudentshipAdmin(admin_tabs_extension.ModelAdminWithTabs):
class StudentshipAdmin(VacancyStudentshipAdmin):
    form = StudentshipForm
    filter_horizontal = (
        'publish_to',
        'supervisors',
        'please_contact',
    )

    fieldset_supervision = ('', {'fields': ('supervisors',)})
    tabs = (
            ('Basic', {'fieldsets': (fieldsets["basic"], fieldsets["host"], fieldsets["image"], fieldsets["publishing_control"],)}),
            ('Date & significance', {'fieldsets': (fieldsets["closing_date"], fieldsets["importance"])}),
            ('Body', {'fieldsets': (fieldsets["body"],)}),
            ('Where to Publish', {'fieldsets': (fieldsets["where_to_publish"],),}),
            ('Supervisors', {'fieldsets': (fieldset_supervision,)}),
            ('Please contact', {'fieldsets': (fieldsets["people"],)}),
            ('Links', {'inlines': (ObjectLinkInline,),}),
            ('Advanced Options', {'fieldsets': (fieldsets["url"], fieldsets["slug"],)}),
        )

    # autocomplete fields
    related_search_fields = [
        'hosted_by',
        'please_contact',
        ]


class LessonForm(VacancyStudentshipForm):
    class Meta(VacancyStudentshipForm.Meta):
        model = Lesson


# class LessonAdmin(admin_tabs_extension.ModelAdminWithTabs):
class LessonAdmin(VacancyStudentshipAdmin):
    form = LessonForm
    filter_horizontal = (
        'teachers',
        'please_contact',
    )

    fieldset_teachers = ('', {'fields': ('teachers',)})
    tabs = (
            ('Basic', {'fieldsets': (fieldsets["basic"], fieldsets["host"], fieldsets["image"], fieldsets["publishing_control"],)}),
            ('Date & significance', {'fieldsets': (fieldsets["closing_date"], fieldsets["importance"])}),
            ('Body', {'fieldsets': (fieldsets["body"],)}),
            ('Where to Publish', {'fieldsets': (fieldsets["where_to_publish"],),}),
            ('Teachers', {'fieldsets': (fieldset_teachers,)}),
            ('Please contact', {'fieldsets': (fieldsets["people"],)}),
            ('Links', {'inlines': (ObjectLinkInline,),}),
            ('Advanced Options', {'fieldsets': (fieldsets["url"], fieldsets["slug"],)}),
        )

    # autocomplete fields
    related_search_fields = [
        'hosted_by',
        'please_contact',
        ]

admin.site.register(Vacancy,VacancyAdmin)
admin.site.register(Studentship,StudentshipAdmin)
admin.site.register(Lesson,LessonAdmin)
