import users.models
import knowledge.models

from users.views import addUserInfoContext
from knowledge.forms import SourceForm, KnowledgeForm

from django.shortcuts import render, get_object_or_404

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
	print('show knowledge:')
	print(kn)
	return render(request, 'knowledge/show-knowledge.html', addUserInfoContext(request, {
		'knowledge':kn
	}))