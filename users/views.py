import users.models
import knowledge.models

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse as urlReverse
from django.contrib.auth import authenticate, login, logout

def loginView(request):
	if request.method == 'GET':
		return render(request, 'user/login.html', {})

	user = authenticate(username=request.POST['username'], password=request.POST['password'])
	if user is not None:
		# the password verified for the user
		if user.is_active:
			baseUrl = urlReverse('base-view')
			nextUrl = request.GET.get('next', baseUrl)
			login(request, user)
			print('---- login user: ' + str(user) + ' redirect to ' + nextUrl)

			return HttpResponseRedirect(nextUrl)

		else:
			# print("The password is valid, but the account has been disabled!")
			return render(request, 'user/login.html', {
				'invalidLogin': True,
				'errorMessage': 'Account has been deactivated.'
			})
	else:
		# the authentication system was unable to verify the username and password
		return render(request, 'user/login.html', {
			'invalidLogin': True,
			'errorMessage': 'Invalid username or password.'
		})

def logoutAj(request):
	print('logout user')
	logout(request)
	return HttpResponseRedirect(urlReverse('login'))


def addUserInfoContext(request, context):
	user = users.models.getKnowledgeUser(request.user)
	print('---- base context data for ' + str(user))
	print(user)

	context['user_realname'] = user.realName
	context['user_is_manager'] = user.isManager
	return context



@login_required()
def baseView(request):
	print('---- base view')
	
	return render(request, 'base.html', addUserInfoContext(request, {

		}) )

