__author__ = 'kasra'
import knowledge.models

class SearchEngine:

	@staticmethod
	def searchKnowledge(info):
		sub = info.get('subject', '')
		source_sub = info.get('source_subject', '')
		return knowledge.models.Knowledge.objects.filter(subject__icontains=sub).filter(source__subject__icontains=source_sub)

	@staticmethod
	def searchUser(info):
		name = info.get('name', '')
		username = info.get('username', '')
		return knowledge.models.Knowledge.objects.filter(user__username__icontains=username).filter(realName__icontains=name)

	@staticmethod
	def searchSource(info):
		sub = info.get('subject', '')
		return knowledge.models.Knowledge.objects.filter(subject__icontains=sub)
