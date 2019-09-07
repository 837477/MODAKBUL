let vote_list_for_search;
//modal 관련 변수
var is_votemodal_open = 0;
var is_votemodal_fixed_open = 0;
var now_postmodal_top = 0;
var is_image_modal_open = 0;
//미디어쿼리 폰트 크기
let label_font_size_media = 20;
if (window.innerWidth < 450){
    label_font_size_media = 10;
}

//시간 보여주는 함수
function printClock() {   
    var clock = document.getElementById("M_statistics_time_js");            // 출력할 장소 선택
    var currentDate = new Date();                                     // 현재시간
    var calendar = currentDate.getFullYear() + "-" + (currentDate.getMonth()+1) + "-" + currentDate.getDate() // 현재 날짜
    var amPm = 'AM'; // 초기값 AM
    var currentHours = addZeros(currentDate.getHours(),2); 
    var currentMinute = addZeros(currentDate.getMinutes() ,2);
    var currentSeconds =  addZeros(currentDate.getSeconds(),2);
    
    if(currentHours >= 12){ // 시간이 12보다 클 때 PM으로 세팅, 12를 빼줌
        amPm = 'PM';
        currentHours = addZeros(currentHours - 12,2);
    }
    clock.innerHTML = currentHours+":"+currentMinute+":"+currentSeconds +" <span style='font-size:50px;'>"+ amPm+"</span>"; //날짜를 출력해 줌
    setTimeout("printClock()",1000);         // 1초마다 printClock() 함수 호출
}
function addZeros(num, digit) { // 자릿수 맞춰주기
      var zero = '';
      num = num.toString();
      if (num.length < digit) {
        for (i = 0; i < digit - num.length; i++) {
          zero += '0';
        }
      }
      return zero + num;
}

//https://www.chartjs.org/docs/latest/ 출처참고
//막대그래프
function hist(id_, title_, labels_, data_, bgcolor_, tfsize_, lfsize_, fcolor_) {
    var ctx = document.getElementById(id_);
    function op100(value, index, array) {
        return value + "FF";
    }
    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: labels_,
            datasets: [{
                label: ' ',
                data: data_,
                backgroundColor: bgcolor_.map(op100),
                borderColor: bgcolor_.map(op100),
                borderWidth: 1
            }]
        },
        options:{
            layout: {
                padding: {
                    left: 50,
                    right: 50,
                    top: 50,
                    bottom: 0
                }
            },
             tooltips: {
                titleFontSize: tfsize_,
                bodyFontSize: tfsize_,
                //titleFontFamily: ,
                //bodyFontFamily: ,
            },
            legend: {
                display: false,
                //fontFamily: ,
            },
            title: {
                display: (title_ == "") ? false:true,
                text: title_,
                fontSize : tfsize_,
                fontColor: fcolor_,
                //fontFamily: ,
            },
            scales: {
                yAxes: [{
                    display: false,
                    ticks: {
                    fontSize : lfsize_,
                    fontColor: fcolor_,
                    },
                    barPercentage: 10,
                    barThickness: 15,
                    maxBarThickness: 20,
                    minBarLength: 10,
                    gridLines: {
                        offsetGridLines: true
                    }
                }],
                xAxes: [{
                    display: false,
                    ticks: {
                    fontSize : lfsize_,
                    fontColor: fcolor_,
                    },
                    barPercentage: 10,
                    barThickness: 15,
                    maxBarThickness: 20,
                    minBarLength: 10,
                    gridLines: {
                        offsetGridLines: true
                    }
                }]
            },
            maintainAspectRatio: false
        }
    });
}
//원형그래프
function pie(id_, title_, labels_, data_, bgcolor_, tfsize_, lfsize_, fcolor_) {
    var ctx = document.getElementById(id_);
    function op100(value, index, array) {
        return value + "FF";
    }
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels_,
            datasets: [{
                label: ' ',
                data: data_,
                backgroundColor: bgcolor_.map(op100),
                borderColor: bgcolor_.map(op100),
                borderWidth: 1
            }]
        },
        options:{
            legend: {
                display: true,
               labels: {
                    fontSize : lfsize_,
                    fontColor: fcolor_,
                    //fontFamily: ,
                }
            },
            title: {
                display: (title_ == "") ? false:true,
                text: title_,
                fontSize : tfsize_,
                fontColor: fcolor_,
                //fontFamily: ,
            },
            tooltips: {
                titleFontSize: tfsize_,
                bodyFontSize: tfsize_,
                //titleFontFamily: ,
                //bodyFontFamily: ,
            }
        }
    });
}
//선형그래프
function line(id_, title_, labels_, data_, bgcolor_, tfsize_, lfsize_, fcolor_) {
    var ctx = document.getElementById(id_);
    function op100(value, index, array) {
        return value + "FF";
    }
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels_,
            datasets: [{
                label: ' ',
                data: data_,
                backgroundColor: "#00000000",
                borderColor: bgcolor_,
                borderWidth: 2
            }]
        },
        options:{
            legend: {
                display: false,
            },
            title: {
                display: (title_ == "") ? false:true,
                text: title_,
                fontSize : tfsize_,
                fontColor: fcolor_,
                //fontFamily: ,
            },
             tooltips: {
                titleFontSize: tfsize_,
                bodyFontSize: tfsize_,
                displayColors: true,
                //titleFontFamily: ,
                //bodyFontFamily: ,
            },
             scales: {
                yAxes: [{
                    display: true,
                    ticks: {
                    fontSize : lfsize_,
                    fontColor: fcolor_,
                }
                }],
                xAxes: [{
                    display: true,
                    ticks: {
                    fontSize : lfsize_,
                    fontColor: fcolor_,
                }
                }]
            }
           
        }
    });
}

