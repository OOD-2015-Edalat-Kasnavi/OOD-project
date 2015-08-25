from datetime import datetime
import users.models

from django.db import models



def knowledge_file_name(instance, filename):
	return '/'.join(['file', instance.author.user.username, filename])

###################  knowledge  ###################
class Knowledge(models.Model):
	subject = models.CharField(max_length=255)
	source = models.ForeignKey('Source', related_name='knowledge')
	author = models.ForeignKey('users.KUser', related_name='knowledge')
	summary = models.CharField(max_length=255, blank=True, null=True)
	gainWay = models.TextField(blank=True, null=True)
	access = models.IntegerField(default=0)
	createDate = models.DateTimeField(default=datetime.now)

	content = models.TextField(blank=True, null=True)
	file = models.FileField(blank=True, null=True, upload_to=knowledge_file_name)

	def __str__(self):
		return 'Knowledge: ' + self.subject

	def presentation(self):
		return self.subject

	def rate(self, kuser, vote):
		try:
			rate = Rate.objects.get(knowledge=self, voter=kuser)
		except:
			rate = Rate()
			rate.knowledge = self
			rate.voter = kuser
		rate.up = vote
		rate.save()

	@staticmethod
	def kdelete(id):
		print('remove knowledge :' + repr(id))
		Knowledge.objects.filter(pk=id).delete()


class Rate(models.Model):
	up = models.BooleanField(default=True)
	voter = models.ForeignKey('users.KUser', related_name='rates')
	knowledge = models.ForeignKey('Knowledge', related_name='rates')

	class Meta:
		unique_together = ['voter', 'knowledge']

	def __str__(self):
		return str(self.knowledge) + ' vote ' + ('up' if self.up else 'down') + ' by ' + str(self.voter)


###################  Source  ###################
class Source(models.Model):
	subject = models.CharField(max_length=255, unique=True)
	description = models.TextField()
	createDate = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return self.subject

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

	def abuse_presentation(self):
		return 'برچسب: ' + self.ktype.name + '-' + self.knowledge.subject

	@staticmethod
	def kdelete(id):
		print('remove tag :' + repr(id))
		Tag.objects.filter(pk=id).delete()



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

	def abuse_presentation(self):
		return 'رابطه: ' + self.ktype.name + ' از ' + self.fromKnowledge.subject + ' به ' + self.toKnowledge.subject

	@staticmethod
	def kdelete(id):
		print('remove relation :' + repr(id))
		InterknowledgeRelationship.objects.filter(pk=id).delete()



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








