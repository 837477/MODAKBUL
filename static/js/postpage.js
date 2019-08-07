var img_set = ['png', 'jpg', 'jpeg', 'gif', 'bmp'];
var file_path = "../static/files/";
//set post_page
function postpage_init() {
	let now_url = window.location.href.split('#');
	let now_post_id = now_url[now_url.length - 1];
	get_post_info(now_post_id);
}
//get post info function
function get_post_info(get_post_id) {
	let a_jax = A_JAX(TEST_IP+"get_post/"+get_post_id, "GET", null, null);
	$.when(a_jax).done(function(){
		var json = a_jax.responseJSON;
		if (json['result'] == "success"){
			is_post_property = json['property']*1;
			$('#postpage_post').attr('alt', "post_"+json['post']['post_id']);
			$('#postpage_author_color').css("background-color", json['post']['author_color']);
			$('#postpage_author_name').append(json['post']['author_name']);
			$('#postpage_post_time').append("| "+json['post']['post_date']); 	// 날짜 수정
			$('#postpage_post_title').append(json['post']['post_title']);
			$('#postpage_post_body').append(json['post']['post_content']);
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