//날짜 list 형식으로 calculate 함수
//'today' or 'week' or 'month' 를 인자로 넘긴다.
function calculate_date_list(what) {
    let currentDate = new Date();
    let date_one = currentDate.getDate();
    let date_week = [];
    let date_month = [];
    if (what == 'today'){
        return date_one;   
    } else if (what == 'week'){
        for (let i = 0; i < 7; i++){
            currentDate.setDate(currentDate.getDate() - 1)
            date_week.push(currentDate.getDate());
        }
        return date_week.reverse();
    } else if (what == 'month'){
        currentDate.setDate(currentDate.getDate() - 1);
        date_month.push(currentDate.getDate());
        for (let i = 0; i < 6; i++){
            currentDate.setDate(currentDate.getDate() - 5);
            date_month.push(currentDate.getDate());
        }
        return date_month.reverse();
    }
}

//AJAX 데이터 요청 밎 송신 (what == 'visitor' or 'post' or 'both')
function visitor_post_graph(what, who){
    let a_jax = A_JAX(TEST_IP+'get_analysis/'+31, "GET", null, null);
    $.when(a_jax).done(function(){
        let json = a_jax.responseJSON;
        if (json['result'] == 'success'){
            if (who == 'visitor'){
                draw_visitor_graph(what, json);
            } else if (who == 'post'){
                draw_post_upload_graph(what, json);
            } else if (who == 'both'){
                draw_visitor_graph(what, json);
                draw_post_upload_graph(what,json);
            }
        } else {
            snackbar("일시적인 오류로 정보를 가져오지 못하였습니다.");
            return;
        }
    });
}

