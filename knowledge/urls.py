__author__ = 'kasra'

import knowledge.views

from django.conf.urls import include, url

urlpatterns = [
    url(r'^source/add$', knowledge.views.addSourceView, name='add-source'),
    url(r'^knowledge/add$', knowledge.views.addKnowledgeView, name='add-knowledge')

]
