__author__ = 'kasra'

import knowledge.views

from django.conf.urls import include, url

urlpatterns = [
    url(r'^source/add$', knowledge.views.showAddSource, name='add-source'),
    url(r'^knowledge/add$', knowledge.views.showAddKnowledge, name='add-knowledge'),
    url(r'^knowledge/(?P<knowledge_id>\d+)$', knowledge.views.showKnowledge, name='show-knowledge')

]
