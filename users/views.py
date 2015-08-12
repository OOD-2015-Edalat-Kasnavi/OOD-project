import sys
import json

import users.models
import knowledge.models
import knowledge.engine
from users.forms import KUserForm, SpecialPrivilegeForm

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse as urlReverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404, JsonResponse

def loginView(request):
	if request.method == 'GET':
		return render(request, 'user/login.html', {
			'page_title': '»Login',
		})

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
				'page_title': 'Login',
				'invalidLogin': True,
				'errorMessage': 'Account has been deactivated.'
			})
	else:
		# the authentication system was unable to verify the username and password
		return render(request, 'user/login.html', {
			'page_title': 'Login',
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
		'page_title': 'دانش گستر',

		}) )


@login_required()
def userProfileView(request, user_id):
	usr = get_object_or_404(users.models.KUser, pk=user_id)
	print('show user profile')

	return render(request, 'user/show-user-profile.html', addUserInfoContext(request, {
		'page_title': usr.realName,
		'kuser': usr,
	}))


@login_required()
def searchUser(request):
	print('search user')
	if request.method == 'POST':
		raise Http404

	kusers = knowledge.engine.SearchEngine.searchUser(request.GET)

	return render(request, 'user/search-user.html', addUserInfoContext(request, {
		'page_title': 'Search user',
		'kusers': kusers,
	}))


@login_required()
def showRegisterKUser(request):
	success = False
	if request.method == 'GET':
		form = KUserForm()
	if request.method == 'POST':
		form = KUserForm(request.POST)
		print('---- validating form')
		if form.is_valid():
			print('---- valid form')
			try:
				print('register user for')
				form.save()
				print('form saved')
				success = True
			except :
				print("Unexpected error:", sys.exc_info()[0])
				success = False

		else :
			print('---- invalid form')


	return render(request, 'user/register.html', addUserInfoContext(request, {
		'page_title': 'Register',
		'form': form,
		'success': success
	}))


@login_required()
def showDismissKUser(request):
	print('dismiss users')
	if request.method == 'GET':
		kusers = users.models.KUser.objects.all()
		print('send page for get method')
		return render(request, 'user/show-dismiss-user.html', addUserInfoContext(request, {
			'page_title': 'Dismiss',
			'kusers': kusers,
		}))

	elif request.method == 'POST':
		success_mes = '<div class="form-success">کاربران اخراج شدند.</div>'
		print(request.POST)
		ids = json.loads(request.POST['ids'])
		print('ids:')
		print(ids)
		print(type(ids))
		kusers = users.models.KUser.objects.filter(pk__in=ids)
		print(kusers)
		for kuser in kusers:
			kuser.fire()
		return JsonResponse({'message': success_mes, 'success': True})

	return None


@login_required()
def showSpecialprivilageRequest(request):
	success = False
	if request.method == 'GET':
		form = SpecialPrivilegeForm()
	if request.method == 'POST':
		form = SpecialPrivilegeForm(request.POST)
		print('---- validating form')
		if form.is_valid():
			print('---- valid form')
			mod = form.save(commit=False)
			mod.user = users.models.getKnowledgeUser(request.user)
			mod.save()
			success = True

		else :
			print('---- invalid form')

	return render(request, 'user/show-special-privilage-request.html', addUserInfoContext(request, {
		'page_title': 'Add source',
		'form': form,
		'success': success
	}))


