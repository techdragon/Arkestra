from django.utils.translation import ugettext_lazy as _
from django.db import models
from datetime import date as pythondate
from datetime import datetime
from arkestra_utilities.generic_models import ArkestraGenericModel
from arkestra_utilities.mixins import URLModelMixin
from cms.models import CMSPlugin
from contacts_and_people.models import Entity, Person, Building, default_entity_id

class Project(ArkestraGenericModel, URLModelMixin):
    url_path = "projects"
    # objects = NewsArticleManager()
    
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

from django.conf import settings
PLUGIN_HEADING_LEVELS = settings.PLUGIN_HEADING_LEVELS
PLUGIN_HEADING_LEVEL_DEFAULT = settings.PLUGIN_HEADING_LEVEL_DEFAULT
class ProjectPlugin(CMSPlugin):
    heading_text = models.CharField(max_length=25, default=_(u"News"))
    entity = models.ForeignKey(Entity, null=True, blank=True, 
        help_text="Leave blank for autoselect", 
        related_name="%(class)s_plugin")
    FORMATS = (
        ("title", u"Title only"),
        ("details image", u"Details"),
        )
    format = models.CharField("Item format", max_length=25,choices = FORMATS, default = "details image")    
    heading_level = models.PositiveSmallIntegerField(choices = PLUGIN_HEADING_LEVELS, default = PLUGIN_HEADING_LEVEL_DEFAULT)
    ORDERING = (
        ("date", u"Date alone"),
        ("importance/date", u"Importance & date"),
        )
    order_by = models.CharField(max_length = 25, choices=ORDERING, default="importance/date")
    LIST_FORMATS = (
        ("vertical", u"Vertical"),
        ("horizontal", u"Horizontal"),
        )
    list_format = models.CharField("List format", max_length = 25, choices=LIST_FORMATS, default="vertical")
    # group_dates = models.BooleanField("Show date groups", default = True)
    limit_to = models.PositiveSmallIntegerField("Maximum number of items", default = 5, null = True, blank = True, 
        help_text = u"Leave blank for no limit")

    def sub_heading_level(self): # requires that we change 0 to None in the database
        if self.heading_level == None: # this means the user has chosen "No heading"
            return 6 # we need to give sub_heading_level a value
        else:
            return self.heading_level + 1 # so if headings are h3, sub-headings are h4
