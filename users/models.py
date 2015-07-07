from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(DjangoUser):
	realName = models.CharField(max_length=255)
	job = models.CharField(max_length=255)
	sex = models.BooleanField()
	privilege = models.IntegerField()
	employeeId = models.IntegerField()
	state = models.IntegerField()

	def __str__(self):
		return 'User: ' + self.username



class Manager(User):
	class Meta:
		verbose_name = 'Manager'
		verbose_name_plural = 'Managers'

	def __str__(self):
		return 'Manager: ' + self.username
