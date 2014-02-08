from django.db import models

from cms.models import CMSPlugin


from arkestra_utilities.output_libraries.dates import nice_date
from arkestra_utilities.generic_models import ArkestraGenericPluginOptions, ArkestraGenericModel
from arkestra_utilities.mixins import URLModelMixin
from arkestra_utilities.settings import PLUGIN_HEADING_LEVELS, PLUGIN_HEADING_LEVEL_DEFAULT

from contacts_and_people.models import Entity, Person #, default_entity_id

from managers import VacancyManager, StudentshipManager, LessonManager

class CommonVacancyAndStudentshipInformation(ArkestraGenericModel, URLModelMixin):
    class Meta:
        abstract = True
        ordering = ['-closing_date']

    closing_date = models.DateField()

    description = models.TextField(null=True, blank=True,
        help_text="No longer used")

    def link_to_more(self):
        return self.get_hosted_by.get_related_info_page_url("vacancies-and-studentships")

    @property
    def get_when(self):
        """
        get_when provides a human-readable attribute under which items can be grouped.
        Usually, this is an easily-readble rendering of the date (e.g. "April 2010") but it can also be "Top news", for items to be given special prominence.
        """
        try:
            # The render function of CMSNewsAndEventsPlugin can set a temporary sticky attribute for Top news items
            if self.sticky:
                return "Top news"
        except AttributeError:
            pass

        date_format = "F Y"
        get_when = nice_date(self.closing_date, date_format)
        return get_when

    @property
    def date(self):
        return self.closing_date


class Vacancy(CommonVacancyAndStudentshipInformation):
    url_path = "vacancy"

    job_number = models.CharField(max_length=9)
    salary = models.CharField(blank=True, max_length=255, null=True,
        help_text=u"Please include currency symbol")

    objects = VacancyManager()

    class Meta:
        verbose_name_plural = "Vacancies"


class Studentship(CommonVacancyAndStudentshipInformation):
    url_path = "studentship"

    supervisors = models.ManyToManyField(Person, null=True, blank=True,
        related_name="%(class)s_people")

    objects = StudentshipManager()


class Lesson(CommonVacancyAndStudentshipInformation):
    url_path = "lesson"

    teachers = models.ManyToManyField(Person, null=True, blank=True,
        related_name="%(class)s_people")

    max_students = models.IntegerField(null=True, blank=True)
    current_students = models.IntegerField(null=True, blank=True)

    objects = LessonManager()


class VacanciesPlugin(CMSPlugin, ArkestraGenericPluginOptions):
    DISPLAY = (
        (u"vacancies & studentships", u"Vacancies and studentships"),
        (u"vacancies", u"Vacancies only"),
        (u"studentships", u"Studentships only"),
        (u"lessons", u"Lessons only"),
    )
    display = models.CharField(max_length=25,choices=DISPLAY, default="vacancies & studentships")
    # entity = models.ForeignKey(Entity, null=True, blank=True,
    #     help_text="Leave blank for autoselect", related_name="%(class)s_plugin")
    vacancies_heading_text = models.CharField(max_length=25, default="Vacancies")
    studentships_heading_text = models.CharField(max_length=25, default="Studentships")
    lessons_heading_text = models.CharField(max_length=25, default="Lessons")
