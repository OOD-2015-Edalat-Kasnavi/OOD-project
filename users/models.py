from datetime import datetime

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
		self.user.set_password(newPass)

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






