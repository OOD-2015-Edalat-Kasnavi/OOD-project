__author__ = 'kasra'

import knowledge.views

from django.conf.urls import include, url


def emptyFunc():
    pass

urlpatterns = [
    url(r'^source/add/$', knowledge.views.showAddSource, name='add-source'),
    url(r'^knowledge/add/$', knowledge.views.showAddKnowledge, name='add-knowledge'),
    url(r'^tag-type/add/$', knowledge.views.showAddRelationType, name='add-tag-type'),
    url(r'^relation-type/add/$', knowledge.views.showAddRelationType, name='add-relation-type'),
    url(r'^tag/remove/$', knowledge.views.removeTagAj, name='remove-tag'),
    url(r'^relation/remove/$', knowledge.views.removeRelationAj, name='remove-relation'),
    url(r'^knowledge/(?P<knowledge_id>\d+)/$', knowledge.views.showKnowledge, name='show-knowledge'),
    url(r'^knowledge/(?P<knowledge_id>\d+)/add-relation/$', knowledge.views.addRelationAJ, name='add-relation-knowledge'),
    url(r'^knowledge/(?P<knowledge_id>\d+)/add-tag/$', knowledge.views.addTagAJ, name='add-tag-knowledge'),
    url(r'^knowledge/(?P<knowledge_id>\d+)/add-comment/$', knowledge.views.addCommentAJ, name='add-comment-knowledge'),
    url(r'^source/(?P<source_id>\d+)/$', knowledge.views.showSource, name='show-source'),

    url(r'^search/knowledge/$', knowledge.views.showSearchKnowledge, name='show-search-knowledge'),
    url(r'^search/source/$', knowledge.views.showSearchSource, name='show-search-source'),
    url(r'^report-abuse/$', knowledge.views.reportAbuseAj, name='report-abuse'),


    url(r'^relation-type/(?P<relation_id>\d+)/$', emptyFunc, name='show-relation-type'),
    url(r'^tag-type/(?P<tag_id>\d+)/$', emptyFunc, name='show-tag-type'),

]
