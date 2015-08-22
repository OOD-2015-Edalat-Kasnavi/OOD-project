__author__ = 'kasra'
from users.models import getRequestKUser
from django.http import HttpResponseForbidden

access_show_knowledge = 10
access_show_source = 15
access_show_user = 20
access_add_knowledge = 20
access_add_source = 30
access_add_tag = 30
access_add_relation = 40
access_add_tag_type = 40
access_add_relation_type = 60
access_comment = 15
access_rate = 15
access_search_user = 40
access_search_knowledge = 15
access_search_source = 20
access_report_abuse = 30
access_remove_tag = 50
access_remove_relation = 60
access_remove_knowledge = 80

def manager_only_decorator(view_func):
	def _wrapped_view_func(request, *args, **kwargs):
		if not getRequestKUser(request).isManager:
			return HttpResponseForbidden('access denied.')
		return view_func(request, *args, **kwargs)
	return _wrapped_view_func


def check_privilege_decorator(access):
	def _decorator(view_func):
		def _wrapped_view_func(request, *args, **kwargs):
			if getRequestKUser(request).privilege < access:
				return HttpResponseForbidden('access denied.')
			return view_func(request, *args, **kwargs)
		return _wrapped_view_func
	return _decorator