//방문자수 그래프 그리는 함수 (what == 'week' or 'month')
function draw_visitor_graph(what, json) {
    let user_color = json['user_color'];
    let font_color = "#e2e2e2";
    let graph_lable_name = calculate_date_list(what);
    let graph_lable_value = [];    // 연산값
    let visitor_cnt_list = json['everyday_analysis'];
    let total_visitor = json['total_visitor'];
    let today_visitor = json['today_visitor'];
    $('#M_statistics_today_data').empty();
    $('#M_statistics_today_data').append(today_visitor);  //오늘 방문자수
    $('#M_statistics_today_all_data').empty();
    $('#M_statistics_today_all_data').append(total_visitor);
    //visitor_cnt_list 가 7개 미만일 경우
    if (visitor_cnt_list.length < 7){
        graph_lable_name = [];
        for (let i =0; i< visitor_cnt_list.length; i++){
            let time = new Date(Date.parse(visitor_cnt_list[i]['v_date']));
            graph_lable_name.push(time.getDate()*1);
        }
        for (let i = 0; i< visitor_cnt_list.length; i++){
            graph_lable_value.push(visitor_cnt_list[i]['visitor_cnt']*1);
        }
    }
    else if (what == 'week'){
        for (let i = visitor_cnt_list.length - 7; i< visitor_cnt_list.length; i++){
            graph_lable_value.push(visitor_cnt_list[i]['visitor_cnt']*1);
        }
    } else if (what == 'month'){
        let j = 6;
        for (let i = visitor_cnt_list.length - 1; i >= 0; i--){
            let time = new Date(Date.parse(visitor_cnt_list[i]['v_date']));
            if (time.getDate()*1 == graph_lable_name[j]){
                graph_lable_value.unshift(visitor_cnt_list[i]['visitor_cnt']);
                j -= 1;
            }
        }
        if (graph_lable_value.length != 7){
            let value_list_len = 7 - graph_lable_value.length;
            for (let i = 0; i < value_list_len; i++){
                graph_lable_value.unshift(0);
            }
        }
    }
    if (what == 'today'){
        return visitor_cnt_list[visitor_cnt_list.length-1]['visitor_cnt'];
    } else {
        if (localStorage.getItem('modakbul_theme') != null){
            if (localStorage.getItem('modakbul_theme') == 'white'){
                font_color = '#5f6f81';
            } else {
                font_color = '#e2e2e2';
            }
        }
        $('#M_statistics_graph_visitor_js').empty();
        $('#M_statistics_graph_visitor_js').append('<canvas id="M_today_visitors_graph" width="auto" height="auto"></canvas>');
        //선형 그래프
        line(
            "M_today_visitors_graph",   // target ID
            "방문자 수",                 // graph title
            graph_lable_name,           // lable_name_list
            graph_lable_value,          // lable_value_list
            user_color,                // line_color
            20,                         // title_font_size
            label_font_size_media,      // label_font-size
            font_color                  // font_color
            );
    }
}

//포스트 업로드 그래프 그리는 함수 (what == 'week' or 'month')
function draw_post_upload_graph(what, json) {
    let user_color = json['user_color'];
    let font_color = "#e2e2e2";
    let graph_lable_name = calculate_date_list(what);
    let graph_lable_value = [];    // 연산값
    let visitor_cnt_list = json['everyday_analysis'];
    //visitor_cnt_list 가 7개 미만일 경우
    if (visitor_cnt_list.length < 7){
        graph_lable_name = [];
        for (let i =0; i< visitor_cnt_list.length; i++){
            let time = new Date(Date.parse(visitor_cnt_list[i]['v_date']));
            graph_lable_name.push(time.getDate()*1);
        }
        for (let i = 0; i< visitor_cnt_list.length; i++){
            graph_lable_value.push(visitor_cnt_list[i]['posts_cnt']*1);
        }
    }
    else if (what == 'week'){
        for (let i = visitor_cnt_list.length - 7; i< visitor_cnt_list.length; i++){
            graph_lable_value.push(visitor_cnt_list[i]['posts_cnt']*1);
        }
    } else if (what == 'month'){
        let j = 6;
        for (let i = visitor_cnt_list.length - 1; i >= 0; i--){
            let time = new Date(Date.parse(visitor_cnt_list[i]['v_date']));
            if (time.getDate()*1 == graph_lable_name[j]){
                graph_lable_value.unshift(visitor_cnt_list[i]['posts_cnt']);
                j -= 1;
            }
        }
        if (graph_lable_value.length != 7){
            let value_list_len = 7 - graph_lable_value.length;
            for (let i = 0; i < value_list_len; i++){
                graph_lable_value.unshift(0);
            }
        }
    }
    if (what == 'today'){
        snackbar("잘못된 접근입니다.");
        return;
    } else {
        if (localStorage.getItem('modakbul_theme') != null){
            if (localStorage.getItem('modakbul_theme') == 'white'){
                font_color = '#5f6f81';
            } else {
                font_color = '#e2e2e2';
            }
        }
        $('#M_statistics_graph_post_upload_js').empty();
        $('#M_statistics_graph_post_upload_js').append('<canvas id="M_today_post_upload_graph" width="auto" height="auto"></canvas>');
        //선형 그래프
        line(
            "M_today_post_upload_graph", // target ID
            "포스트 업로드 수",                 // graph title
            graph_lable_name,           // lable_name_list
            graph_lable_value,          // lable_value_list
            user_color,                // line_color
            20,                         // title_font_size
            label_font_size_media,      // label_font-size
            font_color                  // font_color
            );
    }
}

