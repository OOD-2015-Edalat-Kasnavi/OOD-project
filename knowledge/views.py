from datetime import datetime

import users.models
import knowledge.models
import knowledge.engine
from users.views import addUserInfoContext
from knowledge.factory import KnowledgeHtmlFactory

from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.template import Template, Context, loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from knowledge.forms import SourceForm, KnowledgeForm, InterKnowledgeRelationshipForm, TagForm

# Create your views here.

@login_required()
def showAddSource(request):
	success = False
	if request.method == 'GET':
		form = SourceForm()
	if request.method == 'POST':
		form = SourceForm(request.POST)
		print('---- validating form')
		if form.is_valid():
			print('---- valid form')
			mod = form.save()
			success = True

		else :
			print('---- invalid form')
			

	return render(request, 'knowledge/add-source.html', addUserInfoContext(request, {
		'form': form,
		'success': success
	}))


@login_required()
def showAddKnowledge(request):
	user = users.models.getKnowledgeUser(request.user)
	success = False
	if request.method == 'GET':
		form = KnowledgeForm()
	if request.method == 'POST':
		form = KnowledgeForm(request.POST)
		print('---- validating form')
		if form.is_valid():
			print('---- valid form')
			mod = form.save(commit=False)
			mod.author = user
			print('---- add author to knowledge :' + str(user))
			success = True
			print(mod)
			mod.save()

		else :
			print('---- invalid form')
			

	return render(request, 'knowledge/add-knowledge.html', addUserInfoContext(request, {
		'form': form,
		'success': success
	}))


@login_required()
def showKnowledge(request, knowledge_id):
	kn = get_object_or_404(knowledge.models.Knowledge, pk=knowledge_id)
	add_relation_form = InterKnowledgeRelationshipForm()
	add_tag_form = TagForm()
	print('show knowledge:')
	print(kn)
	return render(request, 'knowledge/show-knowledge.html', addUserInfoContext(request, {
		'knowledge':kn,
		'add_relation_form': add_relation_form,
		'add_tag_form': add_tag_form
	}))


@login_required()
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
		try :
			tag.save()
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

	return JsonResponse({
		'comment': KnowledgeHtmlFactory.CommentFactory(comment),
	})


@login_required()
def showSearchKnowledge(request):
	print('search knowledge')
	if request.method == 'POST':
		raise Http404

	kns = knowledge.engine.SearchEngine.searchKnowledge(request.GET)

	return render(request, 'knowledge/search-knowledge.html', addUserInfoContext(request, {
		'knowledge': kns,

	}))






