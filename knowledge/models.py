from datetime import datetime
from users.models import KUser

from django.db import models


defaultAccessForKnowledge = 50

###################  knowledge  ###################
class Knowledge(models.Model):
	subject = models.CharField(max_length=255)
	source = models.ForeignKey('Source', related_name='knowledge')
	author = models.ForeignKey('users.KUser', related_name='knowledge')
	summary = models.CharField(max_length=255, blank=True, null=True)
	gainWay = models.TextField(blank=True, null=True)
	access = models.IntegerField(default=defaultAccessForKnowledge)
	createDate = models.DateTimeField(default=datetime.now)

	content = models.TextField(blank=True, null=True)
	file = models.FileField(blank=True, null=True)

	def __str__(self):
		return 'Knowledge: ' + self.subject

	def presentation(self):
		return self.subject


class Rate(models.Model):
	up = models.BooleanField(default=True)
	voter = models.ForeignKey('users.KUser', related_name='rates')
	knowledge = models.ForeignKey('Knowledge', related_name='rates')

	class Meta:
		unique_together = ['voter', 'knowledge']

	def __str__(self):
		return str(self.Knowledge) + ' vote ' + ('up' if self.up else 'down') + ' by ' + str(self.v)


###################  Source  ###################
class Source(models.Model):
	subject = models.CharField(max_length=255, unique=True)
	description = models.TextField()
	createDate = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return 'Source: ' + self.subject

	def presentation(self):
		return self.subject


class ProjectProces(Source):
	phase = models.CharField(max_length=255)
	startDate = models.DateTimeField()
	endDate = models.DateTimeField()

	def __str__(self):
		return 'ProjectProces: ' + self.phase + '.' + self.subject
		

###################  Tag  ###################
class TagType(models.Model):
	name = models.CharField(max_length=255, unique=True,error_messages={'unique':'نوع برچسب برای این مبحث موجود است.'})

	def __str__(self):
		return 'TagType: ' + self.name

	def presentation(self):
		return self.name


class Tag(models.Model):
	ktype = models.ForeignKey('TagType', related_name='tags')
	knowledge = models.ForeignKey('Knowledge', related_name='tags')

	class Meta:
		unique_together = ['ktype', 'knowledge']

	def __str__(self):
		return 'Tag: (' + self.ktype.name + ') -> ' + self.knowledge.subject



###################  Relation  ###################
class InterknowledgeRelationshipType(models.Model):
	name = models.CharField(max_length=255, unique=True,error_messages={'unique':'نوع رابطه برای این مبحث موجود است.'})

	def __str__(self):
		return 'RelationshipType: ' + self.name

	def presentation(self):
		return self.name


class InterknowledgeRelationship(models.Model):
	ktype = models.ForeignKey('InterknowledgeRelationshipType', related_name='relations')
	fromKnowledge = models.ForeignKey('Knowledge', related_name='relationToKnowledge')
	toKnowledge = models.ForeignKey('Knowledge', related_name='relationFromKnowledge')

	class Meta:
		unique_together = ['ktype', 'fromKnowledge', 'toKnowledge']

	def __str__(self):
		return 'InterknowledgeRelationship: (' +self.ktype.name + '( '\
		       + self.fromKnowledge.subject + ' -> ' + self.toKnowledge.subject + ' )'



###################  comment  ###################
class Comment(models.Model):
	author = models.ForeignKey('users.KUser', related_name='comments')
	knowledge = models.ForeignKey('Knowledge', related_name='comments')
	text = models.TextField()
	date = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return 'comment: ' + self.author.user.username + ' on ' + self.knowledge.subject


class KnowledgeUsage(models.Model):
	projectProces = models.ForeignKey('ProjectProces', related_name='usedIn')

	def __str__(self):
		return 'knowledge use: ' + self.author.user.username + ' used ' + self.knowledge.subject + ' in ' + self.projectProces.phase


###################  letter  ###################
# class Letter(models.Model):
# 	subject = models.CharField(max_length=255)
# 	sender = models.CharField(max_length=255)
# 	reciver = models.CharField(max_length=255)
# 	text = models.TextField()
# 	date = models.DateTimeField()

# 	def __str__(self):
# 		return 'letter: ' + self.subject + ' from ' + self.sender + ' to ' + self.reciver