//좋아요 그래프 그리는 함수 
function draw_like_graph(what) {
    let what_num = 7;
    if (what == 'today'){
        what_num = 1;
    } else if (what == 'week'){
        what_num == 7;
    } else if (what == 'month'){
        what_num == 30;
    }
    let font_color = "#e2e2e2";
    let graph_lable_name = [];
    let graph_lable_value = [];    // 연산값
    let a_jax = A_JAX(TEST_IP+'posts_like_rank/'+what_num, "GET", null, null);
    $.when(a_jax).done(function(){
        let json_like = a_jax.responseJSON;
        if (json_like['result'] == 'success'){
            if (localStorage.getItem('modakbul_theme') != null){
                if (localStorage.getItem('modakbul_theme') == 'white'){
                    font_color = '#5f6f81';
                } else {
                    font_color = '#e2e2e2';
                }
            }
            let posts_like_rank = json_like['posts_like_rank'];
            let posts_like_rank_len = posts_like_rank.length;
            if (posts_like_rank_len > 7){
                posts_like_rank_len = 7;
            } else if (posts_like_rank_len == 0){
                snackbar("좋아요된 게시글이 없습니다.");
                return;
            }
            for (let i = 0; i < posts_like_rank_len; i++){
                if (posts_like_rank[i]['post_title'].length > 15){
                    posts_like_rank[i]['post_title'] = posts_like_rank[i]['post_title'].slice(0,15) + "..";
                }
                graph_lable_name.push(posts_like_rank[i]['post_title']);
                graph_lable_value.push(posts_like_rank[i]['like_cnt']);
            }
            
            $('#M_statistics_graph_like_js').empty();
            $('#M_statistics_graph_like_js').append('<canvas id="M_today_post_like" width="auto" height="auto"></canvas>');
            pie(    // HOT 게시글은 TOP 7 만 보여주기
                "M_today_post_like", //해당 캔버스 아이디
                "TOP 게시글", // 없으면 ""
                graph_lable_name, //레이블
                graph_lable_value,               // 각 레이블의 값
                ['#FF6384',        // 각 막대의 색깔(모든 리스트의 길이는 같게)
                '#36A2EB',
                '#FFCE56',
                '#4BC0C0',
                '#9966FF',
                '#FF9F40',
                '#2EFE2E'],
                20,  // 제목폰트
                label_font_size_media,  // 라벨 폰트
                font_color // 모든 글씨 색깔
                );
        } else {
            snackbar("일시적인 오류로 정보를 가져오지 못하였습니다.");
            return;
        }
    });
}

//조회수 그래프 그리는 함수
function draw_view_graph(what) {
    let what_num = 7;
    if (what == 'today'){
        what_num = 1;
    } else if (what == 'week'){
        what_num == 7;
    } else if (what == 'month'){
        what_num == 30;
    }
    let font_color = "#e2e2e2";
    let graph_lable_name = [];
    let graph_lable_value = [];    // 연산값
    let a_jax = A_JAX(TEST_IP+'posts_view_rank/'+what_num, "GET", null, null);
    $.when(a_jax).done(function(){
        let json_view = a_jax.responseJSON;
        if (json_view['result'] == 'success'){
            if (localStorage.getItem('modakbul_theme') != null){
                if (localStorage.getItem('modakbul_theme') == 'white'){
                    font_color = '#5f6f81';
                } else {
                    font_color = '#e2e2e2';
                }
            }
            let posts_view_rank = json_view['posts_view_rank'];
            let posts_view_rank_len = posts_view_rank.length;
            if (posts_view_rank_len > 7){
                posts_view_rank_len = 7;
            } else if (posts_view_rank_len == 0){
                snackbar("조회된 게시글이 없습니다.");
                return;
            }
            for (let i = 0; i < posts_view_rank_len; i++){
                if (posts_view_rank[i]['post_title'].length > 15){
                    posts_view_rank[i]['post_title'] = posts_view_rank[i]['post_title'].slice(0,15) + "..";
                }
                graph_lable_name.push(posts_view_rank[i]['post_title']);
                graph_lable_value.push(posts_view_rank[i]['post_view']);
            }
            
            $('#M_statistics_graph_view_js').empty();
            $('#M_statistics_graph_view_js').append('<canvas id="M_today_post_view" width="auto" height="auto"></canvas>');
            pie(    // HOT 게시글은 TOP 7 만 보여주기
            "M_today_post_view", //해당 캔버스 아이디
            "HOT 게시글", // 없으면 ""
            graph_lable_name, //레이블
            graph_lable_value,               // 각 레이블의 값
            ['#FE9A2E',        // 각 막대의 색깔(모든 리스트의 길이는 같게)
            '#2EFE2E',
            '#FE2EF7',
            '#58FAF4',
            '#FA5858',
            '#8181F7',
            '#642EFE'],
            20,  // 제목폰트
            label_font_size_media,  // 라벨 폰트
            font_color // 모든 글씨 색깔
            );
        } else {
            snackbar("일시적인 오류로 정보를 가져오지 못하였습니다.");
            return;
        }
    });
}

