__author__ = 'kasra'

import knowledge.models

from django import forms


def convertFormErrorToFarsi(form):
	for field in form.fields.values():
		field.error_messages = {'required':('پر کردن ' + '"{fieldname}"' + ' ضروری است.').
		format(fieldname=field.label),
		'invalid':('اطلاعات ' + '"{fieldname}"' + ' صحیح نیست.').format(fieldname=field.label),
		}


class SourceForm(forms.ModelForm):
	class Meta:
		model = knowledge.models.Source
		fields = ['subject', 'description']
		labels = {
			'subject': 'موضوع',
			'description': 'شرح'
		}

	def __init__(self, *args, **kwargs):
		super(SourceForm, self).__init__(*args, **kwargs)
		convertFormErrorToFarsi(self)




class InterKnowledgeRelationshipForm(forms.ModelForm):
	class Meta:
		model = knowledge.models.InterknowledgeRelationship
		fields = ['ktype', 'fromKnowledge', 'toKnowledge']
		labels = {
			'ktype': 'نوع',
			'fromKnowledge': 'از',
			'toKnowledge': 'به'
		}

	def __init__(self, *args, **kwargs):
		super(InterKnowledgeRelationshipForm, self).__init__(*args, **kwargs)
		convertFormErrorToFarsi(self)



class TagForm(forms.ModelForm):
	class Meta:
		model = knowledge.models.Tag
		fields = ['ktype']
		labels = {
			'ktype': 'نوع',
		}

	def __init__(self, *args, **kwargs):
		super(TagForm, self).__init__(*args, **kwargs)
		convertFormErrorToFarsi(self)


class KnowledgeForm(forms.ModelForm):
	class Meta:
		model = knowledge.models.Knowledge
		fields = ['subject', 'source', 'content', 'summary', 'gainWay', 'access', 'file']
		exclude = ['author']
		labels = {
			'subject': 'موضوع',
			'source': 'منبع',
			'content': 'محتوا',
			'summary':'خلاصه',
			'gainWay':'طریقه ی کسب',
			'access':'دسترسی',
			'file':'فایل',
		}

	def __init__(self, *args, **kwargs):
		super(KnowledgeForm, self).__init__(*args, **kwargs)
		convertFormErrorToFarsi(self)



class RelationTypeForm(forms.ModelForm):
	class Meta:
		model = knowledge.models.InterknowledgeRelationshipType
		fields = ['name']
		labels = {
			'name': 'مبحث',
		}

	def __init__(self, *args, **kwargs):
		super(RelationTypeForm, self).__init__(*args, **kwargs)
		convertFormErrorToFarsi(self)

class TagTypeForm(forms.ModelForm):
	class Meta:
		model = knowledge.models.TagType
		fields = ['name']
		labels = {
			'name': 'مبحث',
		}

	def __init__(self, *args, **kwargs):
		super(TagTypeForm, self).__init__(*args, **kwargs)
		convertFormErrorToFarsi(self)

