from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q

from . import SimpleImage, SimpleDocument, SimpleAudio, SimpleVideo
from . import User, Organization, Project, Series, Story


#-----------------------------------------------------------------------#
#  TASK
#-----------------------------------------------------------------------#

class Task(models.Model):
    """A Task.

    A task is an action item assigned to a project, series,
    story or an event. A task has an assigned team of users.
    """

    organization = models.ForeignKey(
        Organization,
    )

    owner = models.ForeignKey(
      User,
      related_name='taskowner'
    )

    name = models.TextField(
        help_text='Name of the task.'
    )

    text = models.TextField(
        help_text='Content of the task.',
        blank=True,
    )

    assigned_to = models.ManyToManyField(
        # There can be multiple users listed as assigned to the task.
        User,
        related_name='taskassigneduser',
        help_text='The users assigned to the task.',
        blank=True,
    )

    # Choices for Task status.
    IDENTIFIED = 'Identified'
    IN_PROGRESS = 'In Progress'
    COMPLETE = 'Complete'
    TASK_STATUS_CHOICES = (
        (IDENTIFIED, 'Identified'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETE, 'Complete'),
    )

    status = models.CharField(
        max_length=50,
        choices=TASK_STATUS_CHOICES,
        help_text='Task status.'
    )

    important = models.BooleanField(
        default=False,
        help_text='Whether a task is important.'
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time task is created.',
        blank=True,
    )

    due_date = models.DateTimeField(
        help_text='Date and time task is to be completed.',
        blank=True,
    )

    inprogress_date = models.DateTimeField(
        help_text='Date and time task status is changed to in progress.',
        blank=True,
        null=True,
    )

    completion_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time task status is changed to complete.',
        blank=True,
        null=True,
    )

    # a task can be associated with a project, series, story or an event.
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    discussion = models.ForeignKey(
        'Discussion',
        help_text='Id of discussion for the task.',
        blank=True,
        null=True,
    )

    notes = models.ManyToManyField(
        'Note',
        blank=True,
    )

    # assets
    simple_image_assets = models.ManyToManyField(
        SimpleImage,
        blank=True,
    )

    simple_document_assets = models.ManyToManyField(
        SimpleDocument,
        blank=True,
    )

    simple_audio_assets = models.ManyToManyField(
        SimpleAudio,
        blank=True,
    )

    simple_video_assets = models.ManyToManyField(
        SimpleVideo,
        blank=True,
    )

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = "Tasks"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'pk': self.id})

    def get_task_assignment_vocab(self):
        """Return queryset with org users and users from collaborating orgs for the parent
        of the task. Used in selecting assigned users for a task.
        """

        from . import User
        # TODO future: add contractors

        if self.project:
            parent = self.project
        elif self.series:
            parent = self.series
        elif self.story:
            parent = self.story
        else:
            parent = self.event

        if parent.type == "project" or "series" or "story":
            collaborators = parent.collaborate_with.all()
            owner = parent.organization
            task_vocab = User.objects.filter(Q(Q(organization=self.organization) | Q(organization__in=collaborators) | Q(organization=owner)))
        else:
            task_vocab = self.organization.get_org_users()

        return task_vocab

    @property
    def search_title(self):
        return self.name

    @property
    def description(self):
        return self.text.encode('utf-8')

    @property
    def type(self):
        return "Task"

    def clean(self):
        """Enforce that there is one relationship."""

        super(Task, self).clean()

        count = (
            (1 if self.project else 0) +
            (1 if self.series else 0) +
            (1 if self.story else 0) +
            (1 if self.event else 0)
        )

        if count != 1:
            raise ValidationError("Tasks can only relate to one thing.")
