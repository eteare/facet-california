import datetime

from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.forms import Textarea, TextInput, RadioSelect

from editorial.models import User, Organization, Network, Story


class CreateOrganization(forms.ModelForm):
    """ Create an Organization. """

    class Meta:
        model = Organization
        fields = ['name', 'org_description']
        

class EditUserProfile(forms.ModelForm):
    """ Handle a user completing their profile."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'credit_name', 'title', 'phone', 'bio',
                 'expertise', 'facebook', 'twitter', 'linkedin', 'instagram', 'snapchat', 'vine',]


class SeriesForm(form.ModelForm):
    """" Form to create a new series. """

    class Meta:
        model = Series
        fields = []


class StoryForm(forms.ModelForm):
    """ Form to create a new story. """
    
    class Meta:
        model = Story
        fields = ['name', 'story_description']


