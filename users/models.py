from datetime import datetime

from django.db import models
from django.contrib.auth.models import User, AnonymousUser


###################  User  ###################
class KUser(models.Model):
	user = models.OneToOneField(User)
	realName = models.CharField(max_length=255)
	job = models.CharField(max_length=255)
	privilege = models.IntegerField()
	employeeId = models.IntegerField(unique=True)
	isManager = models.BooleanField(default=False)
	state = models.IntegerField()

	GENDER_CHOICES = (('M', 'Male'),('F', 'Female'),)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

	

	def __str__(self):
		return ('Manager' if self.isManager else 'User') + ': ' + self.user.username




def getKnowledgeUser(usr):
	if isinstance(usr, AnonymousUser):
		return None

	if KUser.objects.filter(user__pk=usr.pk):
		return KUser.objects.get(user__pk=usr.pk)

	return None



###################  Log  ###################
class Log(models.Model):
	user = models.ForeignKey('KUser')
	detail = models.TextField()
	createDate = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return 'Log: (' + self.createDate + ') '+ self.user.username + ': ' + self.detail



###################  Request  ###################
class KRequest(models.Model):
	user = models.ForeignKey('KUser')
	state = models.IntegerField(default=0)

	def deny(self):
		pass
	def permit(self):
		pass


class SpecialPrivilegeRequest(KRequest):
	neededPrivilege = models.IntegerField()
	reason = models.TextField()

	def __str__(self):
		return 'SpecialPrivilegeRequest: ' + self.user.username + ' p:' + str(self.neededPrivilege)


class ReportAbuseRequest(KRequest):
	abusedName = models.CharField(max_length=255)
	abusedUrl = models.CharField(max_length=255)
	reason = models.TextField()

	def __str__(self):
		return 'SpecialPrivilegeRequest: ' + self.abusedName






