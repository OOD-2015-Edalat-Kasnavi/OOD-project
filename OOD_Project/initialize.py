__author__ = 'kasra'
import users.models
from django.contrib.auth.models import User

def initialize():
	try:
		print('check admin')
		if User.objects.filter(username='admin').count() == 0:
			print('create admin')
			usr = User.objects.create_superuser('admin', '', 'admin')
			kuser = users.models.KUser()
			kuser.user = usr
			kuser.realName = 'admin'
			kuser.job = 'admin'
			kuser.privilege = 100
			kuser.employeeId = 0
			kuser.isManager = True
			kuser.gender = 'M'
			print(kuser)
			kuser.save()
	except:
		pass
