from django.core.urlresolvers import reverse

class KnowledgeHtmlFactory(object):
	"""factory for html elements in knowledge"""

	@staticmethod
	def TagButtonFactory(tag):
		print('build tag for:' + str(tag))
		if tag is None:
			return ''

		return "<div class='btn-group'>"+"<a class='btn btn-info'>" + tag.ktype.presentation() +"</a'>"+"<a class='btn btn-info'><span class='glyphicon glyphicon-remove' aria-hidden='true'></span></a>"+"</div>"


	@staticmethod
	def RelationButtonFactory(relation, kn):
		print('build relation for:' + str(relation))
		if relation is None:
			return ''
		btn_type = ''
		other_kn = None
		if relation.fromKnowledge == kn:
			btn_type = 'btn-success'
			other_kn = relation.toKnowledge
		elif relation.toKnowledge == kn:
			btn_type = 'btn-warning'
			other_kn = relation.fromKnowledge
		else:
			return ''

		return "<div class='btn-group'>"+"<a class='btn btn-sm "+btn_type+"'> "+other_kn.presentation()+" </a>"+"<a class='btn btn-sm "+btn_type+"'>"+ relation.ktype.presentation() +"</a>"+"<a class='btn btn-sm "+btn_type+"'><span class='glyphicon glyphicon-remove' aria-hidden='true'></span></a>"+"</div>"

	@staticmethod
	def CommentFactory(comment):
		print('build comment ' + str(comment))
		if comment is None:
			return ''

		return '<div class="comment" dir="rtl"><a href="" class="comment-author" dir="rtl">'+comment.author.user.username+':</a>'\
		       +'<span class="comment-text"  dir="rtl">'+comment.text+'</span></div>'