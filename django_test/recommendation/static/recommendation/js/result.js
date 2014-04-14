
$(document).ready(function(){
	if (parseFloat($('#star').text())>=8.4){
		$('#star').css('color', 'rgba(206, 4, 75, 1)');
	}

	$(function ()
	{ $(".pop_over").popover({placement:'top'});
	});


	$('#next').click(function(){
		var host = window.location.host;
		var pathname = window.location.pathname;
		var query = window.location.search;
		var page = parseInt($('#page').text()) + 1;
		window.location.href = 'http://' + host + pathname + '?page=' + page;
	})

	$('#last').click(function(){
		var host = window.location.host;
		var pathname = window.location.pathname;
		var query = window.location.search;
		var page = parseInt($('#page').text()) - 1;
		window.location.href = 'http://' + host + pathname + '?page=' + page;
	})

	$('#about').click(function(){
		window.location.href = 'http://www.patrickcai.com/me';
	})

	$('#test').click(function(){
		window.location.href = 'http://www.patrickcai.com/douban_movie_recommendation';
	})

})