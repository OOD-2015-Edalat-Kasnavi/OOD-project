import users.models
import knowledge.models

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from  django.core.urlresolvers import reverse as urlReverse
from django.contrib.auth.decorators import login_required

def loginView(request):
	if request.method == 'GET':
		return render(request, 'login.html', {})

	user = authenticate(username=request.POST['username'], password=request.POST['password'])
	if user is not None:
		# the password verified for the user
		if user.is_active:
			baseUrl = urlReverse('base-view')
			nextUrl = request.GET.get('next', baseUrl)
			print('login user: ' + str(user) + ' redirect to ' + nextUrl)
			return HttpResponseRedirect( nextUrl)

		else:
			# print("The password is valid, but the account has been disabled!")
			return render(request, 'login.html', {
				'invalidLogin': True,
				'errorMessage': 'Account has been deactivated.'
			})
	else:
		# the authentication system was unable to verify the username and password
		return render(request, 'login.html', {
			'invalidLogin': True,
			'errorMessage': 'Invalid username or password.'
		})


# @login_required()
def baseView(request):
	print('show base for :')
	userType = ''
	if type(request.user) is users.models.User:
		userType = 'user'
	if type(request.user) is users.models.Manager:
		userType = 'manager'
	return render(request, userType+'-base.html', {
	})

