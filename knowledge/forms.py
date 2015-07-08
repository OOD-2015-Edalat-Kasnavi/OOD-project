__author__ = 'kasra'

import knowledge.models

from django.forms import ModelForm

def convertFormErrorToFarsi(form):
	for field in form.fields.values():
		field.error_messages = {'required':('پر کردن ' + '{fieldname}' + ' ضروری است.').
		format(fieldname=field.label),
		'invalid':('اطلاعات ' + '{fieldname}' + 'صحیح نیست.').format(fieldname=field.label),
		}


class SourceForm(ModelForm):
	class Meta:
		model = knowledge.models.Source
		fields = ['subject', 'description']
		labels = {
			'subject': 'موضوع',
			'description': 'شرح'
		}

	def __init__(self, *args, **kwargs):
		super(SourceForm, self).__init__(*args, **kwargs)

		# if you want to do it to all of them
		convertFormErrorToFarsi(self)



class KnowledgeForm(ModelForm):
	class Meta:
		model = knowledge.models.Knowledge
		fields = ['subject', 'source', 'description', 'summary', 'gainWay', 'access']
		exclude = ['author']
		labels = {
			'subject': 'موضوع',
			'source': 'منبع',
			'description': 'شرح',
			'summary':'خلاصه',
			'gainWay':'طریقه ی کسب',
			'access':'دسترسی'
		}

	def __init__(self, *args, **kwargs):
		super(KnowledgeForm, self).__init__(*args, **kwargs)
		# if you want to do it to all of them
		convertFormErrorToFarsi(self)


