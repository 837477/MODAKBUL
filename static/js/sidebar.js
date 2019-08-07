$(window).ready(function () {
    let a_jax = A_JAX(TEST_IP+'get_boards', 'GET', null, null);
    $.when(a_jax).done(function () {
        let result_html = '<ul id="gn-menu2" class="gn-menu">';
        let data = a_jax.responseJSON.boards;
        let result_list = [];
        let nested_list = [];

        for (let i=0; i<data.length; i++) {
            if (data[i].board_url.split('_')[1] === undefined) result_list.push(data[i]);
            else nested_list.push(data[i]);
        }

        for (let i=0; i<nested_list.length; i++) {
            for (let j=0; j<result_list.length; j++) {
                for (let k=0; k<nested_list[i].board_url.split('_').length; k++) {
                    let check;
                    if (Array.isArray(result_list[j]) === true) {
                        check = result_list[j][0].board_url;
                    }
                    else {
                        check = result_list[j].board_url;
                    }

                    if (nested_list[i].board_url.split('_')[k] == check)
                    {
                        if (Array.isArray(result_list[j]) === true) {
                            result_list[j].push(nested_list[i]);
                        }
                        else {
                            result_list[j] = [result_list[j], nested_list[i]];
                        }
                    }
                }
            }
        }

        for (let i=0; i<result_list.length; i++) {
            if (Array.isArray(result_list[i]) === true) {
                let subboard = '';
                for (let j=1; j<result_list[i].length; j++) {
                    subboard += '<a href="/board?type=' + result_list[i][j].board_url + '">' +
                        '<i class="fas fa-minus M_dropdown_hypeon"></i>' + result_list[i][j].board_name + '</a>';
                }
                let icon = '';
                if (result_list[i][0].board_name === '학생회비내역') icon = 'fas fa-file-invoice-dollar';
                else if (result_list[i][0].board_name === '대외활동')icon ='fas fa-cubes';
                else icon = 'fas fa-sticky-note';
                result_html +=
                    '<li class="M_dropdown_list">' +
                    '<div onclick="location.href='+"'/board?type="+result_list[i][0].board_url+"'"+'" class="M_dropdown_real_body">' +
                    '<i id="M_studentMoneyButton" class="' + icon + '" style="padding: 0 23px"></i>' + result_list[i][0].board_name +
                    '</div>' +
                    '<i id="M_dropdown_icon_money" class="fas fa-sort-down M_dropdown_icon" onclick="M_dropdown_global($(this))"></i>' +
                    '</li>' +
                    '<div id="M_studentMoney" class="display_none"><div>' + subboard + '</div></div>';
            }
            else {
                if (result_list[i].board_name === '공지사항') {
                    result_html += '<li><a href="/board?type='+ result_list[i].board_url+'" class="M_nav_user_button">' +
                        '<i class="fas fa-bullhorn" style="padding: 0 22px"></i>' + result_list[i].board_name + '</a></li>';
                }
                else if (result_list[i].board_name === '학생회소개') {
                    result_html += '<li><a href="/intro" class="M_nav_user_button">' +
                        '<i class="far fa-bell" style="padding: 0 22px"></i>' + result_list[i].board_name + '</a></li>';
                }
                else if (result_list[i].board_name === '민원') {
                    result_html += '<li><a href="/board?type=민원" class="M_nav_user_button">' +
                        '<i class="fas fa-feather-alt" style="padding: 0 22px"></i>민원</a></li>';
                }
                else if (result_list[i].board_name === '갤러리') {
                    result_html += '<li><a href="/gallery?type=갤러리" class="M_nav_user_button">' +
                        '<i class="far fa-images" style="padding: 0 22px"></i>갤러리</a></li>';
                }
                else if (result_list[i].board_name === '투표/설문조사') {
                    result_html += '<li><a href="/vote" class="M_nav_user_button">' +
                        '<i class="far fa-check-square" style="padding: 0 22px"></i>' + result_list[i].board_name + '</a></li>';
                }
                else if (result_list[i].board_name === '통계자료') {
                    result_html += '<li><a href="/statistics" class="M_nav_user_button">' +
                        '<i class="far fa-chart-bar" style="padding: 0 22px"></i>' + result_list[i].board_name + '</a></li>';
                }
                else {
                    result_html += '<li><a href="/board?type='+ result_list[i].board_url+'" class="M_nav_user_button">' +
                        '<i class="far fa-sticky-note" style="padding: 0 22px"></i>' + result_list[i].board_name + '</a></li>';
                }
            }
        }
        result_html += '</ul>';
        $('#gn-scroller').append(result_html);
        setTheme();
    });
    
    if (localStorage.getItem('modakbul_token') == null){
        return;
    }
    let user_ajax = A_JAX(TEST_IP+'get_userinfo', 'GET', null, null);
    $.when(user_ajax).done(function(){
        let user_json = user_ajax.responseJSON;
        if (user_json['result'] == 'success'){
            if (user_ajax.responseJSON.user_tags.indexOf('ADMIN') !== -1) {
                $('#gn-menu2').append('<li><a href="/settings" class="M_nav_user_button">' +
                    '<i class="fas fa-cog" style="padding: 0 22px"></i>설정</a></li>');
                setTheme();
            }
        } else {
            snackbar("일시적인 오류로 정보를 불러오지 못하였습니다.");
        }
    });
});

var check_logo_cnt = 0;
function EE_change_logo_to_fire(tag) {
    check_logo_cnt = 1;
    setTimeout(function() {
        if (check_logo_cnt != 0){
            localStorage.setItem('modakbul_logo', 'fire');
            tag.addClass('display_none_important');
            $('#logo_change_target_fire').removeClass('display_none_important');
            snackbar("모닥불 프로젝트");
        }
    }, 5000);
}
function EE_chage_logo_to_logo(tag) {
    check_logo_cnt = 1;
    setTimeout(function() {
        if (check_logo_cnt != 0){
            localStorage.removeItem('modakbul_logo');
            tag.addClass('display_none_important');
            $('#logo_change_target_logo').removeClass('display_none_important');
        }
    }, 5000);
}
function EE_return_logo() {
    check_logo_cnt = 0;
}