//설문조사 검색 함수
function search_vote_analysistics(tag) {
    let target = $('#M_statistics_vote_list_target');
    let value = tag.val();
    for (let i = 0; i < vote_list_for_search.length; i++){
        let num = vote_list_for_search[i]['vote_id'];
        $('div[alt=vote_'+num+']').css('display', 'block');
    }
    for(let i = 0; i < vote_list_for_search.length; i++){
        if (vote_list_for_search[i]['vote_title'].indexOf(value) == -1){
            let num = vote_list_for_search[i]['vote_id'];
            $('div[alt=vote_'+num+']').css('display', 'none');
        }
    }
}
//설문조사 리스트 반환 함수
function search_vote_analysistics_list() {
    $('#M_loading_modal_background').removeClass('display_none');
    let a_jax = A_JAX(TEST_IP+'get_vote_status', 'GET', null, null);
    $.when(a_jax).done(function () {
        let json = a_jax.responseJSON;
        if (json['result'] == 'success'){
            let div_class = 'M_info_div M_board_content M_boxshadow wow flipInX';
            if (localStorage.getItem('modakbul_theme') === 'dark') {
                div_class +=  ' M_boxshadow_dark_shadow" style="' +
                    'visibility: visible; background-color: rgb(73, 78, 82); color: rgb(245, 246, 250); border: 0px solid rgb(221, 221, 221);';
            }
            let undone_list = json['undone_vote'];
            for (let i=0; i<undone_list.length; i++) {
                let data = undone_list[i];
                let start_time = data['start_date'];
                let end_time = data['end_date'];
                let title = data['vote_title'];
                let vote_id = data['vote_id'];
                let views = data['join_cnt'];
                let undone_div_class = ' M_statistics_undone_vote ' + div_class;
                $("#M_statistics_vote_list_target")
                    .append(
                        '<div class="' + undone_div_class + '" onclick="votemodal_open('+ vote_id +')"  alt="vote_'+ vote_id +'">' +
                        '<div class="M_vote_date_title">기간 : </div>' +
                        '<div class="M_time_info">'+ start_time + ' ~ </div>' +
                        '<div class="M_time_info">'+ end_time + '</div>' +
                        '<div class="M_vote_content_info">' + views +'</div>' +
                        '<i class="fas fa-male M_vote_content_icon"></i>' +
                        '<div class="M_board_content_title">'+ title +'</div>' +
                        '</div>');
            }
            let done_list = json['done_vote'];
            for (let i=0; i<done_list.length; i++) {
                let data = done_list[i];
                let start_time = data['start_date'];
                let end_time = data['end_date'];
                let title = data['vote_title'];
                let vote_id = data['vote_id'];
                let views = data['join_cnt'];
                let done_div_class = ' M_statistics_done_vote ' + div_class;
                $("#M_statistics_vote_list_target")
                    .append(
                        '<div class="' + done_div_class + ' M_statistics_done_vote" onclick="votemodal_open('+ vote_id +')" alt="vote_'+ vote_id +'">' +
                        '<div class="M_vote_date_title">기간 : </div>' +
                        '<div class="M_time_info">'+ start_time + ' ~ </div>' +
                        '<div class="M_time_info">'+ end_time + '</div>' +
                        '<div class="M_vote_content_info">' + views +'</div>' +
                        '<i class="fas fa-male M_vote_content_icon"></i>' +
                        '<div class="M_board_content_title">'+ title +'</div>' +
                        '</div>');
            }
            //모든 vote 리스트
            vote_list_for_search = undone_list.concat(done_list);
            $('#M_loading_modal_background').addClass('display_none');
        } else {
            $('#M_loading_modal_background').addClass('display_none');
            snackbar("일시적인 오류로 정보를 가져오지 못하였습니다.");
        }
    });
}

