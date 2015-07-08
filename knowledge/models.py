from datetime import datetime
from users.models import KUser

from django.db import models


defaultAccessForKnowledge = 50

class Knowledge(models.Model):
	subject = models.CharField(max_length=255)
	source = models.ForeignKey('Source')
	author = models.ForeignKey('users.KUser')
	summary = models.CharField(max_length=255, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	gainWay = models.TextField(blank=True, null=True)
	access = models.IntegerField(default=defaultAccessForKnowledge)
	createDate = models.DateTimeField(default=datetime.now)


class TextKnowledge(Knowledge):
	content = models.TextField()

	def __str__(self):
		return 'TextKnowledge: ' + self.subject


class FileKnowledge(Knowledge):
	file = models.FileField()

	def __str__(self):
		return 'FileKnowledge: ' + self.subject


class Source(models.Model):
	subject = models.CharField(max_length=255)
	description = models.TextField()
	createDate = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return 'Source: ' + self.subject