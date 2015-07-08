import users.models
import knowledge.models

from users.views import addBaseViewContext
from knowledge.forms import SourceForm, KnowledgeForm

from django.shortcuts import render

# Create your views here.

def addSourceView(request):
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
			

	return render(request, 'knowledge/add-source.html', addBaseViewContext(request, {
		'form': form,
		'success': success
	}))


def addKnowledgeView(request):
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
			print('---- add author to knowledgeow:' + str(user))
			success = True
			print(mod)
			mod.save()

		else :
			print('---- invalid form')
			

	return render(request, 'knowledge/add-knowledge.html', addBaseViewContext(request, {
		'form': form,
		'success': success
	}))