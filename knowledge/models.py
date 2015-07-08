from datetime import datetime

from django.db import models


class Knowledge(models.Model):
	subject = models.CharField(max_length=255   )
	summary = models.TextField()
	description = models.TextField()
	gainWay = models.TextField()
	access = models.IntegerField()
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