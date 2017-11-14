from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField
# from simple_history.models import HistoricalRecords
from model_utils.models import TimeStampedModel
import time as timemk
from datetime import datetime, timedelta, time
from imagekit.models import ProcessedImageField, ImageSpecField
# from pilkit.processors import ResizeToFit, SmartResize
# from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
# from itertools import chain
# from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
# from django.db.models.signals import post_save
# from django.dispatch import receiver

from . import User, Organization, Network, Project, Series, Story

#-----------------------------------------------------------------------#
#   Notes:
#   Note, NetworkNote, OrganizationNote, UserNote, SeriesNote, StoryNote
#-----------------------------------------------------------------------#


@python_2_unicode_compatible
class Note(models.Model):
    """ Abstract base class for notes."""

    title = models.CharField(
        max_length=255,
    )

    text = models.TextField(
        help_text='Content of the note',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the note was created.'
    )

    important = models.BooleanField(
        default=False,
        help_text='Mark as important for pinning to top of notes',
        blank=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for note search.',
        blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    @property
    def description(self):
        return "Keywords: {keywords}".format(keywords = self.keywords)

    @property
    def search_title(self):
        return self.title


class NetworkNote(Note):
    """ General purpose notes for a network."""

    owner=models.ForeignKey(
        User,
        related_name='networknote_owner'
    )

    network=models.ForeignKey(
        Network,
        related_name='networknote_network'
    )

    def get_absolute_url(self):
        return reverse('network_detail', kwargs={'pk': self.network.id})

    @property
    def type(self):
        return "Network Note"


class OrganizationNote(Note):
    """ General purpose notes for an organization."""

    owner=models.ForeignKey(
        User,
        related_name='organizationnote_owner'
    )

    organization=models.ForeignKey(
        Organization,
        related_name="orgnote_org"
    )

    def get_absolute_url(self):
        return reverse('org_detail', kwargs={'pk': self.organization.id})

    @property
    def type(self):
        return "Organization Note"


class UserNote(Note):
    """ General purpose notes from a user. """

    owner = models.ForeignKey(
        User,
        related_name='usernote_owner'
    )

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.owner.id})

    @property
    def type(self):
        return "User Note"


class ProjectNote(Note):
    """ General purpose notes for a project."""

    owner=models.ForeignKey(
        User,
        related_name='projectnote_owner'
    )

    organization=models.ForeignKey(
        Organization,
        related_name="projectnote_org"
    )

    project = models.ForeignKey(
        Project,
        related_name="projectnote",
    )

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.project.id})

    @property
    def type(self):
        return "Project Note"


class SeriesNote(Note):
    """ A note attached to a series."""

    owner = models.ForeignKey(
        User,
        related_name='seriesnote_owner'
    )

    organization=models.ForeignKey(
        Organization,
        related_name="seriesnote_org"
    )

    series = models.ForeignKey(
        Series,
        related_name="seriesnote",
    )

    def get_absolute_url(self):
        return reverse('series_detail', kwargs={'pk': self.series.id})

    def __str__(self):
        return "SeriesNote: {seriesnote} for Series: {series}".format(
                                seriesnote=self.id,
                                series=self.series.id,
                                )

    @property
    def type(self):
        return "Series Note"


class StoryNote(Note):
    """ Planning notes and conversation for a story. """

    owner = models.ForeignKey(
        User,
        related_name='storynote_owner'
    )

    organization=models.ForeignKey(
        Organization,
        related_name="storynote_org"
    )

    story = models.ForeignKey(
        Story,
    )

    def __str__(self):
        return "StoryNote: {storynote} for Story: {story}".format(
                                storynote=self.id,
                                story=self.story.id,
                                )

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.story.id})

    @property
    def type(self):
        return "Story Note"