/**
 * Created by kasra on 5/15/2015.
 */

$('#navbar-search-form .dropdown-menu li a').each(function(id, elem){
	elem.onclick = function(event){
		$('#navbar-subject-chooser').html(elem.text + '<span class="caret"></span>');
	}
});
$('table.table-select tr').each(function(idx, elem){
	elem.onclick = function(event){
		$(elem).toggleClass('selected-row');
	}
});