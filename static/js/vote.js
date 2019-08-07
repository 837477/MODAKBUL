//라벨, 이름, 시간, 제목, 본문, 조회수, 공감수, 댓글, 첨부파일, 사진, 태그
var is_postmodal_open = 0;
var is_postmodal_fixed_open = 0;
var now_postmodal_top = 0;
var is_image_modal_open = 0;
var img_set = ['png', 'jpg', 'jpeg', 'gif', 'bmp'];
var file_path = "../static/files/";

function postmodal_open(get_post_id){
	let token = localStorage.getItem('modakbul_token');
	if (token == null){
		snackbar("로그인해주세요.");
		return;
	}
	get_post_info(get_post_id);
	$('#M_menu_button_modify').removeClass('display_none_important');
	$('#M_menu_button_trash').removeClass('display_none_important');
	now_postmodal_top = $(window).scrollTop();
	history.pushState(null, null, "#post");
	is_postmodal_open = 1;
	$('#M_user_post_modal_background').css("height", $(window).height() + 100);
	$('#M_user_post_modal_background').css('position', "fixed");
	$('#M_user_post_modal_background').removeClass('display_none');
	$('#M_user_post_modal_background').removeClass('fadeOut');
	$('#M_user_post_modal_background').addClass('fadeIn');
	$('html, body').css({'overflow': 'hidden'});
	$('html, body').css({'top': now_postmodal_top*-1});
	$('html, body').addClass('M_modal_open_fixed');
	$('#M_user_post_modal_container').removeClass('fadeOutDown');
	$('#M_user_post_modal_container').addClass('fadeInUp');
	$('#M_user_post_modal_container').removeClass('display_none');
	$('#M_user_post_modal_container').css('height', $(window).height() - 70);
}

function postmodal_close(is_secret = null){
	is_postmodal_open = 0;
	image_modal_close();	
	$('#M_menu_button_modify').addClass('display_none_important');
	$('#M_menu_button_trash').addClass('display_none_important');
	$("#M_post_user_comment_input").blur();
	if (is_secret != 1){
		//조회수 증가 A_JAX
		let post_get_id = $('#M_user_post_modal_container').attr('alt').split('_')[1]*1;
		let a_jax2 = A_JAX(TEST_IP+"view_up/"+post_get_id, "GET", null, null);
	}
	history.replaceState(null, null, "#list");
	$('#M_user_post_modal_background').addClass('fadeOut');
	$('#M_user_post_modal_background').removeClass('fadeIn');
	$('#M_user_post_modal_container').addClass("fadeOutDown");
	$('#M_user_post_modal_container').removeClass('fadeInUp');
	setTimeout(function(){
  		$('#M_user_post_modal_container').addClass("display_none");
  		$('#M_user_post_modal_background').addClass('display_none');
  	}, 400);
	$('html, body').removeAttr("style");
	$('html, body').removeClass('M_modal_open_fixed');
	$('html').scrollTop(now_postmodal_top);
	$("#M_post_user_comment_input").val("");
	empty_post_info();
}

// modal 이 외 클릭 시, modal 닫기
$(document).mouseup(function (e) {
	if (is_postmodal_open == 1 && is_image_modal_open == 0){
		var container = $("#M_user_post_modal_container");
		var control_button = $('#ss_menu');
		if (!container.is(e.target) && container.has(e.target).length === 0 && !control_button.is(e.target) && control_button.has(e.target).length === 0 && !$('#M_post_user_comment_container').is(e.target) && $('#M_post_user_comment_container').has(e.target).length === 0){
			postmodal_close();
		}
	}
});

