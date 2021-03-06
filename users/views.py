import sys
import json
from itertools import chain

import users.models
import knowledge.models
import knowledge.engine
from users import kuser_auth
from users.models import Log, getRequestKUser
from users.forms import KUserForm, SpecialPrivilegeForm, ChangePassForm

from django.template import Template, Context, loader
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
			Log.log_action(request, "ورود به سامانه")
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
	context['kauth_access_add_tag'] = user.privilege >= kuser_auth.access_add_tag
	context['kauth_access_add_relation'] = user.privilege >= kuser_auth.access_add_relation
	return context



@login_required()
def baseView(request):
	print('---- base view')
	
	return render(request, 'base.html', addUserInfoContext(request, {
		'page_title': 'دانش گستر',

		}) )


@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_show_user)
def userProfileView(request, user_id):
	usr = get_object_or_404(users.models.KUser, pk=user_id)
	print('show user profile')

	return render(request, 'user/show-user-profile.html', addUserInfoContext(request, {
		'page_title': usr.realName,
		'kuser': usr,
	}))


@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_search_user)
def searchUser(request):
	print('search user')
	if request.method == 'POST':
		raise Http404

	kusers = knowledge.engine.SearchEngine.searchUser(request.GET)
	Log.log_action(request, "جستجوی کاربران")

	return render(request, 'user/search-user.html', addUserInfoContext(request, {
		'page_title': 'Search user',
		'kusers': kusers,
	}))


@login_required()
@kuser_auth.manager_only_decorator
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
				Log.log_action(request,'کاربر جدید ساخنه شد.')
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
@kuser_auth.manager_only_decorator
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
		man = getRequestKUser(request)
		for kuser in kusers:
			if kuser.privilege > man.privilege:
				print('insufficient access')
				return JsonResponse({'message': '<div class="form-error">دسترسی مجاز نیست.</div>', 'success': False})
		for kuser in kusers:
			kuser.fire()
			Log.log_action(request,'کاربر ' + kuser.user.username + ' اخراج شد.')
		return JsonResponse({'message': success_mes, 'success': True})

	return None



@login_required()
@kuser_auth.manager_only_decorator
def showReportUserActivity(request):
	print('report user activity')
	if request.method == 'GET':
		kusers = users.models.KUser.objects.all()
		print('send page for get method')
		return render(request, 'user/show-report-user-activity.html', addUserInfoContext(request, {
			'page_title': 'report user activity',
			'kusers': kusers,
		}))

	elif request.method == 'POST':
		logs = knowledge.engine.ReportEngine.reportUserActivity(request.POST)
		Log.log_action(request, 'درخواست گزارش فعالیت کارمندان')
		context = {
			'logs': logs,
		}
		t = loader.get_template('user/report-user-activity-result.html')
		resp = t.render(context)

		return JsonResponse({'result': resp, 'success': True})

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
			kuser = users.models.getKnowledgeUser(request.user)
			mod.user = kuser
			mod.url = urlReverse('show-user-profile', kwargs={'user_id': kuser.id})
			mod.save()
			success = True
			Log.log_action(request,'درخواست دسترسی ویژه ثبت شد.')

		else :
			print('---- invalid form')

	return render(request, 'user/show-special-privilage-request.html', addUserInfoContext(request, {
		'page_title': 'Special privilege request',
		'form': form,
		'success': success
	}))




@login_required()
@kuser_auth.manager_only_decorator
def showRequestManager(request):
	message = ''
	if request.method == 'GET':
		pass
	if request.method == 'POST':
		ids = json.loads(request.POST['ids'])
		print(ids)
		decide_reqs = users.models.KRequest.objects.filter(pk__in=ids)
		print(decide_reqs)
		for req in decide_reqs:
			if request.POST['action'] == 'reject':
				req.deny()
			else:
				req.permit()
		message = 'درخواست ها با موفقیت ' + ('رد ' if request.POST['action'] == 'reject' else 'پذیرفته ') + 'شدند.'

	krequests = list(chain(users.models.SpecialPrivilegeRequest.objects.filter(state=0), users.models.ReportAbuseRequest.objects.filter(state=0)))


	return render(request, 'user/show-request-manager.html', addUserInfoContext(request, {
		'page_title': 'Request manager',
		'requests': krequests,
		'message': message,
	}))


@login_required()
def showChangePass(request):
	success = False
	if request.method == 'GET':
		form = ChangePassForm()
	if request.method == 'POST':
		form = ChangePassForm(request.POST, username=request.user.username)
		print('---- validating form')
		if form.is_valid():
			kuser = users.models.getKnowledgeUser(request.user)
			kuser.changePassword(form.cleaned_data['pass1'])
			success = True
		else :
			print('---- invalid form')


	return render(request, 'user/show-change-password.html', addUserInfoContext(request, {
		'page_title': 'Change Password',
		'form': form,
		'success': success
	}))

