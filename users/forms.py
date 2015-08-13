__author__ = 'kasra'

import users.models
from knowledge.forms import convertFormErrorToFarsi

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class KUserForm(forms.ModelForm):

	# user = models.OneToOneField(User) mail,username,pass1,pass2,
	# state = models.IntegerField()
	email = forms.EmailField(label="میل")
	username = forms.RegexField(label="نام کاربری", max_length=30, regex=r'^[\w.@+-]+$', error_messages={'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
	pass1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
	pass2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput)

	def clean_pass2(self):
		data = self.cleaned_data['pass2']
		if data != self.cleaned_data['pass1']:
			raise forms.ValidationError('رمز عبور تطابق ندارد.', 'not matched')
		return data

	def clean_username(self):
		data = self.cleaned_data['username']
		if User.objects.filter(username=self.cleaned_data['username']).count() :
			raise forms.ValidationError('نام کاربری موجود است. لطفا نام دیگری انتخاب کنید.', 'duplicate')
		return data

	class Meta:
		model = users.models.KUser
		fields = ['realName', 'job', 'privilege', 'employeeId', 'isManager', 'gender']
		labels = {
			'realName': 'نام',
			'job': 'شغل',
			'privilege': 'سطح دسترسی',
			'employeeId': 'شماره ی کارمندی',
			'isManager': 'رتبه',
			'gender': 'جنسیت'
		}

	def __init__(self, *args, **kwargs):
		super(KUserForm, self).__init__(*args, **kwargs)
		convertFormErrorToFarsi(self)

	def save(self, commit=True):
		"""
			this method always save django user
		"""
		print('save django.user ')
		print(self.cleaned_data)
		usr = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['pass1'])
		kuser = users.models.KUser()
		kuser.user = usr
		kuser.realName = self.cleaned_data['realName']
		kuser.job = self.cleaned_data['job']
		kuser.privilege = self.cleaned_data['privilege']
		kuser.employeeId = self.cleaned_data['employeeId']
		kuser.isManager = self.cleaned_data['isManager']
		kuser.gender = self.cleaned_data['gender']
		print('create kuser:')
		print(kuser)

		if commit:
			kuser.save()
		return kuser



class SpecialPrivilegeForm(forms.ModelForm):
	class Meta:
		model = users.models.SpecialPrivilegeRequest
		fields = ['neededPrivilege', 'reason']
		labels = {
			'neededPrivilege': 'دسترسی مورد نیاز',
			'reason': 'دلیل',
		}

	def __init__(self, *args, **kwargs):
		super(SpecialPrivilegeForm, self).__init__(*args, **kwargs)
		convertFormErrorToFarsi(self)


class ChangePassForm(forms.Form):
	old_pass = forms.CharField(label='رمز عبور قدیمی', widget=forms.PasswordInput)
	pass1 = forms.CharField(label='رمز عبور جدید', widget=forms.PasswordInput)
	pass2 = forms.CharField(label='تکرار رمز عبور جدید', widget=forms.PasswordInput)

	def clean_pass2(self):
		data = self.cleaned_data['pass2']
		if data != self.cleaned_data['pass1']:
			raise forms.ValidationError('رمز عبور تطابق ندارد.', 'not matched')
		return data

	def clean_old_pass(self):
		data = self.cleaned_data['old_pass']
		if not authenticate(username=self.username, password=data):
			raise forms.ValidationError('رمز عبور اشتباه است.', 'wrong-pass')
		return data

	def __init__(self, *args, **kwargs):
		self.username = kwargs.pop('username', None)
		print('add username to change pass: ' + str(self.username))
		super(ChangePassForm, self).__init__(*args, **kwargs)
		convertFormErrorToFarsi(self)


