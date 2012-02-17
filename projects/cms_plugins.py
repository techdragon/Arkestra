from django import forms
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from arkestra_utilities.generic_models import ArkestraGenericPlugin
from arkestra_utilities.generic_models import ArkestraGenericPluginForm
from arkestra_utilities.mixins import AutocompleteMixin

from contacts_and_people.templatetags.entity_tags import work_out_entity

from models import Project, ProjectPlugin

from menu import menu_dict


class ProjectPluginForm(ArkestraGenericPluginForm, forms.ModelForm):
    class Meta:
        model = ProjectPlugin


class CMSProjectPlugin(ArkestraGenericPlugin, AutocompleteMixin, CMSPluginBase):
    model = ProjectPlugin
    name = _("Projects")
    form = ProjectPluginForm
    menu_cues = menu_dict
    fieldsets = (
        (None, {
        'fields': (('list_format',),  ( 'format', 'order_by', 'group_dates',), 'limit_to')
    }),
        ('Advanced options', {
        'classes': ('collapse',),
        'fields': ('entity', 'heading_level', 'heading_text', ),
    }),
    )

    # autocomplete fields
    related_search_fields = ['entity',]
    
    # hejsan: this is the really important bit    
    def get_items(self, instance):
        self.lists = []

        this_list = {"model": Project,}
        this_list["items"] = Project.objects.get_items(instance)
        this_list["links_to_other_items"] = self.projects_other_links
        print "**", this_list["links_to_other_items"] 
        this_list["heading_text"] = instance.heading_text
        this_list["item_template"] = "arkestra/universal_plugin_list_item.html"
        # the following should *also* check this_list["links_to_other_items"] - 
        # but then get_items() will need to call self.add_links_to_other_items() itself
        # this will then mean that news and events pages show two columns if one has links to other items
        if this_list["items"]: 
            self.lists.append(this_list)

    def projects_other_links(self, instance, this_list):
        this_list["other_items"] = []
        if this_list["items"] and instance.view == "current":
            all_items_count = len(this_list["items"])
            if instance.limit_to and all_items_count > instance.limit_to:
                this_list["other_items"] = [{
                    "link":instance.entity.get_related_info_page_url("projects-archive"), 
                    "title":"Projects archive",
                    "count": all_items_count,}]
            return this_list

    def icon_src(self, instance):
        return "/static/plugin_icons/projects.png"

plugin_pool.register_plugin(CMSProjectPlugin)
