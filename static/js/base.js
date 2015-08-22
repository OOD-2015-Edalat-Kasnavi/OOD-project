/**
 * Created by kasra on 5/15/2015.
 */

$('#navbar-search-form .dropdown-menu li a').each(function(id, elem){
	elem.onclick = function(event){
		$('#navbar-subject-chooser').html(elem.text + '<span class="caret"></span>');
	}
});
$('table.k-table tr').each(function(idx, elem){
	elem.onclick = function(event){
		$(elem).toggleClass('selected-row');
	}
});

/////////////////  add comment to knowledge  ///////////////////
$('.interact .comment-send-but').on('click', function(event){
	var txt = $('.interact .comment-send-text').val();
	console.log('sending comment');

	$.ajax({type:'POST',
		url: 'add-comment/',
		data: {'text':txt},
		success: function(data){
			console.log(data);
			var com = $(data['comment']);
			var comments = $('.comments');
			console.log(comments);
			console.log(com);
			comments.append(com);
		},
		error: function(data){
			console.log('sending comment failed');
		}
	});
});