$(document).ready(function(){
    let user_noneaction_time = 0;
    $('html').mousemove(function(event){
        user_noneaction_time = 0;
    });
    $('html').click(function(event){
        user_noneaction_time = 0;
    });
    $('html').keyup(function(event){
        user_noneaction_time = 0;
    });
    setInterval(function() {
        user_noneaction_time += 10;
        if (user_noneaction_time == 600) { // 10분 가만히 놔두면
            location.reload();                  //새로고침
        }
    }, 10000);
});