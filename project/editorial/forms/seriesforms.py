"""Forms for Series and related entities.

"""

import datetime
from bootstrap3_datetime.widgets import DateTimePicker
from .customwidgets import OurDateTimePicker, ArrayFieldSelectMultiple
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.forms import Textarea, TextInput, RadioSelect, Select, NumberInput, CheckboxInput, CheckboxSelectMultiple, FileField
from django.contrib.postgres.fields import ArrayField
from datetimewidget.widgets import DateTimeWidget
from tinymce.widgets import TinyMCE
# from django.contrib.staticfiles.templatetags.staticfiles import static


from editorial.models import (
    Series,
)


# ------------------------------ #
#          Series Forms          #
# ------------------------------ #

class SeriesForm(forms.ModelForm):
    """ Form to create a new series. """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SeriesForm, self).__init__(*args, **kwargs)
        self.fields['collaborate_with'].queryset = Organization.get_org_collaborators_vocab(self.request.user.organization)
        self.fields['team'].queryset = Organization.get_org_users(self.request.user.organization)

    class Meta:
        model = Series
        fields = ['name', 'series_description', 'collaborate', 'collaborate_with', 'team']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Series Name'}),
            'series_description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'team': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'series-team', 'data-placeholder': 'Select Series Team'}),
            'collaborate': CheckboxInput(attrs={'class': 'c-indicator c-indicator-default'}),
            'collaborate_with': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'collaborate-with', 'data-placeholder': 'Select Collaborators'}),
            }

    class Media:
        css = {
            'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')
        }
        js = ('scripts/chosen.jquery.min.js',)