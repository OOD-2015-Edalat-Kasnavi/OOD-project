from datetime import datetime

import users.models
import knowledge.models
import knowledge.engine
from users import kuser_auth
from users.models import Log
from users.views import addUserInfoContext
from knowledge.factory import KnowledgeHtmlFactory

from django.template.loader import render_to_string
from django.template import Template, Context, loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse as urlReverse
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from knowledge.forms import SourceForm, KnowledgeForm, InterKnowledgeRelationshipForm, TagForm, RelationTypeForm, TagTypeForm




@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_add_knowledge)
def showAddKnowledge(request):
	user = users.models.getKnowledgeUser(request.user)
	success = False
	if request.method == 'GET':
		form = KnowledgeForm()
	if request.method == 'POST':
		form = KnowledgeForm(request.POST, request.FILES)
		print('---- validating form')
		if form.is_valid():
			print(request.FILES)
			print(request.POST)
			print('---- valid form')
			kn = form.save(commit=False)
			kn.author = user
			if kn.access > user.privilege:
				return HttpResponseForbidden('access denied.')
			print('---- add author to knowledge :' + str(user))
			success = True

			kn.save()
			Log.log_action(request, 'دانش ' + kn.subject + ' ساخته شد.')

		else :
			print('---- invalid form')


	return render(request, 'knowledge/add-knowledge.html', addUserInfoContext(request, {
		'page_title': 'Add knowledge',
		'form': form,
		'success': success,
		'action': 'افزودن',
	}))


@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_add_knowledge)
def showEditKnowledge(request, knowledge_id):
	user = users.models.getKnowledgeUser(request.user)
	kn = get_object_or_404(knowledge.models.Knowledge, pk=knowledge_id)
	if user != kn.author:
		return HttpResponseForbidden('access denied.')

	success = False
	if request.method == 'GET':
		form = KnowledgeForm(instance=kn)
	if request.method == 'POST':
		form = KnowledgeForm(request.POST, request.FILES, instance=kn)
		print('---- validating form')
		if form.is_valid():
			print(request.FILES)
			print(request.POST)
			print('---- valid form')
			kn = form.save()
			print('---- edit knowledge :' + str(kn))
			success = True

			Log.log_action(request, 'دانش ' + kn.subject + ' ویرایش شد.')

		else :
			print('---- invalid form')


	return render(request, 'knowledge/add-knowledge.html', addUserInfoContext(request, {
		'page_title': 'edit knowledge',
		'form': form,
		'success': success,
		'action': 'ویرایش',
	}))

@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_add_source)
def showAddSource(request):
	success = False
	if request.method == 'GET':
		form = SourceForm()
	if request.method == 'POST':
		form = SourceForm(request.POST)
		print('---- validating form')
		if form.is_valid():
			print('---- valid form')
			sc = form.save()
			success = True
			Log.log_action(request, 'منبع ' + sc.subject + ' ساخنه شد.')

		else :
			print('---- invalid form')

	return render(request, 'knowledge/add-source.html', addUserInfoContext(request, {
		'page_title': 'Add source',
		'form': form,
		'success': success
	}))



@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_show_knowledge)
def showKnowledge(request, knowledge_id):
	user = users.models.getKnowledgeUser(request.user)
	kn = get_object_or_404(knowledge.models.Knowledge, pk=knowledge_id)

	if user.privilege < kn.access:
		return HttpResponseForbidden('access denied.')

	rate_up = knowledge.models.Rate.objects.filter(knowledge=kn, up=True).count()
	rate_down = knowledge.models.Rate.objects.filter(knowledge=kn, up=False).count()
	user_rate = ''
	try:
		rt = knowledge.models.Rate.objects.get(knowledge=kn, voter=user)
		if rt and rt.up:
			user_rate = 'up'
		else:
			user_rate = 'down'
	except:
		pass

	print('show knowledge:')
	print(kn)
	Log.log_action(request, 'دانش ' + kn.subject + ' مشاهده شد.')
	return render(request, 'knowledge/show-knowledge.html', addUserInfoContext(request, {
		'page_title': kn.subject,
		'knowledge': kn,
		'add_relation_form': InterKnowledgeRelationshipForm(),
		'add_tag_form': TagForm(),
		'rate_up': rate_up,
		'rate_down': rate_down,
		'user_rate': user_rate,
	}))



