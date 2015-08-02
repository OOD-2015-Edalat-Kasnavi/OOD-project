__author__ = 'kasra'

import knowledge.views

from django.conf.urls import include, url


def emptyFunc():
    pass

urlpatterns = [
    url(r'^source/add/$', knowledge.views.showAddSource, name='add-source'),
    url(r'^knowledge/add/$', knowledge.views.showAddKnowledge, name='add-knowledge'),
    url(r'^knowledge/(?P<knowledge_id>\d+)/$', knowledge.views.showKnowledge, name='show-knowledge'),
    url(r'^knowledge/(?P<knowledge_id>\d+)/add-relation/$', knowledge.views.addRelationAJ, name='add-relation-knowledge'),
    url(r'^knowledge/(?P<knowledge_id>\d+)/add-tag/$', knowledge.views.addTagAJ, name='add-tag-knowledge'),
    url(r'^knowledge/(?P<knowledge_id>\d+)/add-comment/$', knowledge.views.addCommentAJ, name='add-comment-knowledge'),

    url(r'^search/knowledge/$', knowledge.views.showSearchKnowledge, name='show-search-knowledge'),
    url(r'^search/user/$', emptyFunc, name='show-search-user'),
    url(r'^search/source/$', emptyFunc, name='show-search-source'),


    url(r'^source/(?P<source_id>\d+)/$', emptyFunc, name='show-source'),
    url(r'^relation-type/(?P<relation_id>\d+)/$', emptyFunc, name='show-relation-type'),
    url(r'^tag-type/(?P<tag_id>\d+)/$', emptyFunc, name='show-tag-type'),

]
