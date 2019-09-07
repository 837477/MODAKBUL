function darkSetTheme() {
	$('.M_theme').removeClass("fa-moon");
	$('.M_theme').addClass("fa-sun");
	$('body').addClass('M_dark_theme M_dark_theme_body');
	$('#M_body').addClass('M_dark_theme M_dark_theme_body');
	$('#gn-menu').addClass('M_dark_theme M_boxshadow_dark_shadow');
	$('#M_fire_logo').addClass('M_dark_theme');
	$('#gn-menu-wrapper').addClass('M_boxshadow_dark_sidemenu');
	$('#M_nav_user_login').addClass('M_boxshadow_dark_user M_dark_theme');
	$('#M_nav_user_nologin').addClass('M_boxshadow_dark_user M_dark_theme');
	$('#gn-scroller').addClass('M_dark_theme');
	$('.gn-menu-main ul').css({"background-color": "#202124", "color": "#e2e2e2"});
	$('.M_nav_user_button').css("color", "#e2e2e2");
	$('#M_gn-icon').addClass('M_dark_theme');
	$('.M_info_div').css({"background-color": "#494e52", "color": "#f5f6fa", "border": "0px solid #dddddd"});
	$('.gn-menu-wrapper').css("background-color", "#202124");
	$('meta[name="theme-color"]').attr('content', "#202124");
	$('.input100').css("color", "#f5f6fa");
	$('#M_nav_user_nologin a').css("color", "#e2e2e2");
	$('.M_boxshadow').addClass('M_boxshadow_dark_shadow');
	$('#M_search_bar').addClass('M_dark_theme');
	$('#M_search_input').css("color", "#e2e2e2");
	$('#M_post_user_comment_container').css("background-color", "#494e52");
	$('#M_post_user_comment_input').css({"background-color": "#41464a","color": "white"});
	$('#M_post_user_comment_anony_container').css({"background-color": "#41464a","color": "white"});
	$('.demo-1').css("background-color", "#0e0e0f");
	$('.menu__item').css({"color": "#fff", "opacity": "1"});
	$('.M_post_user_comment_send').css({'color': '#e2e2e2', "background-color": "#41464A"});
	$('#M_post_body p').addClass('M_dark_theme_post_body');
}
function whiteSetTheme() {
	$('.M_theme').removeClass("fa-sun");
	$('.M_theme').addClass("fa-moon");
	$('body').removeClass('M_dark_theme M_dark_theme_body');
	$('#M_body').removeClass('M_dark_theme M_dark_theme_body');
	$('#gn-menu').removeClass('M_dark_theme M_boxshadow_dark_shadow');
	$('#M_fire_logo').removeClass('M_dark_theme');
	$('#gn-menu-wrapper').removeClass('M_boxshadow_dark_sidemenu');
	$('#M_nav_user_login').removeClass('M_boxshadow_dark_user M_dark_theme');
	$('#M_nav_user_nologin').removeClass('M_boxshadow_dark_user M_dark_theme');
	$('#gn-scroller').removeClass('M_dark_theme');
	$('.gn-menu-main ul').css({"background-color": "white", "color": "#5f6f81"});
	$('.M_nav_user_button').css("color", "#5f6f81");
	$('#M_gn-icon').removeClass('M_dark_theme');
	$('.M_info_div').css({"background-color": "white", "color": "#3E5569", "border": "0.5px solid #dddddd"});
	$('.gn-menu-wrapper').css("background-color", "white");
	$('meta[name="theme-color"]').attr('content', "white");
	$('.input100').css("color", "#555555");
	$('#M_nav_user_nologin a').css("color", "#5f6f81");
	$('.M_boxshadow').removeClass('M_boxshadow_dark_shadow');
	$('#M_search_bar').removeClass('M_dark_theme');
	$('#M_search_input').css("color", "#5f6f81");
	$('#M_post_user_comment_container').css("background-color", "white");
	$('#M_post_user_comment_input').css({"background-color": "#e2e2e2","color": "#3e5569"});
	$('#M_post_user_comment_anony_container').css({"background-color": "#e2e2e2","color": "#3e5569"});
	$('.demo-1').css("background-color", "#ffffff");
	$('.menu__item').css({"color": "#000", "opacity": "0.7"});
	$('.M_post_user_comment_send').css({'color': '#5f6f81', "background-color": "#e2e2e2"});
	$('#M_post_body p').removeClass('M_dark_theme_post_body');
}
function changeTheme() {
	// now_theme check
	if (localStorage.getItem('modakbul_theme') == null){
		localStorage.setItem('modakbul_theme', "dark");
	} else if (localStorage.getItem('modakbul_theme') == 'white') {
		localStorage.setItem('modakbul_theme', "dark");
	} else {
		localStorage.setItem('modakbul_theme', "white");
	}
	var now_theme = localStorage.getItem('modakbul_theme');
	if (now_theme == 'white'){
		whiteSetTheme();
	}
	else {
		darkSetTheme();
	}
	M_summernote_change();
}
function setTheme() {
	if (localStorage.getItem('modakbul_theme') == null){
		localStorage.setItem('modakbul_theme', "white");
	} else if (localStorage.getItem('modakbul_theme') == 'white') {
		whiteSetTheme();
	} else {
		darkSetTheme();
	}
}