@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_show_knowledge)
def rateKnowledgeAJ(request, knowledge_id):
	user = users.models.getKnowledgeUser(request.user)
	kn = get_object_or_404(knowledge.models.Knowledge, pk=knowledge_id)

	if user.privilege < kn.access:
		return HttpResponseForbidden('access denied.')

	try:
		rate = knowledge.models.Rate.objects.get(knowledge=kn, voter=user)
	except:
		rate = knowledge.models.Rate()
		rate.knowledge = kn
		rate.voter = user
	vote = request.GET['vote']
	rate.up = (vote == 'up')
	rate.save()

	print('rate:')
	print(rate)
	Log.log_action(request, 'به دانش ' + kn.subject + ' رتبه داده شد.')


	return HttpResponseRedirect(urlReverse('show-knowledge', kwargs={'knowledge_id': kn.id}))


@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_show_source)
def showSource(request, source_id):
	src = get_object_or_404(knowledge.models.Source, pk=source_id)
	print('show source: ')
	print(src)
	Log.log_action(request, 'منبع ' + src.subject + ' مشاهده شد.')
	return render(request, 'knowledge/show-source.html', addUserInfoContext(request, {
		'page_title': src.subject,
		'source': src,
	}))


@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_add_relation)
def addRelationAJ(request, knowledge_id):
	print('add relationship AJ')
	if request.method == 'GET':
		raise Http404
	kn = get_object_or_404(knowledge.models.Knowledge, pk=knowledge_id)
	add_relation_form = InterKnowledgeRelationshipForm(request.POST)

	relation = None
	success = False
	print('---- validating form')

	if add_relation_form.is_valid():
		print('---- valid form')
		relation = add_relation_form.save()
		Log.log_action(request,'رابطه ' + relation.presentation() + ' ساخته شد.')
		success = True
	else :
		print('---- invalid form')

	context = {
		'knowledge': kn,
		'success': success,
		'add_relation_form': add_relation_form
	}

	t = loader.get_template('knowledge/util/add-relation.html')
	resp = t.render(context)
	but = KnowledgeHtmlFactory.RelationButtonFactory(relation, kn) if success else ''

	return JsonResponse({
		'form': resp,
		'button': but
	})



@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_add_tag)
def addTagAJ(request, knowledge_id):
	print('add tag AJ')
	if request.method == 'GET':
		raise Http404
	kn = get_object_or_404(knowledge.models.Knowledge, pk=knowledge_id)
	add_tag_form = TagForm(request.POST)
	print(kn)

	tag = None
	success = False
	print('---- validating form')
	if add_tag_form.is_valid():
		print('---- valid form')
		tag = add_tag_form.save(commit=False)
		tag.knowledge = kn
		try:
			tag.save()
			Log.log_action(request, '' + tag.abuse_presentation() + ' ساخته شد.')
			success = True
		except:
			success = False
			add_tag_form.add_error(None, 'تگ مورد نظر موجود هست.')
			add_tag_form.is_valid()
	else :
		print('---- invalid form')

	context = {
		'knowledge': kn,
		'success': success,
		'add_tag_form': add_tag_form
	}

	t = loader.get_template('knowledge/util/add-tag.html')
	resp = t.render(context)
	but = KnowledgeHtmlFactory.TagButtonFactory(tag) if success else ''

	return JsonResponse({
		'form': resp,
		'button': but
	})



@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_comment)
def addCommentAJ(request, knowledge_id):
	print('add comment AJ')
	if request.method == 'GET':
		raise Http404
	kn = get_object_or_404(knowledge.models.Knowledge, pk=knowledge_id)

	user = users.models.getKnowledgeUser(request.user)
	txt = request.POST['text']
	time = datetime.now()

	# print('add comment user:'+str(user) + ' text:"' +txt + '" time:' + str(time))

	comment = knowledge.models.Comment()
	comment.knowledge = kn
	comment.author = user
	comment.text = txt
	comment.date = time
	comment.save()

	Log.log_action(request,'ببه دانش ' + kn.subject + ' نظر داده شد.')

	return JsonResponse({
		'comment': KnowledgeHtmlFactory.CommentFactory(comment),
	})


@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_search_knowledge)
def showSearchKnowledge(request):
	print('search knowledge')
	if request.method == 'POST':
		raise Http404

	kns = knowledge.engine.SearchEngine.searchKnowledge(request.GET)

	return render(request, 'knowledge/search-knowledge.html', addUserInfoContext(request, {
		'page_title': 'Search knowledge',
		'knowledge': kns,

	}))


