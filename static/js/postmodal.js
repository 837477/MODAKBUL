//라벨, 이름, 시간, 제목, 본문, 조회수, 공감수, 댓글, 첨부파일, 사진, 태그
var is_postmodal_open = 0;
var is_postmodal_fixed_open = 0;
var now_postmodal_top = 0;
var is_image_modal_open = 0;
var is_post_like = 0;
var img_set = ['png', 'jpg', 'jpeg', 'gif', 'bmp'];
var file_path = "../static/files/";
var is_post_modify = 0;
var is_post_property = 0;
function postpage_open(get_post_href, get_post_id){
	let a_jax = A_JAX(TEST_IP+"view_up/"+get_post_id, "GET", null, null);
	window.open(get_post_href, '_blank');
}

function postmodal_open(get_post_id){
	let searchParams = new URLSearchParams(window.location.search);
	let request_board = searchParams.get('type');
	is_post_like = 0;
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

//마우스 드래그로 스크롤할 수 있는 함수  = 이미지 container
const slider = document.querySelector('#M_post_body_image_container');

let isDown = false;
let startX;
let scrollLeft;
slider.addEventListener('mousedown', (e) => {
  isDown = true;
  slider.classList.add('active');
  startX = e.pageX - slider.offsetLeft;
  scrollLeft = slider.scrollLeft;
});
slider.addEventListener('mouseleave', () => {
  isDown = false;
  slider.classList.remove('active');
});
slider.addEventListener('mouseup', () => {
  isDown = false;
  slider.classList.remove('active');
});
slider.addEventListener('mousemove', (e) => {
  if(!isDown) return;
  e.preventDefault();
  const x = e.pageX - slider.offsetLeft;
  const walk = (x - startX) * 3; //scroll-fast
  slider.scrollLeft = scrollLeft - walk;
});
//마우스 드래그로 스크롤할 수 있는 함수  = 첨부파일 container
const slider2 = document.querySelector('#M_post_body_attachment_container');
let isDown2 = false;
let startX2;
let scrollLeft2;
slider2.addEventListener('mousedown', (e) => {
  isDown2 = true;
  slider2.classList.add('active');
  startX2 = e.pageX - slider.offsetLeft;
  scrollLeft2 = slider.scrollLeft;
});
slider2.addEventListener('mouseleave', () => {
  isDown2 = false;
  slider2.classList.remove('active');
});
slider2.addEventListener('mouseup', () => {
  isDown2 = false;
  slider2.classList.remove('active');
});
slider2.addEventListener('mousemove', (e) => {
  if(!isDown2) return;
  e.preventDefault();
  const x = e.pageX - slider2.offsetLeft;
  const walk2 = (x - startX2) * 3; //scroll-fast
  slider2.scrollLeft = scrollLeft2 - walk2;
});


function comment_enter() {
	if (window.event.keyCode == 13) {
		let is_double_comment = 0;
		let is_anony = 0;
		if ($('input:checkbox[id="M_post_user_comment_anony"]').is(":checked") == true){
			is_anony = 1;
		}
		let token = localStorage.getItem('modakbul_token');
		if (token == null){
			snackbar("로그인을 해주세요.");
			return;
		}
		if ($('#M_post_user_comment_input').attr('alt') != null){
			is_double_comment = $('#M_post_user_comment_input').attr('alt');
		}
		let send_data = new FormData();
		send_data.append('post_id', $('#M_user_post_modal_container').attr('alt').split('_')[1]*1);
		send_data.append('comment', $("#M_post_user_comment_input").val());
		send_data.append('anony', is_anony);
		send_data.append('comment_id', is_double_comment*1);
		a_jax = A_JAX_FILE(TEST_IP+"comment_upload", "POST", token, send_data);
		$.when(a_jax).done(function(){
			var json = a_jax.responseJSON;
			if (json['result'] == "success"){
				var a_jax_user = A_JAX(TEST_IP+"get_userinfo", "GET", token, null);
				$.when(a_jax_user).done(function(){
					json = a_jax_user.responseJSON;
					if (json['result'] == "success"){
						$("#M_post_user_comment_input").blur();
						user_comments_id = [];
						for (let i = 0; i< json['user_comments'].length; i++){
							user_comments_id.push(json['user_comments'][i]);
						}
						empty_post_info();
						let get_post_id =$('#M_user_post_modal_container').attr('alt').split('_')[1]*1;
						get_post_info(get_post_id);
					}
					else {
						snackbar("일시적인 오류로 정보를 가져오지 못하였습니다.");
					}
				});
			}
			else if (json['result'] == "unavailable word"){
    	  		snackbar("내용에 욕설이 들어가있습니다.");
    	  	}
			else if (json['result'] == "bad request"){
				snackbar("다시 로그인해주세요.");
			}
			else {
				snackbar("일시적인 오류로 정보를 보내지 못하였습니다.");
			}
		});
		$("#M_post_user_comment_input").val("");
    }
}

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
	if (token != null){
		var a_jax = A_JAX(TEST_IP+"get_post/"+get_post_id, "GET", token, null);
	} else {
		var a_jax = A_JAX(TEST_IP+"get_post/"+get_post_id, "GET", null, null);
	}
	$.when(a_jax).done(function(){
		var json = a_jax.responseJSON;
		if (json['result'] == "success"){
			is_post_property = json['property']*1;
			$('#M_user_post_modal_container').attr('alt', "post_"+json['post']['post_id']);
			$('#M_post_profile_color').css("background-color", json['post']['author_color']);
			$('#M_post_author').append(json['post']['author_name']);
			$('#M_post_time').append("| "+json['post']['post_date']); 	// 날짜 수정
			$('#M_post_top_title').append(json['post']['post_title']);
			$('#M_post_body').append(json['post']['post_content']);
			let files = json['files'];
			let img_files = [];
			let attachment_files = [];
			for (let i = 0 ; i < files.length; i++){
				let file_name = files[i].split('.');
				if (img_set.includes(file_name[file_name.length - 1])){
					img_files.push(files[i]);
				} else {
					attachment_files.push(files[i]);
				}
			}
			let image_container = $('#M_post_body_image_container');
			if (img_files.length != 0) {
				image_container.css('display', "inline-block");
				for (let i = 0; i < img_files.length; i++){
					let img_content = document.createElement('div');
					img_content.classList.add("M_post_body_content");
					let img_tag = document.createElement('img');
					img_tag.classList.add('M_post_body_image_content');
					img_tag.setAttribute('src', file_path+img_files[i]);
					img_tag.setAttribute('onclick', "image_modal_open(this);");
					img_content.append(img_tag);
					image_container.append(img_content);
				}
			} else {
				image_container.css('display', "none");
			}
			let attachment_container = $('#M_post_body_attachment_container');
			if (attachment_files.length != 0){
				attachment_container.css('display', "inline-block");
				for (let i = 0; i < attachment_files.length; i++){
					let attachment_content = document.createElement('div');
					attachment_content.classList.add("M_post_body_content", "M_post_body_content_attachment");
					attachment_content.setAttribute('onclick', "attachment_donwload('"+attachment_files[i]+"')");
					let attachment_icon = document.createElement('i');
					attachment_icon.classList.add('fas', 'fa-paperclip', 'M_post_body_content_attachment_icon');
					let attachment_title = document.createElement('span');
					attachment_title.classList.add('M_post_body_attach_title');
					let attachment_title_date = attachment_files[i].split('_')[0];
					let attachment_title_info = attachment_files[i].slice(attachment_title_date.length + 1);
					attachment_title.append(attachment_title_info);
					attachment_content.append(attachment_icon, attachment_title);
					attachment_container.append(attachment_content);
				}
			} else {
				attachment_container.css('display', "none");
			}
			$('#M_post_url_copy').attr('alt', json['post']['post_id']);
			$('#M_post_body_icons_view').append(json['post']['post_view']);
			$('#M_post_body_icons_like').append(json['post']['like_cnt']);
			$('#M_post_body_icons_comment').append(json['post']['comment_cnt']);
			//댓글
			var comment_target = $('#comment_target');
			for (let i = 0; i < json['comment'].length; i++){
				let container = document.createElement('div');
				container.setAttribute('alt', 'comment_'+json['comment'][i]['comment_id']);
				container.classList.add('M_post_comment_container');
				let top_container = document.createElement('div');
				top_container.classList.add('M_comment_top_container');
				let comment_color = document.createElement('div');
				comment_color.classList.add('M_comment_profile_color');
				comment_color.style.backgroundColor = json['comment'][i]['author_color'];
				let comment_author = document.createElement('div');
				comment_author.classList.add('M_comment_author');
				comment_author.append(json['comment'][i]['author_name']);
				let comment_time = document.createElement('div');
				comment_time.classList.add('M_comment_time');
				comment_time.append("| "+json['comment'][i]['comment_date']);
				top_container.append(comment_color, comment_author, comment_time);
				let comment_double_icon = document.createElement('i');
				comment_double_icon.classList.add("fas", "fa-comment", 'M_comment_double');
				comment_double_icon.setAttribute('onclick', "double_comment_button_check("+json['comment'][i]['comment_id']+")");
				if (json.hasOwnProperty('admin')){
					let comment_trash_icon = document.createElement('i');
					comment_trash_icon.classList.add("fas", "fa-trash-alt", 'M_comment_double');
					comment_trash_icon.setAttribute('onclick', "comment_trash_button("+json['comment'][i]['comment_id']+")");
					top_container.append(comment_trash_icon);
				}
				else if (user_comments_id.includes(json['comment'][i]['comment_id'])){
					let comment_trash_icon = document.createElement('i');
					comment_trash_icon.classList.add("fas", "fa-trash-alt", 'M_comment_double');
					comment_trash_icon.setAttribute('onclick', "comment_trash_button("+json['comment'][i]['comment_id']+")");
					top_container.append(comment_trash_icon);
				}	
				top_container.append(comment_double_icon);
				container.append(top_container);
				let comment_body = document.createElement('div');
				comment_body.classList.add("M_comment_body");
				comment_body.append(json['comment'][i]['comment']);
				let comment_line = document.createElement('div');
				comment_line.classList.add("M_post_comment_line");
				container.append(comment_body, comment_line);
				comment_target.append(container);
				for (let j = 0; j < json['comment'][i]['double_comment'].length; j++){
					let d_container = document.createElement('div');
					d_container.setAttribute('alt', 'comment_'+json['comment'][i]['double_comment'][j]['comment_id']);
					d_container.classList.add('M_post_double_comment_container');
					let d_top_container = document.createElement('div');
					d_top_container.classList.add('M_comment_top_container');
					let d_comment_color = document.createElement('div');
					d_comment_color.classList.add('M_comment_profile_color');
					d_comment_color.style.backgroundColor = json['comment'][i]['double_comment'][j]['author_color'];
					let d_comment_author = document.createElement('div');
					d_comment_author.classList.add('M_comment_author');
					d_comment_author.append(json['comment'][i]['double_comment'][j]['author_name']);
					let d_comment_time = document.createElement('div');
					d_comment_time.classList.add('M_comment_time');
					d_comment_time.append("| "+json['comment'][i]['double_comment'][j]['comment_date']);
					if (json.hasOwnProperty('admin')){
						let d_comment_trash_icon = document.createElement('i');
						d_comment_trash_icon.classList.add("fas", "fa-trash-alt", 'M_comment_double');
						d_comment_trash_icon.setAttribute('onclick', "comment_trash_button("+json['comment'][i]['double_comment'][j]['comment_id']+")");
						d_top_container.append(d_comment_trash_icon);
					}
					else if (user_comments_id.includes(json['comment'][i]['double_comment'][j]['comment_id'])){
						let d_comment_trash_icon = document.createElement('i');
						d_comment_trash_icon.classList.add("fas", "fa-trash-alt", 'M_comment_double');
						d_comment_trash_icon.setAttribute('onclick', "comment_trash_button("+json['comment'][i]['double_comment'][j]['comment_id']+")");
						d_top_container.append(d_comment_trash_icon);
					}
					d_top_container.append(d_comment_color, d_comment_author, d_comment_time);
					d_container.append(d_top_container);
					let d_comment_body = document.createElement('div');
					d_comment_body.classList.add("M_comment_body");
					d_comment_body.append(json['comment'][i]['double_comment'][j]['comment']);
					let d_comment_line = document.createElement('div');
					d_comment_line.classList.add("M_post_comment_line");
					d_container.append(d_comment_body, d_comment_line);
					comment_target.append(d_container);
				}
			}
			if (user_like_posts_id.includes(json['post']['post_id'])){
				is_post_like = 1;
				$('#M_post_top_heart').css({"color":"red", "text-shadow": "0px 0px 10px red"});
			}
		}
		else if (json['result'] == 'do not access'){
			snackbar("비밀글입니다.");
			postmodal_close(1);
		}
		else {
			snackbar("일시적인 오류로 정보를 가져오지 못하였습니다.");
		}
	});
}

