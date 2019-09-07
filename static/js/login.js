//user이 좋아요한 포스트 id
var user_like_posts_id = [];
//user이 쓴 comment
var user_comments_id = [];
//로그인 버튼을 누를 시, 실행되는 함수
function user_login(){
	var login_ID = $('#user_id').val();	// user_id 란 ID 값의 value 값 가져옴
	var login_PW = $('#user_pw').val();	// user_pw 란 ID 값의 value 값 가져옴
	
	if (login_ID.length <= 0 || login_PW.length <= 0){
		snackbar("아이디 및 비밀번호를 입력해주세요.");
		return;
	}
	$('#M_loading_modal_background').removeClass('display_none');
	var send_data = {id: login_ID, pw: login_PW};
	var a_jax = A_JAX(TEST_IP+"sign_in_up", "POST", null, send_data);	//"/login" 이라는 url에 아이디/비밀번호 data 전송
	$.when(a_jax).done(function(){
		$('#M_loading_modal_background').addClass('display_none');
		var json = a_jax.responseJSON;
		if (json['result'] == "you are not sejong"){			// result 값이 "your not Sejong" 이라면 실행
			snackbar("올바르지 않은 회원 정보입니다.");
		}
		else if (json['result'] == "wrong info"){	// result 값이 "password incorrect" 이라면 실행
			snackbar("비밀번호를 다시 입력해주세요.");
		}
		else if (json['result'] == "blacklist"){			// 블랙리스트일 경우
			snackbar("블랙리스트 입니다.");
		}
		else if (json['result'] == "success"){				// result 값이 "success" 이라면 실행
			// 로그인 성공 token 생성
			localStorage.setItem('modakbul_token', json['access_token']);
			snackbar("로그인 성공!");
			setTimeout(function() {location.href = "/";}, 300);
		}
		else {
			snackbar("올바르지 않은 회원 정보입니다.");
		}
	});
}
//로그아웃 버튼을 누를 시, 실행되는 함수
function user_logout(){
	localStorage.removeItem('modakbul_token');
	$("#M_nav_user_login").animate({height: 'hide'}, 'fast');
	snackbar("로그아웃 되었습니다.");
}
function user_logout_setting(){
	localStorage.removeItem('modakbul_token');
	$("#M_nav_user_login").animate({height: 'hide'}, 'fast');
	snackbar("로그아웃 되었습니다.");
	location.href = '/';
}

//엔터 로그인
function login_enter(){
    if (window.event.keyCode == 13) {
        user_login();
    }
}

function need_login_snackbar(){
	snackbar("로그인을 해주세요!");
}

function get_user_info() {
	//소융대 학과 모음집
	var majors = ['데이터사이언스학과', '디자인이노베이션', '디지털콘텐츠학과', '만화애니메이션텍', '소프트웨어학과', '정보보호학과', '지능기전공학부', '창의소프트학부', '컴퓨터공학과'];
	var token = localStorage.getItem('modakbul_token');
	if (token == null){
		return;
	}
	var color = $('#M_user_img');
	var name = $('#M_user_content_name');
	var major = $('#M_user_content_major');
	var number = $('#M_user_content_number');
	$('#M_loading_modal_background').removeClass('display_none');
	var a_jax = A_JAX(TEST_IP+"get_userinfo", "GET", token, null);
	$.when(a_jax).done(function(){
		$('#M_loading_modal_background').addClass('display_none');
		var json = a_jax.responseJSON;
		if (json['result'] == "success"){
			name.empty();
			major.empty();
			number.empty();
			if (json['user_tags'].length > 1){
				for (var i=0; i< json['user_tags'].length; i++){
					if (majors.includes(json['user_tags'][i])){
						major.append(json['user_tags'][i]);
					}
				}
			}else{
				major.append(json['user_tags'][0]);
			}
			name.append(json['user_name']);
			number.append(json['user_id']);
			color.css("background-color", json['user_color']);
			for (let i=0; i< json['user_like_posts'].length; i++){
				user_like_posts_id.push(json['user_like_posts'][i]);
			}
			for (let i = 0; i< json['user_comments'].length; i++){
				user_comments_id.push(json['user_comments'][i]);
			}
			//control button 유무 체크
			let searchParams = new URLSearchParams(window.location.search);
			let request_board = searchParams.get('type');
			if (request_board == null){
				return;
			}
			let control_button_ajax = A_JAX(TEST_IP+"get_board/"+request_board, "GET", null, null);
			$.when(control_button_ajax).done(function(){
				let control_button_json = control_button_ajax.responseJSON;
				if (control_button_json['result'] == 'success'){
					if (control_button_json['board']['board_access'] == 1){				//허용
						$('#M_menu_button_container').removeClass('display_none_important');
					} else if (control_button_json['board']['board_access'] == 0){		//비허용
						/*if (json['user_id'] == 'admin'){
							$('#M_menu_button_container').removeClass('display_none_important');
						}*/
					}	
				}
			});
		}
		else if (json['result'] == 'blacklist'){
			snackbar("블랙리스트 입니다.");
			localStorage.removeItem('modakbul_token');
		}
		else{
			snackbar("일시적인 오류로 정보를 가져오지 못하였습니다.");
			localStorage.removeItem('modakbul_token');
		}
	});
}


//로그인 창 애니메이션 함수
(function ($) {
    "use strict";
    /*==================================================================
    [ Focus input ]*/
    $('.input100').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })    
    })
})(jQuery);