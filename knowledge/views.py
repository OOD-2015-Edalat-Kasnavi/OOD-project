import users.models
import knowledge.models
from users.views import addUserInfoContext

from django.http import Http404
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from knowledge.forms import SourceForm, KnowledgeForm, InterKnowledgeRelationshipForm

# Create your views here.

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


def showKnowledge(request, knowledge_id):
	kn = get_object_or_404(knowledge.models.Knowledge, pk=knowledge_id)
	add_relation_form = InterKnowledgeRelationshipForm()
	print('show knowledge:')
	print(kn)
	return render(request, 'knowledge/show-knowledge.html', addUserInfoContext(request, {
		'knowledge':kn,
		'add_relation_response': False,
		'add_relation_form': add_relation_form
	}))


def addRelationAJ(request, knowledge_id):
	print('add relationship AJ')
	if request.method == 'GET':
		raise Http404
	kn = get_object_or_404(knowledge.models.Knowledge, pk=knowledge_id)
	add_relation_form = InterKnowledgeRelationshipForm(request.POST)

	success = False
	print('---- validating form')
	if add_relation_form.is_valid():
		print('---- valid form')
		add_relation_form.save()
		success = True
	else :
		print('---- invalid form')

	return render(request, 'knowledge/show-knowledge.html', addUserInfoContext(request, {
		'knowledge':kn,
		'success': success,
		'add_relation_response' : True,
		'add_relation_form': add_relation_form
	}))



