from knowledge.forms import SourceForm
# from knowledge.models

from django.shortcuts import render

# Create your views here.

def addSourceView(request):
	if request.method == 'GET':
		form = SourceForm()
	if request.method == 'POST':
		form = SourceForm(request.POST)
		if form.is_valid:
			print('valid form')
		else :
			form = SourceForm()

	return render(request, 'knowledge/add-source.html', {
		'addSourceForm': form
	})