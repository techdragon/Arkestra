from django.utils.translation import ugettext_lazy as _
from django.db import models
from datetime import date as pythondate
from datetime import datetime
from arkestra_utilities.generic_models import ArkestraGenericModel
from arkestra_utilities.mixins import URLModelMixin

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
