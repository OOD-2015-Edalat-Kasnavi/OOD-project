__author__ = 'kasra'

import knowledge.models

from django.forms import ModelForm


class SourceForm(ModelForm):
	class Meta:
		model = knowledge.models.Source
		fields = ['subject', 'description']


