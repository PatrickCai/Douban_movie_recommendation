


$(document).ready(function(){

  $('#about').click(function(){
    window.location.href = 'http://www.patrickcai.com/me';
  })

  $('#test').click(function(){
    window.location.href = 'http://www.patrickcai.com/douban_movie_recommendation';
  })

  $("button").click(function(){
  	var user = $('input').val();
	 /www\.douban\.com\/people\/(\S+)\//.test(user);
  	user = RegExp.$1;
    if (user==''){
      alert('嘤嘤嘤，格式错误啦~');
      return 0;
    }
  	$.get('create',{username:user} ,function(waiting_time){
      if(waiting_time==0){
        domain = document.domain;
        if (domain=='127.0.0.1'){
          domain = domain + ':8000';
        }
        window.location.href = 'http://' + domain + '/people/' + user;
      }      
      else{
        waiting_time = parseInt(waiting_time/60);
        alert_info = '机器人正在辛苦的爬取数据中，大约' +waiting_time+'分钟后网页会自动加载结果~';
        alert_shut = '你可以先浏览其他网站，请不要关闭我TvT';
        $('#alert').text(alert_info);
        $('#alert_shutdown').text(alert_shut);
        $('#next_button').css('display', 'none')
        setInterval(function(){
          domain = document.domain;
          if (domain=='127.0.0.1'){
            domain = domain + ':8000';
          }
          window.location.href = 'http://' + domain + '/people/' + user;
        }, 1000*60*(waiting_time));
        setInterval(function(){
          waiting_time = waiting_time - 1;
          alert_info = '机器人正在辛苦的爬取数据中，大约' +waiting_time+'分钟后网页会自动加载结果~';
          $('#alert').text(alert_info);

        }, 1000*60)

      }

  	})
  });
});