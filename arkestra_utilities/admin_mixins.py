from django.db.models import ForeignKey
from django.conf import settings
from django import forms
from django.template.loader import select_template
from django.contrib.contenttypes.models import ContentType
from django.forms.models import ModelFormMetaclass

from cms.utils import cms_static_url

from widgetry import fk_lookup
from widgetry.tabs.placeholderadmin import ModelAdminWithTabsAndCMSPlaceholder

from contacts_and_people.models import Entity
from links.models import ExternalLink
    
class AutocompleteMixin(object):
    class Media:
        js = [
            cms_static_url('js/libs/jquery.ui.core.js'),
        ]
        css = {
            'all': ('/static/jquery/themes/base/ui.all.css',)
        }    

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Overrides the default widget for Foreignkey fields if they are
        specified in the related_search_fields class attribute.
        """
        if (isinstance(db_field, ForeignKey) and 
                db_field.name in self.related_search_fields):
            kwargs['widget'] = fk_lookup.FkLookup(db_field.rel.to)          
        return super(AutocompleteMixin, self).formfield_for_dbfield(db_field, **kwargs)


class SupplyRequestMixin(object):
    def get_form(self, request, obj=None, **kwargs):
        form_class = super(SupplyRequestMixin, self).get_form(request, obj, **kwargs)
        form_class.request = request
        return form_class


class GenericModelAdmin(AutocompleteMixin, SupplyRequestMixin, ModelAdminWithTabsAndCMSPlaceholder):

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "publish_to": 
            kwargs["queryset"] = Entity.objects.filter(website__published = True)
        return super(AutocompleteMixin, self).formfield_for_manytomany(db_field, request, **kwargs)

    change_form_template = "admin/generic_change_form.html"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        This is complex. Here we find out from ModelAdminWithTabsAndCMSPlaceholder.change_form_template what templates it's looking for, and get select_template to choose the first. When we got to admin/generic_change_form.html, we pass it "admin_template" so it knows which to extend.
        """ 
        extra_context = extra_context or {}
        extra_context["admin_template"] = select_template(super(ModelAdminWithTabsAndCMSPlaceholder, self).change_form_template)
        extra_context['external_link_model_id'] = ContentType.objects.get_for_model(ExternalLink).id
        return super(GenericModelAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


class InputURLMixin(forms.ModelForm): 
    # really this is simply acting as a base admin form for various models
    # but not just GenericModels (e.g. Person, Entity too)
    input_url = forms.CharField(max_length=255, required = False,
        help_text=u"<strong>External URL</strong> not found above? Enter a new one.", 
        )



fieldsets = {
    'basic': ('', {'fields': ('title',  'short_title', 'summary')}),
    'host': ('', {'fields': ('hosted_by',)}),
    'image': ('', {'fields': ('image',)}),
    'body':  ('', {
        'fields': ('body',),
        'classes': ('plugin-holder', 'plugin-holder-nopage',)
        }),
    'where_to_publish': ('', {'fields': ('publish_to',)}),
    'people': ('People to contact about this item', {'fields': ('please_contact',)}),
    'publishing_control': ('Publishing control', {'fields': ('published', 'in_lists')}),
    'date': ('', {'fields': ('date',)}),
    'closing_date': ('', {'fields': ('closing_date',)}),
    'importance': ('', {'fields': ('importance',)}),
    'url': ('If this is an external item', {'fields': ('external_url', 'input_url',)}),         
    'slug': ('If this is an internal item', {'fields': ('slug',)}),
    'location': ('', {'fields': ('precise_location', 'access_note',)}),
    'address_report': ('', {'fields': ('address_report',)}),
    'email': ('', {'fields': ('email',)}),
    }