@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_search_source)
def showSearchSource(request):
	print('search source')
	if request.method == 'POST':
		raise Http404

	sources = knowledge.engine.SearchEngine.searchSource(request.GET)

	return render(request, 'knowledge/search-source.html', addUserInfoContext(request, {
		'page_title': 'Search source',
		'sources': sources,
	}))



@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_add_relation_type)
@kuser_auth.manager_only_decorator
def showAddRelationType(request):
	success = False
	if request.method == 'GET':
		form = RelationTypeForm()
	if request.method == 'POST':
		form = RelationTypeForm(request.POST)
		print('---- validating form')
		if form.is_valid():
			print('---- valid form')
			rel = form.save()
			success = True
			Log.log_action(request,'نوع رابطه ی ' + rel.abuse_presentation() + ' ساخته شد.')
		else :
			print('---- invalid form')

	return render(request, 'knowledge/add-relation-type.html', addUserInfoContext(request, {
		'page_title': 'Add Relation type',
		'form': form,
		'success': success
	}))



@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_add_tag_type)
def showAddTagType(request):
	success = False
	if request.method == 'GET':
		form = TagTypeForm()
	if request.method == 'POST':
		form = TagTypeForm(request.POST)
		print('---- validating form')
		if form.is_valid():
			print('---- valid form')
			tag = form.save()
			success = True
			Log.log_action(request,'نوع برچسب ' + tag.abuse_presentation() + ' ساخته شد.')
		else :
			print('---- invalid form')

	return render(request, 'knowledge/add-tag-type.html', addUserInfoContext(request, {
		'page_title': 'Add Tag type',
		'form': form,
		'success': success
	}))




@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_report_abuse)
def reportAbuseAj(request):
	print('report abuse')
	if request.method == 'GET':
		raise Http404
	if request.method == 'POST':
		url = request.POST.dict().get('url')
		pres = request.POST.dict().get('name')
		reason = request.POST.dict().get('reason')
		remove_id = request.POST.dict().get('remove_id')
		remove_type = request.POST.dict().get('type')
		print(request.POST.dict())
		# print('abuse reported  name: ' + pres + ' url: ' + url + ' rem_id:' + str(remove_id) + ' t' + str(type(remove_id)) + ' rem_type:' + str(remove_type) + ' t' + str(type(remove_type)))
		print('abuse reported  name: ' + pres + ' url: ' + url)
		print(' rem_id:' + str(remove_id) )
		print(' t' + str(type(remove_id)))
		print(' rem_type:' + str(remove_type))

		if (not pres) or (not url):
			return HttpResponseForbidden('invalid request')
		abuse = users.models.ReportAbuseRequest()
		abuse.user = users.models.getKnowledgeUser(request.user)
		abuse.ref = remove_type
		abuse.remove_id = remove_id
		abuse.abusedName = pres
		abuse.url = url
		abuse.reason = reason
		abuse.save()
		Log.log_action(request,'درخواست استفاده نادرست ثبت شد.')
		print('abuse reported')
		print(abuse)
		return HttpResponse(' درخواست با موفقیت ثبت شد.')
	return None



@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_remove_tag)
@kuser_auth.manager_only_decorator
def removeTagAj(request):
	if request.method == 'GET':
		raise Http404
	if request.method == 'POST':
		id = request.POST.dict().get('id')
		print('remove tag id: ' + id)

		knowledge.models.Tag.objects.filter(pk=id).delete()

		Log.log_action(request,'برچسب حذف شد.')
		return HttpResponse('حذف با موفقیت انجام شد.')
	return None


@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_remove_relation)
@kuser_auth.manager_only_decorator
def removeRelationAj(request):
	if request.method == 'GET':
		raise Http404
	if request.method == 'POST':
		id = request.POST.dict().get('id')
		print('remove tag id: ' + id)

		knowledge.models.InterknowledgeRelationship.objects.filter(pk=id).delete()
		Log.log_action(request,'رابطه حذف شد.')
		return HttpResponse('حذف با موفقیت انجام شد.')
	return None



@login_required()
@kuser_auth.check_privilege_decorator(kuser_auth.access_remove_knowledge)
@kuser_auth.manager_only_decorator
def removeKnowledgeAj(request):
	if request.method == 'GET':
		raise Http404
	if request.method == 'POST':
		id = request.POST.dict().get('id')
		print('remove knowledge id: ' + id)

		knowledge.models.Knowledge.objects.filter(pk=id).delete()
		Log.log_action(request,'دانش حذف شد.')
		return HttpResponse('حذف با موفقیت انجام شد.')
	return None