function empty_post_info(){
	$('#M_post_author').empty();
	$('#M_post_time').empty();
	$('#M_post_top_title').empty();
	$('#M_post_body').empty();
	$('#M_post_body_icons_view').empty();
	$('#M_post_body_icons_like').empty();
	$('#M_post_body_icons_comment').empty();
	$('#M_post_body_image_container').empty();
	$('#M_post_body_attachment_container').empty();
	$('#comment_target').empty();
	is_post_like = 0;
	$('#M_post_top_heart').removeAttr('style');
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

var comment_double_check = 0;
function double_comment_button_check(comment_id) {
	comment_double_check = 1;
	$('div[alt=comment_'+comment_id+']').addClass("comment_check");
	if (localStorage.getItem('modakbul_theme') === 'dark') {
        $('div[alt=comment_'+comment_id+']').css("background-color", "#41464a");
    } else {
        $('div[alt=comment_'+comment_id+']').css("background-color", "#f5f6fa");
    }
    $('#M_post_user_comment_input').attr('alt', comment_id);
	$('#M_post_user_comment_input').focus();
}


function post_like_button() {
	if (is_post_like == 0) {
		if (localStorage.getItem('modakbul_token') == null){
			snackbar("로그인을 해주세요!");
			return;
		}
		is_post_like = 1;
		let now_like_cnt = $('#M_post_body_icons_like').text();
		$('#M_post_body_icons_like').empty();
		$('#M_post_body_icons_like').append(now_like_cnt*1 + 1);
		let token = localStorage.getItem('modakbul_token');
		let post_id = $('#M_user_post_modal_container').attr('alt').split('_')[1]*1;
		a_jax = A_JAX(TEST_IP+'post_like_up/'+post_id, "GET", token, null);
		$('#M_post_top_heart').css({"color":"red", "text-shadow": "0px 0px 10px red"});
		user_like_posts_id.push(post_id);
	} else {
		is_post_like = 0;
		let now_like_cnt = $('#M_post_body_icons_like').text();
		$('#M_post_body_icons_like').empty();
		$('#M_post_body_icons_like').append(now_like_cnt*1 - 1);
		let token = localStorage.getItem('modakbul_token');
		let post_id = $('#M_user_post_modal_container').attr('alt').split('_')[1]*1;;
		a_jax = A_JAX(TEST_IP+'post_like_down/'+post_id, "GET", token, null);
		$('#M_post_top_heart').removeAttr('style');
		let post_id_index = user_like_posts_id.indexOf(post_id); 
		if (post_id_index > -1) {
			user_like_posts_id.splice(post_id_index, 1);
		}
	}
}


function comment_trash_button(comment_id) {
	if (localStorage.getItem('modakbul_token') == null){
		snackbar('잘못된 접근입니다.');
		return;
	} else {
		if ($('#M_user_content_number').text() == 'admin'){
			let token = localStorage.getItem('modakbul_token');
			a_jax = A_JAX(TEST_IP+"comment_delete/"+comment_id, "GET", token, null);
			$.when(a_jax).done(function(){
				json = a_jax.responseJSON;
				if (json['result'] == 'success'){
					snackbar("댓글을 삭제하였습니다.");
					empty_post_info();
					let get_post_id =$('#M_user_post_modal_container').attr('alt').split('_')[1]*1;
					get_post_info(get_post_id);
				} else if (json['result'] == 'bad request'){
					snackbar("권한이 없습니다.");
				} else {
					snackbar("잘못된 접근입니다.");
				}
			});
		}
		else if (user_comments_id.includes(comment_id)){
			let token = localStorage.getItem('modakbul_token');
			a_jax = A_JAX(TEST_IP+"comment_delete/"+comment_id, "GET", token, null);
			$.when(a_jax).done(function(){
				json = a_jax.responseJSON;
				if (json['result'] == 'success'){
					snackbar("댓글을 삭제하였습니다.");
					empty_post_info();
					let get_post_id =$('#M_user_post_modal_container').attr('alt').split('_')[1]*1;
					get_post_info(get_post_id);
				} else if (json['result'] == 'bad request'){
					snackbar("권한이 없습니다.");
				} else {
					snackbar("잘못된 접근입니다.");
				}
			});
		} else {
			snackbar('잘못된 접근입니다.');
			return;
		}
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

//file download function
function attachment_donwload(file){
	let date = file.split('_')[0];
	let title = file.slice(date.length + 1);
	var element = document.createElement('a');
	element.setAttribute('href', '../static/files/'+file);
	element.setAttribute('download', title);
	element.style.display = 'none';
	document.body.appendChild(element);
	element.click();
	document.body.removeChild(element);
}

//클립보드 복사 함수
function clipboardCopy(tag) {
	let post_id = tag.getAttribute('alt');
	var clipboard_textarea = document.createElement('textarea');
	clipboard_textarea.setAttribute('id', 'clipboard_copy');
	clipboard_textarea.value = TEST_IP+"v#"+post_id;
	clipboard_textarea.style.zIndex = "-3000";
	document.body.appendChild(clipboard_textarea);
	clipboard_textarea.select();
	document.execCommand("copy");
	document.getElementById('clipboard_copy').blur();
	snackbar("URL 복사완료!");
	$('textarea').remove('#clipboard_copy');
}

//포스트 작성 함수
function post_write() {
	token = localStorage.getItem('modakbul_token');
	if (token == null){
		snackbar("로그인을 해주세요.");
		return;
	}
	now_postmodal_top = $(window).scrollTop();
	postmodal_close(1);
	is_postmodal_fixed_open = 1;
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
	is_post_modify = 1;
	let token = localStorage.getItem('modakbul_token');
	if (token == null){
		snackbar("로그인을 해주세요.");
		post_write_cancel();
		return;
	}
	if (is_post_property == 0){
		snackbar("권한이 없습니다.");
		return;
	}
	now_postmodal_top = $(window).scrollTop();
	let post_id = $('#M_user_post_modal_container').attr('alt').split('_')[1]*1;
	let title = $('#M_post_top_title').text();
	let content = $('#M_post_body').html();
	postmodal_close(1);
	is_post_property = 0;
	is_postmodal_fixed_open = 1;
	$('#M_user_post_modal_container_fixed').attr('alt', "post_"+post_id);
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
	$('#M_post_fixed_title_input').val(title);
	$('.note-editable').empty();
	$('.note-editable').append(content);
}

//포스트 삭제 함수
function post_delete() {
	let post_id = $('#M_user_post_modal_container').attr('alt').split('_')[1]*1;
	let token = localStorage.getItem('modakbul_token');
	if (token != null){
		let a_jax = A_JAX(TEST_IP+'post_delete/'+post_id, "GET", token, null);
		$.when(a_jax).done(function(){
			let json = a_jax.responseJSON;
			if (json['result'] == "success"){
				snackbar("포스트 삭제를 성공하였습니다.");
				postmodal_close(1);
				location.reload();
			} else if (json['result'] == "do not access") {
				snackbar("권한이 없습니다.");
			} else {
				snackbar("포스트 삭제를 실패하였습니다.");
			}
		});
	} else {
		snackbar("권한이 없습니다.");
	}
}

//textarea init 함수
function M_summernote_init() {
	let theme = localStorage.getItem('modakbul_theme');
	if (theme == 'dark') {
		$('.note-editable').css('background-color', "#494E52");
		$('.note-editable').css('color', "white");
		$('.note-toolbar').css('background-color', '#494E52');
		$('.note-resizebar').remove();
		$('.note-status-output').remove();
	} else {
		$('.note-editable').css('background-color', "white");
		$('.note-editable').css('color', '#5f6f81');
		$('.note-toolbar').css('background-color', 'white');
		$('.note-resizebar').remove();
		$('.note-status-output').remove();
	}
}
/*
$(function(){
	$('#files-upload').MultiFile({
		max: 10, //업로드 최대 파일 갯수 (지정하지 않으면 무한대)
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
		return;
	}
	let token = localStorage.getItem('modakbul_token');
	let is_anony = 0;
	let is_secret = 0;
	let content = $('.note-editable').html();
	let send_data = new FormData();
	var M_files = document.getElementById('files_upload').files;
	var M_list = [];
	if (is_post_modify == 0) {
		for (var i = 0; i < M_files.length; i++){
			M_list.push(M_files[i]);
		}
		if ($('input:checkbox[id="M_post_user_post_anony"]').is(":checked") == true){
			is_anony = 1;
		}
		if ($('input:checkbox[id="M_post_user_post_secret"]').is(":checked") == true){
			is_secret = 1;
		}
		send_data.append("title", $('#M_post_fixed_title_input').val());
		send_data.append("content", content);
		if (content.length >= 50000){
			snackbar("작성 범위를 초과하였습니다.");
			return;
		}
		let searchParams = new URLSearchParams(window.location.search);
		let request_board = searchParams.get('type');
		send_data.append("secret", is_secret);
		send_data.append("anony", is_anony);
		send_data.append("tags", request_board);
		for (var i = 0; i< M_files.length; i++){
			send_data.append('files', M_list[i]);
		}
		let a_jax = A_JAX_FILE(TEST_IP+"post_upload", "POST", token, send_data);
		$.when(a_jax).done(function(){
			let json = a_jax.responseJSON;
			if (json['result'] == "success"){
				snackbar("게시글을 성공적으로 업로드하였습니다.");
				post_write_cancel();
				location.reload();
    	  	}
    	  	else if (json['result'] == 'bad request'){
    	  	 	snackbar("게시글 업로드를 실패하였습니다.");
    	  	}
    	  	else if (json['result'] == 'fail_save_file'){
    	  		snackbar("게시글 업로드를 실패하였습니다.");
    	  	}
    	  	else if (json['result'] == "wrong_file"){
    	  		snackbar("잘못된 파일 확장자명입니다.");
    	  	}
    	  	else if (json['result'] == "unavailable word"){
    	  		snackbar("내용에 욕설이 들어가있습니다.");
    	  	}
    	  	else if (json['result'] == "do not access"){
    	  		snackbar("권한이 없습니다.");
    	  	}
    	  	else {
    	  		snackbar("게시글 업로드를 실패하였습니다.");
    	  	}
		});
	} else {
		for (var i = 0; i < M_files.length; i++){
			M_list.push(M_files[i]);
		}
		if ($('input:checkbox[id="M_post_user_post_anony"]').is(":checked") == true){
			is_anony = 1;
		}
		if ($('input:checkbox[id="M_post_user_post_secret"]').is(":checked") == true){
			is_secret = 1;
		}
		send_data.append("post_id", $('#M_user_post_modal_container_fixed').attr('alt').split('_')[1]*1);
		send_data.append("title", $('#M_post_fixed_title_input').val());
		send_data.append("content", content);
		if (content.length >= 50000){
			snackbar("작성 범위를 초과하였습니다.")
			return;
		}
		send_data.append("anony", is_anony);
		send_data.append("secret", is_secret);
		for (var i = 0; i< M_files.length; i++){
			send_data.append('files', M_list[i]);
		}
		let a_jax = A_JAX_FILE(TEST_IP+"post_update", "POST", token, send_data);
		$.when(a_jax).done(function(){
			let json = a_jax.responseJSON;
			if (json['result'] == "success"){
				snackbar("게실글을 성공적으로 업로드하였습니다.");
				post_write_cancel();
				location.reload();
    	  	}
    	  	else if (json['result'] == 'bad request'){
    	  	 	snackbar("게시글 업로드를 실패하였습니다.");
    	  	}
    	  	else if (json['result'] == 'fail_save_file'){
    	  		snackbar("게시글 업로드를 실패하였습니다.");
    	  	}
    	  	else if (json['result'] == "wrong_file"){
    	  		snackbar("잘못된 파일 확장자명입니다.");
    	  	}
    	  	else if (json['result'] == "unavailable word"){
    	  		snackbar("내용에 욕설이 들어가있습니다.");
    	  	}
    	  	else {
    	  		snackbar("게시글 업로드를 실패하였습니다.");
    	  	}
		});
	}
}

function post_write_cancel() {
	is_postmodal_fixed_open = 0;
	$('#M_post_fixed_title_input').val("");
	$('#M_file_route').empty();
	$('.note-editable').empty();
	history.replaceState(null, null, "#list");
	$('#M_user_post_modal_background_fixed').addClass('fadeOut');
	$('#M_user_post_modal_background_fixed').removeClass('fadeIn');
	$('#M_user_post_modal_container_fixed').removeClass('fadeInUp');
	setTimeout(function(){
  		$('#M_user_post_modal_container_fixed').addClass("display_none");
  		$('#M_user_post_modal_background_fixed').addClass('display_none');
  	}, 400);
	$('html, body').removeAttr("style");
	$('html, body').removeClass('M_modal_open_fixed');
	$('html').scrollTop(now_postmodal_top);
}

/*
//디버그 확인용 코드
for (var value of send_data.values()) {
   	console.log(value); 
}
*/