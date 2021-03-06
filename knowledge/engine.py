__author__ = 'kasra'
import json

import users.models
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
		return users.models.KUser.objects.filter(user__username__icontains=username).filter(realName__icontains=name)

	@staticmethod
	def searchSource(info):
		sub = info.get('subject', '')
		return knowledge.models.Source.objects.filter(subject__icontains=sub)


class ReportEngine():

	@staticmethod
	def reportUserActivity(info):
		ids = json.loads(info['ids'])
		print('ids:')
		print(ids)
		logs = users.models.Log.objects.filter(user__pk__in=ids)
		print(logs)
		return logs