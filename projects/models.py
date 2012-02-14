# hejsan: preferred order for imports: Python, Django, django CMS, other Django applications, Arkestra

from datetime import date as pythondate
from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from cms.models import CMSPlugin

from arkestra_utilities.generic_models import ArkestraGenericModel, ArkestraGenericPluginOptions
from arkestra_utilities.mixins import URLModelMixin
from arkestra_utilities.managers import ArkestraGenericModelManager
from arkestra_utilities.output_libraries.dates import nice_date

from contacts_and_people.models import Entity, Person, Building, default_entity_id

PLUGIN_HEADING_LEVELS = settings.PLUGIN_HEADING_LEVELS
PLUGIN_HEADING_LEVEL_DEFAULT = settings.PLUGIN_HEADING_LEVEL_DEFAULT
DATE_FORMAT = settings.ARKESTRA_DATE_FORMAT

class ProjectManager(ArkestraGenericModelManager):
    pass

class Project(ArkestraGenericModel, URLModelMixin):
    url_path = "projects"
    objects = ProjectManager()
    
    date = models.DateTimeField(default=datetime.now,
        help_text=_(u"Dateline for the item (the item will not be published until then"))
    sticky_until = models.DateField(_(u"Featured until"), 
        null=True, blank=True, default=pythondate.today,
        help_text=_(u"Will remain a featured item until this date"))
    is_sticky_everywhere = models.BooleanField(_(u"Featured everywhere"),
        default=False, help_text=_(u"Will be featured in other entities's project lists"))
    
    class Meta:
        ordering = ['-date']
    
    @property
    def get_when(self):
        """
        get_when provides a human-readable attribute under which items can be grouped.
        Usually, this is an easily-readble rendering of the date (e.g. "April 2010") but it can also be "Top news", for items to be given special prominence.
        """
        if getattr(self, "sticky", None):
            return "Featured project"
        get_when = nice_date(self.date, DATE_FORMAT["date_groups"])
        return get_when


class ProjectPlugin(CMSPlugin, ArkestraGenericPluginOptions):
    heading_text = models.CharField(max_length=25, default=_(u"Projects"))