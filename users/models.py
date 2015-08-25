from datetime import datetime

import knowledge.models

from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate


###################  User  ###################
class KUser(models.Model):
	user = models.OneToOneField(User)
	realName = models.CharField(max_length=255)
	job = models.CharField(max_length=255)
	privilege = models.IntegerField()
	# django doesn't support unique error message in forms
	employeeId = models.IntegerField(unique=True, error_messages={'unique':"شماره ی کارمندی تکراریست."})
	isManager = models.BooleanField(choices=((False, 'کاربر'), (True, 'مدیر')), default=False)

	STATE_CHOICES = ((0, 'فعال'),(1, 'غیر فعال'),(2, 'اخراج شده'),)
	state = models.SmallIntegerField(default=0, choices=STATE_CHOICES)

	GENDER_CHOICES = (('M', 'Male'),('F', 'Female'),)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

	def presentation(self):
		return self.user.username

	def __str__(self):
		return ('Manager' if self.isManager else 'User') + ': ' + self.user.username

	def changeJob(self, newJob):
		self.job = newJob
		self.save()

	def fire(self):
		print('dismiss user: ' + self.presentation())
		self.state = 2
		self.user.is_active = False
		self.user.is_staff = False
		self.user.is_superuser = False
		self.user.save()
		self.save()

	def emailPassword(self):
		pass

	def changePassword(self, newPass):
		print('change user pass')
		self.user.set_password(newPass)
		self.user.save()

	def checkPass(self, password):
		user = authenticate(username=self.username, password=password)
		if user is not None:
			return True
		return False




def getKnowledgeUser(usr):
	if isinstance(usr, AnonymousUser):
		return None
	if KUser.objects.filter(user__pk=usr.pk):
		return KUser.objects.get(user__pk=usr.pk)
	return None

def getRequestKUser(request):
	return getKnowledgeUser(request.user)


###################  Log  ###################
class Log(models.Model):
	user = models.ForeignKey('KUser')
	detail = models.TextField()
	createDate = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return 'Log: (' + str(self.createDate) + ') ' + self.user.user.username + ': ' + self.detail

	@staticmethod
	def log_action(request, action):
		usr = getRequestKUser(request)
		log = Log()
		log.user = usr
		log.detail = action
		log.save()

###################  Request  ###################
class KRequest(models.Model):
	user = models.ForeignKey('KUser')
	STATE_CHOICES = ((0, 'برسسی نشده'),(1, 'پذیرفته شده'),(2, 'رد شده'),)
	state = models.IntegerField(default=0, choices=STATE_CHOICES)
	reason = models.TextField(blank=True, null=True)
	url = models.CharField(max_length=255)


	def getReason(self):
		return self.reason if self.reason else 'دلیل ذکر نشده است.'

	def polymorphism(self):
		if SpecialPrivilegeRequest.objects.filter(pk=self.id).count():
			return SpecialPrivilegeRequest.objects.get(pk=self.id)
		return ReportAbuseRequest.objects.get(pk=self.id)

	def presentation(self):
		print("## parent polymorphisem:")
		return self.polymorphism().presentation()

	def deny(self):
		print("## parent polymorphisem:")
		return self.polymorphism().deny()
	def permit(self):
		print("## parent polymorphisem:")
		return self.polymorphism().permit()


class SpecialPrivilegeRequest(KRequest):
	neededPrivilege = models.IntegerField()

	def __str__(self):
		return 'SpecialPrivilegeRequest: ' + self.user.user.username + ' privilege:' + str(self.neededPrivilege)
	def presentation(self):
		return 'افزایش دسترسی به ' + str(self.neededPrivilege)

	def deny(self):
		self.state = 2
		print("---- SpecialPrivilegeRequest deny:")
		self.save()

	def permit(self):
		self.state = 1
		self.user.privilege = self.neededPrivilege
		self.user.save()
		print("---- SpecialPrivilegeRequest permit:")
		self.save()



class ReportAbuseRequest(KRequest):
	abusedName = models.CharField(max_length=255)
	REF_CHOICES = ((0, 'knowledge'),(1, 'tag'),(2, 'relation'),)
	ref = models.SmallIntegerField(choices=REF_CHOICES)
	remove_id = models.IntegerField()

	def __str__(self):
		return 'ReportAbuseRequest: ' + self.abusedName
	def presentation(self):
		return 'استفاده نادرست از' + self.abusedName

	def deny(self):
		self.state = 2
		print("---- ReportAbuseRequest deny:")
		self.save()

	def permit(self):
		self.state = 1
		if self.ref == 0:
			knowledge.models.Knowledge.kdelete(self.remove_id)
		if self.ref == 1:
			knowledge.models.Tag.kdelete(self.remove_id)
		if self.ref == 2:
			knowledge.models.InterknowledgeRelationship.kdelete(self.remove_id)
		print("---- ReportAbuseRequest permit:")
		self.save()