//설문조사 페이지 열기
function votemodal_open(get_vote_id){
    let token = localStorage.getItem('modakbul_token');
    if (token == null){
        snackbar("로그인해주세요.");
        return;
    }
    get_vote_info(get_vote_id);
    now_postmodal_top = $(window).scrollTop();
    history.pushState(null, null, "#post");
    is_votemodal_open = 1;
    $('#M_user_vote_modal_background').css("height", $(window).height() + 100);
    $('#M_user_vote_modal_background').css('position', "fixed");
    $('#M_user_vote_modal_background').removeClass('display_none');
    $('#M_user_vote_modal_background').removeClass('fadeOut');
    $('#M_user_vote_modal_background').addClass('fadeIn');
    $('html, body').css({'overflow': 'hidden'});
    $('html, body').css({'top': now_postmodal_top*-1});
    $('html, body').addClass('M_modal_open_fixed');
    $('#M_user_vote_modal_container').removeClass('fadeOutDown');
    $('#M_user_vote_modal_container').addClass('fadeInUp');
    $('#M_user_vote_modal_container').removeClass('display_none');
    $('#M_user_vote_modal_container').css('height', $(window).height() - 70);
}

//설문조사 페이지 닫기
function votemodal_close(is_secret = null){
    is_votemodal_open = 0;
    image_modal_close();    
    $('#M_menu_button_modify').addClass('display_none_important');
    $('#M_menu_button_trash').addClass('display_none_important');
    $("#M_post_user_comment_input").blur();
    history.replaceState(null, null, "#list");
    $('#M_user_vote_modal_background').addClass('fadeOut');
    $('#M_user_vote_modal_background').removeClass('fadeIn');
    $('#M_user_vote_modal_container').addClass("fadeOutDown");
    $('#M_user_vote_modal_container').removeClass('fadeInUp');
    setTimeout(function(){
        $('#M_user_vote_modal_container').addClass("display_none");
        $('#M_user_vote_modal_background').addClass('display_none');
    }, 400);
    $('html, body').removeAttr("style");
    $('html, body').removeClass('M_modal_open_fixed');
    $('html').scrollTop(now_postmodal_top);
    $("#M_post_user_comment_input").val("");
    empty_vote_info();
}

// modal 이 외 클릭 시, modal 닫기
$(document).mouseup(function (e) {
    if (is_votemodal_open == 1 && is_image_modal_open == 0){
        var container = $("#M_user_vote_modal_container");
        let loading = $('#M_loading_modal_background');
        if (!container.is(e.target) && container.has(e.target).length === 0 && !loading.is(e.target) && loading.has(e.target).length === 0){
            votemodal_close();
        }
    }
});

// ESC 키 누를시 닫기
$(document).keydown(function(event){
    if (event.keyCode == 27){
        if (is_image_modal_open == 1){
            image_modal_close();
        }
        else {
            if (is_votemodal_open == 1){
                votemodal_close();
            }
            if (search_bar_value == 1){
                search_bar_value = 0;
                var container = $("#M_search_bar");
                var search_bar = $("#M_search_bar");
                search_bar.removeClass("fadeInDown");
                search_bar.addClass("fadeOutUp");
                setTimeout(function(){search_bar.addClass("display_none")}, 400);
                $("#M_search_input").val("")
            }
        }
    }
});

