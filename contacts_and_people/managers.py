import logging

#app = contacts_and_people
from django.db import models
from django.db.utils import DatabaseError
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch

from cms.models import Page, CMSPlugin
from cms.models.fields import PlaceholderField

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from filer.fields.image import FilerImageField

from arkestra_utilities.mixins import URLModelMixin
from arkestra_utilities.settings import MULTIPLE_ENTITY_MODE, ARKESTRA_BASE_ENTITY, DEFAULT_NEWS_PAGE_TITLE, DEFAULT_CONTACTS_PAGE_TITLE, DEFAULT_VACANCIES_PAGE_TITLE, DEFAULT_PUBLICATIONS_PAGE_TITLE
from links.models import ExternalLink

import news_and_events

class BuildingManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class EntityManager(TreeManager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

    def base_entity(self):
        try:
            # are Entities available at all?
            list(Entity.objects.all())
            # print "** Entity objects are available from the database"
        except:
            # no - the database isn't ready
            # print "** Entity objects are not available from the database"
            pass
        else:
            # we managed to get Entity.objects.all()
            # we don't use default_entity (or default_entity_id) in MULTIPLE_ENTITY_MODE
            try:
                # print "trying"
                entity = Entity.objects.get(id = base_entity_id)
            # it can't be found, maybe because of a misconfiguation or because we haven't added any Entities yet
            except (Entity.DoesNotExist, DatabaseError), e:
                # print "** Either the Entity does not exist, or I got a DatabaseError:"
                # print "**", e
                pass
            else:
                # print "** I successfully found a default entity:", entity
                return entity

    def default_entity_id(self):
        if self.base_entity and not MULTIPLE_ENTITY_MODE:
            return base_entity_id


class PersonManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