$(document).keydown(function(event){
	if (event.keyCode == 27){
		if (is_image_modal_open == 1){
			image_modal_close();
		}
		else {
			if (is_postmodal_open == 1){
				if ($("#M_post_user_comment_input").is(":focus")){
					$("#M_post_user_comment_input").val("");
    				$("#M_post_user_comment_input").blur();
				} else {
					postmodal_close();
				}
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
//포스트 정보 가져오는 함수
function get_post_info(get_post_id) {
	let token = localStorage.getItem('modakbul_token');
	var a_jax = A_JAX(TEST_IP+"get_vote/"+get_post_id, "GET", token, null);
	$.when(a_jax).done(function(){
		var json = a_jax.responseJSON;
		if (json['result'] == "success"){
			$('#M_user_post_modal_container').attr('alt', "vote_"+get_post_id);
			$('#M_post_profile_color').css("background-color", "#d8d8d8");
			$('#M_post_author').append('관리자');
			$('#M_post_start_date').append(json['vote']['start_date']);
			$('#M_post_end_date').append(json['vote']['end_date']);
			$('#M_post_top_title').append(json['vote']['vote_title']);
			$('#M_post_url_copy').attr('alt', get_post_id);
			$('#M_post_body_icons_data').append(json['vote']['join_cnt']);
			$('#M_post_body').append(json['vote']['vote_content']);
			if (json['vote']['vote_file_path'] == null){
				$('#M_vote_picture_container').addClass('display_none_important');
			} else {
				$('#M_vote_picture').attr('src', "../static/files/"+json['vote']['vote_file_path']);
			}
			let que_length = json['vote']['que_list'].length;
			for (let i = 0; i < que_length; i++){
				let section = document.createElement('section');
				section.setAttribute("alt", "que_"+json['vote']['que_list'][i]['que_id']);
				let form_tag = document.createElement('form');
				form_tag.setAttribute('autocomplete', 'off');
				let question_title = json['vote']['que_list'][i]['que'];
				let question_title_tag = document.createElement('h2');
				question_title_tag.append(question_title);
				form_tag.append(question_title_tag);
				let question_id = json['vote']['que_list'][i]['que_id'];
				let question_type = json['vote']['que_list'][i]['que_type'];
				let question_type_name;
				if (question_type == 0){
					question_type_name = "checkbox";
					form_tag.classList.add("ac-custom", "ac-checkbox", "ac-checkmark");
				} else if (question_type == 1){
					question_type_name = "radio";
					form_tag.classList.add("ac-custom", "ac-radio", "ac-circle");
				} else {
					question_type_name = "answer";
					form_tag.classList.add("ac-custom");
				}
				if (question_type == 0) {
					let answer_ul = document.createElement('ul');
					for (let j = 0 ; j < json['vote']['que_list'][i]['select'].length; j ++){
						let answer_li = document.createElement('li');
						let answer_input = document.createElement('input');
						answer_input.setAttribute('type', question_type_name);
						answer_input.setAttribute('id', 'cb'+(i*1+1)+'_'+(j*1+1));
						let select_content = json['vote']['que_list'][i]['select'][j]['select_content'];
						let select_id = json['vote']['que_list'][i]['select'][j]['select_id'];
						let answer_label = document.createElement('label');
						answer_label.setAttribute('for', 'cb'+(i*1+1)+'_'+(j*1+1));
						answer_label.setAttribute('alt', select_id);
						answer_label.append(select_content);
						answer_li.append(answer_input, answer_label);
						answer_ul.append(answer_li);
					}
					form_tag.append(answer_ul);
					section.append(form_tag);
				} else if(question_type == 1) {
					let answer_ul = document.createElement('ul');
					for (let j = 0 ; j < json['vote']['que_list'][i]['select'].length; j ++){
						let answer_li = document.createElement('li');
						let answer_input = document.createElement('input');
						answer_input.setAttribute('type', question_type_name);
						answer_input.setAttribute('id', 'r'+(i*1+1)+'_'+(j*1+1));
						answer_input.setAttribute('name', 'r'+i);
						let select_content = json['vote']['que_list'][i]['select'][j]['select_content'];
						let select_id = json['vote']['que_list'][i]['select'][j]['select_id'];
						let answer_label = document.createElement('label');
						answer_label.setAttribute('for', 'r'+(i*1+1)+'_'+(j*1+1));
						answer_label.setAttribute('alt', select_id);
						answer_label.append(select_content);
						answer_li.append(answer_input, answer_label);
						answer_ul.append(answer_li);
					}
					form_tag.append(answer_ul);
					section.append(form_tag);
				} else {
					let answer_input = document.createElement('input');
					answer_input.classList.add('M_vote_answer_type_answer');
					answer_input.setAttribute('type', 'text');
					answer_input.setAttribute('autocomplete', 'off');
					answer_input.setAttribute('maxlength', '100');
					answer_input.setAttribute('placeholder', "답변을 입력해주세요.");
					form_tag.append(answer_input);
					section.append(form_tag);
				}
				let question_bottom_line = document.createElement('div');
				question_bottom_line.classList.add("M_vote_body_line");
				$('#M_vote_que_target').append(section);
				if ( i != que_length - 1){
					$('#M_vote_que_target').append(question_bottom_line);
				}
			}
			vote_init_finally();
		}
		else {
			snackbar("일시적인 오류로 정보를 가져오지 못하였습니다.");
		}
	});
}

function empty_post_info(){
	$('#M_vote_que_target').empty();
	$('#M_post_author').empty();
	$('#M_post_start_date').empty();
	$('#M_post_end_date').empty();
	$('#M_post_top_title').empty();
	$('#M_vote_picture_container').removeClass('display_none_important');
	$('#M_post_body').empty();
	$('#M_post_body_icons_data').empty();
	$('#M_vote_picture').attr('src', '#');
}


// 모바일
var filter = "win16|win32|win64|mac|macintel";
if ( navigator.platform ) { //mobile
	if ( filter.indexOf( navigator.platform.toLowerCase() ) < 0 ) {
		$('#M_post_user_comment_input').focus(function() {
			let mobile_seletor = navigator.platform.toLowerCase();
			//IOS
			if (mobile_seletor.indexOf("iphone")>-1||mobile_seletor.indexOf("ipad")>-1||mobile_seletor.indexOf("ipod")>-1){
				$('#M_user_post_modal_container').animate({scrollTop : $('#M_user_post_modal_container').height() + $('#M_user_post_modal_container').height()/100*68}, 400);
			} else {	//ANDROID
				$('#M_post_user_comment_container').css("position", "fixed");
				$('#M_post_user_comment_container').css("padding", "10px 10px 0px 10px");
			}
		});
		$('#M_post_user_comment_input').blur(function() {
			if (comment_double_check == 1){
				let comment_id = $('#M_post_user_comment_input').attr('alt');
				$('#M_post_user_comment_input').removeAttr("alt");
				comment_double_check = 0;
				$('div[alt=comment_'+comment_id+']').removeAttr('style');
				$('div[alt=comment_'+comment_id+']').removeClass("comment_check");
			}
		});
	} else {	//pc
		$('#M_post_user_comment_input').blur(function(){
			if (comment_double_check == 1){
				let comment_id = $('#M_post_user_comment_input').attr('alt');
				$('#M_post_user_comment_input').removeAttr("alt");
				comment_double_check = 0;
				$('div[alt=comment_'+comment_id+']').removeAttr('style');
				$('div[alt=comment_'+comment_id+']').removeClass("comment_check");
			}
		});
	}
}

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

function image_modal_close(){
	$('#M_image_modal_background').addClass('fadeOut');
	$('#M_image_modal_background').removeClass('fadeIn');
	setTimeout(function(){
  		$('#M_image_modal_background').addClass('display_none');
  		is_image_modal_open = 0;
  	}, 400);
	$('html').scrollTop(now_postmodal_top);
}

//포스트 작성 함수
function post_write() {
	now_postmodal_top = $(window).scrollTop();
	postmodal_close(1);
	$('#M_user_post_modal_background_fixed').css("height", $(window).height() + 100);
	$('#M_user_post_modal_background_fixed').css('position', "fixed");
	$('#M_user_post_modal_background_fixed').removeClass('display_none');
	$('#M_user_post_modal_background_fixed').removeClass('fadeOut');
	$('#M_user_post_modal_background_fixed').addClass('fadeIn');
	$('html, body').css({'overflow': 'hidden'});
	$('html, body').addClass('M_modal_open_fixed');
	$('#M_user_post_modal_container_fixed').removeClass('fadeOutDown');
	$('#M_user_post_modal_container_fixed').addClass('fadeInUp');
	$('#M_user_post_modal_container_fixed').removeClass('display_none');
}

//포스트 수정 함수
function post_modify() {
	snackbar("설문조사는 수정할 수 없습니다.");
	return;
}

//포스트 삭제 함수
function post_delete() {
	let post_id = $('#M_user_post_modal_container').attr('alt').split('_')[1]*1;
	let token = localStorage.getItem('modakbul_token');
	if (token != null){
		let a_jax = A_JAX(TEST_IP+'vote_delete/'+post_id, "GET", token, null);
		$.when(a_jax).done(function(){
			let json = a_jax.responseJSON;
			if (json['result'] == "success"){
				snackbar("설문조사 삭제를 성공하였습니다.");
				postmodal_close(1);
				location.reload();
			} else if (json['result'] == "do not access") {
				snackbar("권한이 없습니다.");
			} else {
				snackbar("설문조사 삭제를 실패하였습니다.");
			}
		});
	} else {
		snackbar("권한이 없습니다.");
	}
}
/*
$(function(){
	$('#files-upload').MultiFile({
		max: 1, //업로드 최대 파일 갯수 (지정하지 않으면 무한대)
		maxsize: 51200,  //전체 파일 최대 업로드 크기
		STRING: { //Multi-lingual support : 메시지 수정 가능
		    toomuch: "업로드할 수 있는 최대크기를 초과하였습니다.", 
		    toomany: "업로드할 수 있는 최대 갯수는 $max개 입니다."
		},
		list:"#files-upload" //파일목록을 출력할 요소 지정가능
	});
});
*/
function post_write_accept() {
	if ($('#M_post_fixed_title_input').val() == ""){
		snackbar("제목을 입력해주세요.");
		$('#M_user_post_modal_container_fixed').animate({scrollTop : 0}, 400);
		$('#M_post_fixed_title_input').focus();
		return;
	} else if ($('#M_vote_fixed_body_input').val() == ""){
		snackbar("내용을 입력해주세요.");
		$('#M_user_post_modal_container_fixed').animate({scrollTop : 200}, 400);
		$('#M_vote_fixed_body_input').focus();
		return;
	} else if ($('#M_vote_fixed_body_input').val().length >= 50000){
		snackbar("작성 범위를 초과하였습니다.");
		$('#M_user_post_modal_container_fixed').animate({scrollTop : 200}, 400);
		$('#M_vote_fixed_body_input').focus();
		return;
	} else if ($('#M_vote_end_date_slider').text() == ""){
		snackbar("마감 날짜를 선택해주세요.");
		return;
	}
	let token = localStorage.getItem('modakbul_token');
	let vote = {};
	let send_data = new FormData();
	let que_list = [];
	var M_files = document.getElementById('files_upload').files;
	var M_file = M_files[0];

	vote["title"] = $('#M_post_fixed_title_input').val();
	vote["content"] = $('#M_vote_fixed_body_input').val();
	vote["end_date"] = $('#M_vote_end_date_slider').text().slice(0, 10);

	let question_containers = $('#M_vote_question_cotainer_target').find('div.M_vote_question_container');
	for (let i = 0; i < question_containers.length; i++){
		let que_list_element = {};
		let question_container_type = $(question_containers[i]).attr('box_type');
		let question_container_inputs = $(question_containers[i]).find('input');
		let question_container_input_title = $(question_container_inputs[0]).val();
		if (question_container_input_title == ""){
			snackbar("질문을 모두 입력해주세요.");
			$('#M_user_post_modal_container_fixed').animate({scrollTop : 500}, 400);
			question_container_inputs[0].focus();
			return;
		} else {
			que_list_element['que'] = question_container_input_title;
		}
		
		if (question_container_type == "checkbox"){
			que_list_element['que_type'] = 0;
		} else if (question_container_type == "radio"){
			que_list_element['que_type'] = 1;
		} else if (question_container_type == "answer"){
			que_list_element['que_type'] = 2;
		} else {
			snackbar("잘못된 질문형태 입니다.");
			return;
		}

		if (question_container_type == 'checkbox' || question_container_type == "radio"){
			let que_container_select = [];
			for (let j = 1; j < question_container_inputs.length; j++){
				let number = $(question_container_inputs[j]).prev().text()*1;
				let question_container_input_select = $(question_container_inputs[j]).val();
				if (question_container_input_select == ""){
					snackbar("선택지를 모두 입력해주세요.");
					$('#M_user_post_modal_container_fixed').animate({scrollTop : 500}, 400);
					question_container_inputs[j].focus();
					return;
				} else {
					que_container_select.push(question_container_input_select);
				}
			}
			que_list_element['select'] = que_container_select;
		} 
		que_list.push(que_list_element);
	}
	vote['que_list'] = que_list;

	send_data.append('vote', JSON.stringify(vote));
	send_data.append('file', M_file);

	let a_jax = A_JAX_FILE(TEST_IP+"vote_upload", "POST", token, send_data);
	$.when(a_jax).done(function(){
		let json = a_jax.responseJSON;
		if (json['result'] == "success"){
			snackbar("설문조사를 성공적으로 업로드하였습니다.");
			post_write_cancel();
			location.reload();
      	}
      	else if (json['result'] == 'bad request'){
      	 	snackbar("설문조사 업로드를 실패하였습니다.");
      	}
      	else if (json['result'] == 'fail_save_file'){
      		snackbar("설문조사 업로드를 실패하였습니다.");
      	}
      	else if (json['result'] == "wrong_file"){
      		snackbar("잘못된 파일 확장자명입니다.");
      	} 
      	else if (json['result'] == "you are not admin"){
      		snackbar("권한이 없습니다.");
      	}
      	else if (json['result'] == "unavailable word"){
    	  		snackbar("내용에 욕설이 들어가있습니다.");
    	  	}
      	else {
      		snackbar("설문조사 업로드를 실패하였습니다!");
      	}
	});
}




function post_write_cancel() {
	is_postmodal_fixed_open = 0;
	$('#M_post_fixed_title_input').val("");
	$('#M_vote_fixed_body_input').val("");
	$('#files_upload').val("");
	$('#M_file_route').empty();
	$('#M_vote_question_cotainer_target').empty();
	let output = '<div class="M_vote_question_container" box_type="checkbox">\
					<input type="text" class="M_vote_write_title" placeholder="질문을 입력해주세요." maxlength="100">\
					<div class="M_vote_write_trash" onclick="vote_write_question_delete($(this))"><i class="fas fa-trash-alt" style="position: relative; float: right;"></i></div>\
					<span class="M_vote_write_answer_number">1</span>\
					<input type="text" class="M_vote_write_answer_input" placeholder="선택지를 입력해주세요." maxlength="100">\
					<div class="M_vote_write_answer_add_container">\
						<i class="far fa-check-square M_vote_write_answer_plus"></i>\
						<div class="M_vote_write_answer_input" onclick="vote_write_question_select_add($(this))" alt="1">선택지를 추가하기</div>\
					</div>\
				</div>';
	$('#M_vote_question_cotainer_target').append(output);
	history.replaceState(null, null, "#list");
	$('#M_user_post_modal_background_fixed').addClass('fadeOut');
	$('#M_user_post_modal_background_fixed').removeClass('fadeIn');
	$('#M_user_post_modal_container_fixed').addClass("fadeOutDown");
	$('#M_user_post_modal_container_fixed').removeClass('fadeInUp');
	setTimeout(function(){
  		$('#M_user_post_modal_container_fixed').addClass("display_none");
  		$('#M_user_post_modal_background_fixed').addClass('display_none');
  	}, 400);
	$('html, body').removeAttr("style");
	$('html, body').removeClass('M_modal_open_fixed');
	$('html').scrollTop(now_postmodal_top);
}

//설문조사 accept
function vote_send() {
	let token = localStorage.getItem('modakbul_token');
	let vote_id = $('#M_user_post_modal_container').attr('alt').split('_')[1]*1;
	let send_data = {};
	let question_list = $('#M_vote_que_target').find('section').toArray();
	let question_len = question_list.length;
	let ans_list = [];
	for (let i = 0; i < question_len; i++){
		let question_dict = {};
		let question_type;
		if ($(question_list[i].getElementsByTagName("form")).hasClass("ac-checkbox") === true){
			question_type = 0;
		} else if ($(question_list[i].getElementsByTagName("form")).hasClass("ac-radio") === true){
			question_type = 1;
		} else {
			question_type = 2;
		}
		question_dict["que_id"] = $(question_list[i]).attr('alt').split('_')[1]*1;
		question_dict["que_type"]  = question_type;
		if (question_type == 0 || question_type == 1) {	
			let question_answer_list = $(question_list[i]).find("li");
			let question_answer_check_list = [];
			let is_check = 0;
			for (let j = 0; j < question_answer_list.length; j++){
				if ($(question_answer_list[j]).find("path").length != 0){
					question_answer_check_list.push($(question_answer_list[j]).find("label").attr('alt'));
				} else {
					is_check += 1;
				}
				if (is_check == question_answer_list.length){
					snackbar("질문에 모두 답해주세요.");
					$('#M_user_post_modal_container').animate({scrollTop : 300}, 400);
					return;
				}
			}
			question_dict["ans"] = question_answer_check_list;
		} else {
			if ($(question_list[i]).find('input').val() == ""){
				snackbar("질문에 모두 답해주세요.");
				$('#M_user_post_modal_container').animate({scrollTop : 300}, 400);
				return;
			}
			question_dict["ans"] = $(question_list[i]).find('input').val();
		}
		ans_list.push(question_dict);
	}
	send_data["vote_id"] = vote_id;
	send_data["ans_list"] = ans_list;

	let output = new FormData();
	output.append('answer', JSON.stringify(send_data));

	let a_jax = A_JAX_FILE(TEST_IP+"vote_answer", "POST", token, output);
	$.when(a_jax).done(function(){
		let json = a_jax.responseJSON;
		if (json['result'] == 'success'){
			snackbar("설문조사 완료!");
			postmodal_close();
			setTimeout(function() {location.reload()}, 400);
		} else if (json['result'] == "bad request") {
			snackbar("로그인을 다시 해주세요.");
			return;
		} else if (json['result'] == "already_vote"){
			snackbar("이미 투표한 설문조사입니다.");
		} else if (json['result'] == "admin can not vote"){
			snackbar("관리자는 투표에 참여할 수 없습니다.");
		} else if (json['result'] == "unavailable word"){
    		snackbar("내용에 욕설이 들어가있습니다.");
    	} else {
		 	snackbar("일시적인 오류로 정보를 보내지 못하였습니다.");
		 }
	});
}

function vote_write_question_delete(tag) {
	tag.parent('div').remove();
}

function vote_write_question_select_add(tag) {
	let now_num = tag.attr('alt')*1;
	now_num += 1;
	tag.attr('alt', now_num);
	let answer_number = document.createElement('span');
	answer_number.classList.add("M_vote_write_answer_number");
	answer_number.append(now_num);
	let answer_input = document.createElement('input');
	answer_input.setAttribute('type', 'text');
	answer_input.setAttribute('placeholder', '선택지를 입력해주세요.');
	answer_input.setAttribute('maxlength', '100');
	answer_input.classList.add("M_vote_write_answer_input");
	tag.parent().before($(answer_number));
	tag.parent().before($(answer_input));
}

function vote_write_question_add_checkbox(tag) {
	let output = '<div class="M_vote_question_container" box_type="checkbox">\
					<input type="text" class="M_vote_write_title" placeholder="질문을 입력해주세요." maxlength="100">\
					<div class="M_vote_write_trash" onclick="vote_write_question_delete($(this))"><i class="fas fa-trash-alt" style="position: relative; float: right;"></i></div>\
					<span class="M_vote_write_answer_number">1</span>\
					<input type="text" class="M_vote_write_answer_input" placeholder="선택지를 입력해주세요." maxlength="100">\
					<div class="M_vote_write_answer_add_container">\
						<i class="far fa-check-square M_vote_write_answer_plus"></i>\
						<div class="M_vote_write_answer_input" onclick="vote_write_question_select_add($(this))" alt="1">선택지를 추가하기</div>\
					</div>\
				</div>';
	tag.parent('div').prev().append(output);
}

function vote_write_question_add_radio(tag) {
	let output = '<div class="M_vote_question_container" box_type="radio">\
					<input type="text" class="M_vote_write_title" placeholder="질문을 입력해주세요." maxlength="100">\
					<div class="M_vote_write_trash" onclick="vote_write_question_delete($(this))"><i class="fas fa-trash-alt" style="position: relative; float: right;"></i></div>\
					<span class="M_vote_write_answer_number">1</span>\
					<input type="text" class="M_vote_write_answer_input" placeholder="선택지를 입력해주세요." maxlength="100">\
					<div class="M_vote_write_answer_add_container">\
						<i class="far fa-dot-circle M_vote_write_answer_plus"></i>\
						<div class="M_vote_write_answer_input" onclick="vote_write_question_select_add($(this))" alt="1">선택지를 추가하기</div>\
					</div>\
				</div>';
	tag.parent('div').prev().append(output);
}

function vote_write_question_add_answer(tag) {
	let output = '<div class="M_vote_question_container" box_type="answer">\
					<input type="text" class="M_vote_write_title" placeholder="질문을 입력해주세요." maxlength="100">\
					<div class="M_vote_write_trash" onclick="vote_write_question_delete($(this))"><i class="fas fa-trash-alt" style="position: relative; float: right;"></i></div>\
					<input type="text" class="M_vote_write_answer_input_answer" value="단답형 양식입니다." maxlength="100" readonly>\
				</div>';
	tag.parent('div').prev().append(output);
}

/*업로드 파일 관리*/
$("input[type=file]").change(function () {
    let fileInput = document.getElementById("files_upload");
    let files = fileInput.files;
    let file;
    let string = "";
    if (files.length > 1){
    	alert("사진 개수는 하나만 올려주세요!");
    	$('#files_upload').val('');
    	return;
    }
   	if (jQuery.inArray(files[0]['name'].split(".")[(files[0]['name'].split(".").length-1)], img_set) == -1){
   		alert("사진 파일만 올려주세요!");
   		$('#files_upload').val('');
   		return;
   	}
    for (let i = 0; i < files.length; i++) {
        file = files[i];
        string += file.name;
        string += " / ";
    }
    $('#M_file_route').empty();
    $('#M_file_route').append(string);
});

//관리자일 경우 control button 보여주기
$(window).ready(function () {
	if (localStorage.getItem('modakbul_token') == null){
      	return;
   	}
	let a_jax = A_JAX(TEST_IP+"get_userinfo", "GET",  null, null);
	$.when(a_jax).done(function(){
		var json = a_jax.responseJSON;
		if (json['result'] == "success"){
			if (json['user_id'] == 'admin'){
				$('#M_menu_button_container').removeClass('display_none_important');
			}
		}
	});
});



/*
//디버그 확인용 코드
for (var value of send_data.values()) {
   	console.log(value); 
}
(JSON.stringify(value))
*/