//설문조사 정보 가져오는 함수
function get_vote_info(get_vote_id) {
    let a_jax = A_JAX(TEST_IP+"get_vote_select_status/"+get_vote_id, "GET", null, null);
    $.when(a_jax).done(function(){
        let json = a_jax.responseJSON;
        if (json['result'] == "success"){
            $('#M_user_post_modal_container').attr('alt', "vote_"+get_vote_id);
            $('#M_vote_profile_color').css("background-color", "#d8d8d8");
            $('#M_vote_author').append(json['vote']['vote_author']);
            $('#M_vote_start_date').append(json['vote']['start_date']);
            $('#M_vote_end_date').append(json['vote']['end_date']);
            $('#M_vote_top_title').append(json['vote']['vote_title']);
            $('#M_vote_url_copy').attr('alt', get_vote_id);
            $('#M_vote_body_icons_data').append(json['vote']['join_cnt']);
            $('#M_vote_body').append(json['vote']['vote_content']);
            if (json['vote']['vote_file_path'] == null){
                $('#M_vote_picture_container').addClass('display_none_important');
            } else {
                $('#M_vote_picture').attr('src', "../static/files/"+json['vote']['vote_file_path']);
            }
            let que_list = json['vote']['que_list'];
            let que_len = que_list.length;
            $('#M_vote_que_target').empty();    // Graph 들어갈 target 비워주기
            for (let i = 0; i < que_len; i++){
                //그래프 요소
                let graph_title;
                let graph_lable_name = [];
                let graph_lable_value = [];
                let all_graph_lable_color = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'];
                let graph_lable_color = [];
                let graph_lable_font_size = label_font_size_media;
                let font_color = "#e2e2e2";
                if (localStorage.getItem('modakbul_theme') != null){
                    if (localStorage.getItem('modakbul_theme') == 'white'){
                        font_color = '#5f6f81';
                    } else {
                        font_color = '#e2e2e2';
                    }
                }
                //ajax 요소
                let que_one = que_list[i];
                let que_id = que_one['que_id'];
                let que_type = que_one['que_type'];
                let que_title = que_one['que'];
                if (que_type == 0 || que_type == 1){    // 체크박스 또는 라디오 박스일 경우
                    let select_list = que_one['select'];
                    let graph_height = 160 + (select_list.length - 1) * 80;
                    graph_title = que_title;
                    for (let j = 0; j < select_list.length; j++){
                        graph_lable_name.push(select_list[j]['select_content']);
                        graph_lable_value.push(select_list[j]['select_cnt']);
                        graph_lable_color.push(all_graph_lable_color[i]);
                    }
                    $('#M_vote_que_target').append('<div class="chart-container M_statistics_body_check_type animated" style="cursor: pointer; height: '+graph_height+'px" onclick="statistics_admin_check_user($(this),'+que_id+')" data-wow-duration = "0.6s" alt="que_'+que_id+'">\
                                                        <canvas id="hist'+que_id+'"" width="auto" height="auto"></canvas>\
                                                    </div>');
                    hist(
                        "hist"+que_id, //해당 캔버스 아이디
                        graph_title, // 없으면 ""
                        graph_lable_name, //레이블
                        graph_lable_value,               // 각 레이블의 값
                        graph_lable_color,
                        20,  // 제목폰트
                        label_font_size_media,  // 라벨 폰트
                        font_color // 모든 글씨 색깔
                        );
                } else {                                // 단답형일 경우
                    graph_title = que_title;
                    graph_lable_name.push("참여 인원 수");
                    graph_lable_value.push(json['vote']['join_cnt']);
                    graph_lable_color.push(all_graph_lable_color[i]);
                    $('#M_vote_que_target').append('<div class="chart-container M_statistics_body_answer_type animated" style="cursor: pointer" onclick="statistics_admin_check_user($(this),'+que_id+')" data-wow-duration = "0.6s" alt="que_'+que_id+'">\
                                                        <canvas id="hist'+que_id+'"" width="auto" height="auto"></canvas>\
                                                    </div>');
                     hist(
                        "hist"+que_id, //해당 캔버스 아이디
                        graph_title, // 없으면 ""
                        graph_lable_name, //레이블
                        graph_lable_value,               // 각 레이블의 값
                        graph_lable_color,
                        20,  // 제목폰트
                        label_font_size_media,  // 라벨 폰트
                        font_color // 모든 글씨 색깔
                        );
                }
                //경계선 삽입
            }
        }
        else {
            snackbar("일시적인 오류로 정보를 가져오지 못하였습니다.");
        }
    });
}

//설문조사 정보 비우는 함수
function empty_vote_info(){
    $('#M_vote_que_target').empty();
    $('#M_vote_author').empty();
    $('#M_vote_start_date').empty();
    $('#M_vote_end_date').empty();
    $('#M_vote_top_title').empty();
    $('#M_vote_picture_container').removeClass('display_none_important');
    $('#M_vote_body').empty();
    $('#M_vote_body_icons_data').empty();
    $('#M_vote_picture').attr('src', '#');
}