//hover 시 background-color 수정
$('.M_board_content').hover(function(){
    if (localStorage.getItem('modakbul_theme') === 'dark') {
        $(this).css("background-color", "#41464a");
    } else {
        $(this).css("background-color", "#f8f8f8");
    }
}, function(){
    if (localStorage.getItem('modakbul_theme') === 'dark') {
        $(this).css("background-color", "#494e52");
    } else {
        $(this).css("background-color", "white");
    }
});


function M_summernote_change() {
	let theme = localStorage.getItem('modakbul_theme');
	if (theme == 'dark') {
		$('.note-editable').css('background-color', "#494E52");
		$('.note-editable').css('color', "#e2e2e2");
		$('.note-toolbar').css('background-color', '#494E52');
		$('.note-resizebar').remove();
		$('.note-status-output').remove();
		$('.M_file_route').css('color', "#e2e2e2");
		$('.M_filebox').css('color', "#e2e2e2");
	} else {
		$('.note-editable').css('background-color', "white");
		$('.note-editable').css('color', '#5f6f81');
		$('.note-toolbar').css('background-color', 'white');
		$('.note-resizebar').remove();
		$('.note-status-output').remove();
		$('.M_file_route').css('color', "#5f6f81");
		$('.M_filebox').css('color', "#5f6f81");
	}
}

if (localStorage.getItem('modakbul_logo') == 'fire'){
	$('#logo_change_target_fire').removeClass('display_none_important');
} else {
	$('#logo_change_target_logo').removeClass('display_none_important');
	localStorage.removeItem('modakbul_logo');
}

function change_setting_theme() {
	let now_theme = localStorage.getItem('modakbul_theme');
	if (now_theme == 'white'){
		whiteSetTheme_setting();
	}
	else {
		darkSetTheme_setting();
	}
}

function whiteSetTheme_setting() {
	$('.M_setting_line').css('background-color', "#c30e2e");
	$('.M_password_line').css('background-color', "#c30e2e");
	$('.M_setting_tag').css('background-color', '#c30e2e');
	$('#M_image_preview').css('border', '2px solid #c30e2e');
	$('.M_settings_nav').css('border-right', '2px solid #c30e2e');
	$('.M_nav_add').css('border', '1.5px solid #c30e2e');
	$('.M_nav_submit').css('border', '1.5px solid #5f6f81');
	$('.M_bio_wrapper').css('border-bottom', '1.5px solid #c30e2e');
}
function darkSetTheme_setting() {
	$('.M_setting_line').css('background-color', 'white');
	$('.M_password_line').css('background-color', "white");
	$('.M_setting_tag').css('background-color', 'white');
	$('#M_image_preview').css('border', '2px solid white');
	$('.M_settings_nav').css('border-right', '2px solid white');
	$('.M_nav_add').css('border', '1.5px solid white');
	$('.M_nav_submit').css('border', '1.5px solid white');
	$('.M_bio_wrapper').css('border-bottom', '1.5px solid white');
}