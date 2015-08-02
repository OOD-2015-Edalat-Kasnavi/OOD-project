__author__ = 'kasra'

import knowledge.views

from django.conf.urls import include, url

urlpatterns = [
    url(r'^source/add/$', knowledge.views.showAddSource, name='add-source'),
    url(r'^knowledge/add/$', knowledge.views.showAddKnowledge, name='add-knowledge'),
    url(r'^knowledge/(?P<knowledge_id>\d+)/$', knowledge.views.showKnowledge, name='show-knowledge'),
    url(r'^knowledge/(?P<knowledge_id>\d+)/add-relation/$', knowledge.views.addRelationAJ, name='add-relation-knowledge'),
    url(r'^knowledge/(?P<knowledge_id>\d+)/add-tag/$', knowledge.views.addTagAJ, name='add-tag-knowledge'),
    url(r'^knowledge/(?P<knowledge_id>\d+)/add-comment/$', knowledge.views.addCommentAJ, name='add-comment-knowledge'),

]