//어드민일시, 투표 유저 확인 함수
function statistics_admin_check_user(tag, que_id) {
    let token = localStorage.getItem('modakbul_token');
    if (token != null){
        if (tag.hasClass('M_statistics_body_answer_type')){
            let a_jax = A_JAX(TEST_IP+"get_vote_select_status_user/"+que_id, "GET", token, null);
            $.when(a_jax).done(function(){
                let json = a_jax.responseJSON;
                if (json['result'] == 'success'){
                    let div_height = tag.height() + 50; //px
                    tag.addClass('flipOutX');       //변환 before
                    let div_create = document.createElement('div');
                    div_create.classList.add("M_statistics_body_answer_type_user");
                    div_create.classList.add("display_none_important");
                    div_create.classList.add("animated");
                    div_create.setAttribute('onclick', 'return_user_to_graph($(this), '+que_id+')');
                    div_create.setAttribute('data_wow-duration','0.6s');
                    let select_user_list = json['select_user_list'];
                    for (let i = 0; i< select_user_list.length; i++){
                        let p_create = document.createElement('p');
                        p_create.classList.add("M_statistics_body_answer_type_user_info");
                        p_create.append(select_user_list[i]['answer']);
                        div_create.append(p_create);
                    }
                    tag.before($(div_create));
                    setTimeout(function() {
                        tag.toggleClass('display_none_important');
                        div_create.classList.remove("display_none_important");
                        div_create.classList.add('flipInX');
                        tag.removeClass('flipOutX');
                    }, 600);
                } else if (json['result'] == 'bad request'){
                    snackbar("잘못된 접근입니다.");
                } else if (json['result'] == 'you are not admin'){
                    tag.addClass('rubberBand');
                    setTimeout(function() {
                        tag.removeClass('rubberBand');
                    }, 600);
                    return;
                } else {
                    snackbar("일시적인 오류로 정보를 가져오지 못하였습니다.");
                }
            });
        } else {
            tag.addClass('rubberBand');
            setTimeout(function() {
                tag.removeClass('rubberBand');
            }, 600);
        }
    } else {
        tag.addClass('rubberBand');
        setTimeout(function() {
            tag.removeClass('rubberBand');
        }, 600);
    }
}

//다시 그래프로 되돌리기 함수
function return_user_to_graph(tag, que_id) {
    let graph = $('div[alt=que_'+que_id+']');
    tag.removeClass('flipInX');
    tag.addClass('flipOutX');
    setTimeout(function() {
        tag.remove();
        graph.removeClass('display_none_important');
        graph.addClass('flipInX');
        setTimeout(function() {
            graph.removeClass('flipInX');
        }, 600);
    }, 600);
}

//이미지 모달 열기
function image_modal_open(tag){
    is_image_modal_open = 1;
    let now_src = tag.getAttribute('src');
    $('#M_image_modal_container').attr('src', now_src);
    $('#M_image_modal_background').css('position', "fixed");
    $('#M_image_modal_background').removeClass('display_none');
    $('#M_image_modal_background').removeClass('fadeOut');
    $('#M_image_modal_background').addClass('fadeIn');
    $('html, body').css({'overflow': 'hidden'});
    $('html, body').addClass('M_modal_open_fixed');
}

//이미지 모달 닫기
function image_modal_close(){
    $('#M_image_modal_background').addClass('fadeOut');
    $('#M_image_modal_background').removeClass('fadeIn');
    setTimeout(function(){
        $('#M_image_modal_background').addClass('display_none');
        is_image_modal_open = 0;
    }, 400);
    $('html').scrollTop(now_postmodal_top);
}


//document load시 실행되는함수
function statistics(){
    $('#M_statistics_vote_list_target').empty();    //설문조사 target 비우기
    $('.M_statistics_vote_list_serach_input').val("");
    $('html').animate({scrollTop : 0}, 400);    //제일 위로 스크롤 애니메이션
    printClock();   // 현재시간 JS
    visitor_post_graph('week' ,'both'); //방문자수, 포스트업로드수
    draw_like_graph('week');    //좋아요 그래프
    draw_view_graph('week');    //조회수 그래프
    search_vote_analysistics_list();    //설문조사 통계
}