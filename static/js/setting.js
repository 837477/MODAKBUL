const DEPARTMENTS = ['데이터사이언스학과', '디자인이노베이션', '디지털콘텐츠학과', '만화애니메이션텍', '소프트웨어학과', '정보보호학과', '지능기전공학부', '창의소프트학부', '컴퓨터공학과'];
let bio_cnt = 0;
$(document).ready(()=>{
   let ajax = A_JAX(TEST_IP+'get_variables', "GET", null, null);
   $.when(ajax).done(()=>{

       let name = ajax.responseJSON.variables.filter(data => {
           return data.v_key === '학생회이름'
       });
       let subtitle = ajax.responseJSON.variables.filter(data => {
           return data.v_key === '학생회부제'
       });
       let image = ajax.responseJSON.variables.filter(data =>{
           return data.v_key === '학생회로고'
       });
       $('#M_union_name').attr('placeholder', name[0].value);
       $('#M_union_subtitle').attr('placeholder', subtitle[0].value);
       $('#M_image_preview').attr('src', '../static/image/'+image[0].value);
   });
   let filter = "win16|win32|win64|mac|macintel";
    if ( navigator.platform ) { //mobile
        if ( filter.indexOf( navigator.platform.toLowerCase() ) < 0 ) {
            $('body').css('overflow-y', 'auto');
        } else {
            $('.M_info').css('overflow-y', 'auto');
            $('.M_setting').css('height', '90%');
        }
    }

    let tag_ajax = A_JAX(TEST_IP+'get_access_tags', 'GET', null, null);
    $.when(tag_ajax).done(function() {
        for (let i=0; i<tag_ajax.responseJSON.tags.length; i++)
        {
            $('.M_tag_list').append(
                '<div class="M_tag_list_item">'+
                '# <div class="M_tag_name" style="display:inline;">' + tag_ajax.responseJSON.tags[i] + ' </div>'+
                '<i onclick="delete_modify_tag($(this))" class="fas fa-trash-alt M_tag_icon_delete"></i>'+
                '<i onclick="modify_tag($(this))" class="fas fa-pencil-alt M_tag_icon_fixed"></i>'+
                '<i onclick="cancel_modify_tag($(this))" style="display: none;" class="far fa-times-circle M_tag_icon_cancel"></i>'+
                '<i onclick="accept_modify_tag($(this))" style="display: none;" class="fas fa-check M_tag_icon_check"></i>'+
                '</div>'
            )
        }
    });

    black_list();

    let intro_ajax = A_JAX(TEST_IP+'get_department/0', 'GET', null, null);
    let result_html = '';
    $.when(intro_ajax).done(()=>{

        for (let i=0; i<intro_ajax.responseJSON.department.length; i++)
        {
            result_html +=
                '            <div class="M_bio_wrapper" style="overflow-y: scroll;height: 85%;">\n' +
                '                <div class="M_setting_subtitle_wrapper3">\n' +
                '                    <div class="M_settings_subtitle_wrapper">\n' +
                '                        <div class="M_setting_tag"></div>\n' +
                '                        <div class="M_setting_subtitle">사진</div>\n' +
                '                    </div>\n' +
                '                    <img id="M_principle_profile_pic-'+ intro_ajax.responseJSON.department[i].dm_id +'" onclick="profile_pic_upload(\'' + intro_ajax.responseJSON.department[i].dm_id + '\')\" src="/static/images/' + intro_ajax.responseJSON.department[i].dm_img + '" class="M_setting_introduce_image">\n' +
                '                    <input onchange="profile_change($(this), '+ intro_ajax.responseJSON.department[i].dm_id +')" id="M_principle_profile_upload-'+ intro_ajax.responseJSON.department[i].dm_id +'" type="file" style="display: none;">\n' +
                '                    <div class="M_image_warning_introduce">\n' +
                '                    대표 사진을 업로드해주세요!\n' +
                '                    </div>\n' +
                '                </div>\n' +
                '                <div class="M_setting_subtitle_wrapper4">\n' +
                '                    <div class="M_settings_subtitle_wrapper">\n' +
                '                        <div class="M_setting_tag"></div>\n' +
                '                        <div class="M_setting_subtitle">직책</div>\n' +
                '                    </div>\n' +
                '                    <div class="M_position">\n' +
                '                        <input class="M_bio_input" disabled type="text" value="' + intro_ajax.responseJSON.department[i].dm_name + '">'+
                '                    </div>\n' +
                '                    <div class="M_settings_subtitle_wrapper">\n' +
                '                        <div class="M_setting_tag"></div>\n' +
                '                        <div class="M_setting_subtitle">정보</div>\n' +
                '                    </div>\n' +
                '                    <div class="M_manager">\n' +
                '                        <input class="M_bio_input" type="text" value="' + intro_ajax.responseJSON.department[i].dm_chairman +'">\n' +
                '                    </div>\n' +
                '                    <div class="M_settings_subtitle_wrapper">\n' +
                '                        <div class="M_setting_tag"></div>\n' +
                '                        <div class="M_setting_subtitle">소개</div>\n' +
                '                    </div>\n' +
                '                    <div class="M_manager_bio">\n' +
                '                        <textarea class="M_bio_input" style="height: 100px; margin-bottom: 0;" type="text"></textarea>' +
                '                    </div>'+
                '              </div>'+
                '            </div>';
        }
        $('#M_student_introduce_target').append(result_html);
        change_setting_theme();
    });

    let intro_ajax2 = A_JAX(TEST_IP+'get_department/1', 'GET', null, null);
    let result_html2 = '';
    $.when(intro_ajax2).done(()=>{
        for (let i=0; i<intro_ajax2.responseJSON.department.length; i++)
        {
            result_html2 +=
                '            <div class="M_bio_wrapper" style="overflow-y: scroll;height: 85%;">\n' +
                '                <div class="M_setting_subtitle_wrapper3">\n' +
                '                    <div class="M_settings_subtitle_wrapper">\n' +
                '                        <div class="M_setting_tag"></div>\n' +
                '                        <div class="M_setting_subtitle">사진</div>\n' +
                '                    </div>\n' +
                '                    <img id="M_principle_profile_pic-'+ intro_ajax2.responseJSON.department[i].dm_id +'" onclick="profile_pic_upload(\'' + intro_ajax2.responseJSON.department[i].dm_id + '\')\" src="/static/images/' + intro_ajax2.responseJSON.department[i].dm_img + '" class="M_setting_introduce_image">\n' +
                '                    <input onchange="profile_change($(this), '+ intro_ajax2.responseJSON.department[i].dm_id +')" id="M_principle_profile_upload-'+ intro_ajax2.responseJSON.department[i].dm_id +'" type="file" style="display: none;">\n' +
                '                    <div class="M_image_warning_introduce">\n' +
                '                    대표 사진을 업로드해주세요!\n' +
                '                    </div>\n' +
                '                </div>\n' +
                '                <div class="M_setting_subtitle_wrapper4">\n' +
                '                    <div class="M_settings_subtitle_wrapper">\n' +
                '                        <div class="M_setting_tag"></div>\n' +
                '                        <div class="M_setting_subtitle">직책</div>\n' +
                '                    </div>\n' +
                '                    <div class="M_position">\n' +
                '                        <input class="M_bio_input" type="text" value="' + intro_ajax2.responseJSON.department[i].dm_name + '">'+
                '                    </div>\n' +
                '                    <div class="M_settings_subtitle_wrapper">\n' +
                '                        <div class="M_setting_tag"></div>\n' +
                '                        <div class="M_setting_subtitle">정보</div>\n' +
                '                    </div>\n' +
                '                    <div class="M_manager">\n' +
                '                        <input class="M_bio_input" type="text" value="' + intro_ajax2.responseJSON.department[i].dm_chairman +'">\n' +
                '                    </div>\n' +
                '                    <div class="M_settings_subtitle_wrapper">\n' +
                '                        <div class="M_setting_tag"></div>\n' +
                '                        <div class="M_setting_subtitle">소개</div>\n' +
                '                    </div>\n' +
                '                    <div class="M_manager_bio">\n' +
                '                        <textarea class="M_bio_input" style="height: 100px; margin-bottom: 0;" type="text"></textarea>' +
                '                    </div>'+
                '              </div>'+
                '<div onclick="delete_intro($(this), ' + intro_ajax2.responseJSON.department[i].dm_id + ')" class="M_setting_introduce_delete_button">'+
                '<i class="fas fa-trash-alt"></i>'+
                '</div>'+
                '</div>';
        }
        $('#M_student_introduce_target_2').append(result_html2);
        bio_cnt = intro_ajax2.responseJSON.department[intro_ajax2.responseJSON.department.length - 1].dm_id + 1;
        change_setting_theme();
    });

});

function black_list() {
    let black_ajax = A_JAX(TEST_IP+'get_blacklist', 'GET', null, null);
    $.when(black_ajax).done(()=>{
        result_html = '';
        for (let i=0; i<black_ajax.responseJSON.blacklist.length; i++) {
            let major = '';
            for (let j=0; j<DEPARTMENTS.length; j++)
            {
                if (black_ajax.responseJSON.blacklist[i].tags.indexOf(DEPARTMENTS[j]) !== -1) {
                    major = DEPARTMENTS[j];
                }
            }


            result_html += '<div class="M_black_user_info">' +
                '<div style="background-color: ' +  black_ajax.responseJSON.blacklist[i].user_color + '" class="M_setting_user_tag"></div>'+
                '<div class="M_setting_subtitle_name">'+
                black_ajax.responseJSON.blacklist[i].user_name + ' ' +
                black_ajax.responseJSON.blacklist[i].user_id + ' ' +
                major +
                '</div>'+
                '<div onclick="white_user($(this))" class="M_setting_unblack_button">취소</div></div>';
        }
        $('.M_setting_blacklist').append(result_html);
    })
}

function toggle(flag) {
    let info = $('.M_info');
    let principle_bio = $('.M_principle_bio');
    let bio = $('.M_bio');
    let user = $('.M_user');
    let menu = $('.M_menu');
    let tag = $('.M_tag');
    let password = $('.M_password');

    if (flag === 0){
        info.css('display', 'inline-block');
        principle_bio.css('display', 'none');
        bio.css('display', 'none');
        user.css('display', 'none');
        menu.css('display', 'none');
        tag.css('display', 'none');
        password.css('display', 'none');
    }
    else if (flag === 1){
        info.css('display', 'none');
        principle_bio.css('display', 'inline-block');
        bio.css('display', 'none');
        user.css('display', 'none');
        menu.css('display', 'none');
        tag.css('display', 'none');
        password.css('display', 'none');
    }
    else if (flag === 2){
        info.css('display', 'none');
        principle_bio.css('display', 'none');
        bio.css('display', 'inline-block');
        user.css('display', 'none');
        menu.css('display', 'none');
        tag.css('display', 'none');
        password.css('display', 'none');
    }
    else if (flag === 3){
        info.css('display', 'none');
        principle_bio.css('display', 'none');
        bio.css('display', 'none');
        user.css('display', 'inline-block');
        menu.css('display', 'none');
        tag.css('display', 'none');
        password.css('display', 'none');
    }
    else if (flag === 4){
        info.css('display', 'none');
        principle_bio.css('display', 'none');
        bio.css('display', 'none');
        user.css('display', 'none');
        menu.css('display', 'inline-block');
        tag.css('display', 'none');
        password.css('display', 'none');
    }
    else if (flag === 5){
        info.css('display', 'none');
        principle_bio.css('display', 'none');
        bio.css('display', 'none');
        user.css('display', 'none');
        menu.css('display', 'none');
        tag.css('display', 'inline-block');
        password.css('display', 'none');
    }
    else if (flag === 6){
        info.css('display', 'none');
        principle_bio.css('display', 'none');
        bio.css('display', 'none');
        user.css('display', 'none');
        menu.css('display', 'none');
        tag.css('display', 'none');
        password.css('display', 'inline-block');
    }
}

function accept_modify_tag(tag) {
    let old_value = tag.prev().prev().prev().prev().attr('placeholder');
    let new_value = tag.prev().prev().prev().prev().val();
    let send_data = new FormData();
    send_data.append('new_tag', new_value);
    send_data.append('old_tag', old_value);
    let a_jax = A_JAX_FILE(TEST_IP+'update_tag', 'POST', null, send_data);
    $.when(a_jax).done(function(){
        let json = a_jax.responseJSON;
        if (json['result'] == 'success'){
            snackbar("태그를 수정하였습니다.");
            $('.M_tag_list').empty();
            let tag_ajax = A_JAX(TEST_IP+'get_access_tags', 'GET', null, null);
            $.when(tag_ajax).done(function() {
                for (let i=0; i<tag_ajax.responseJSON.tags.length; i++)
                {
                    $('.M_tag_list').append(
                        '<div class="M_tag_list_item">'+
                        '# <div class="M_tag_name" style="display:inline;">' + tag_ajax.responseJSON.tags[i] + ' </div>'+
                        '<i onclick="delete_modify_tag($(this))" class="fas fa-trash-alt M_tag_icon_delete"></i>'+
                        '<i onclick="modify_tag($(this))" class="fas fa-pencil-alt M_tag_icon_fixed"></i>'+
                        '<i onclick="cancel_modify_tag($(this))" style="display: none;" class="far fa-times-circle M_tag_icon_cancel"></i>'+
                        '<i onclick="accept_modify_tag($(this))" style="display: none;" class="fas fa-check M_tag_icon_check"></i>'+
                        '</div>'
                    )
                }
            });
        } else if (json['result'] == 'do not use special characters'){
            snackbar("특수기호는 사용할 수 없습니다.");
        }
        else {
            snackbar("태그 수정에 실패하였습니다.");
        }
    });
}

function delete_modify_tag(tag) {
    let value;
    if (tag.prev('input').attr('placeholder') != undefined){
        value = tag.prev('input').attr('placeholder');
    } else if (tag.prev('div').text() != "") {
        value = tag.prev('div').text();
    }
    let send_data = new FormData();
    send_data.append('tag', value);
    let a_jax = A_JAX_FILE(TEST_IP+"delete_tag", "POST", null, send_data);
    $.when(a_jax).done(function(){
        let json = a_jax.responseJSON;
        if (json['result'] == 'success'){
            snackbar("태그를 삭제하였습니다.");
            $('.M_tag_list').empty();
            let tag_ajax = A_JAX(TEST_IP+'get_access_tags', 'GET', null, null);
            $.when(tag_ajax).done(function() {
                for (let i=0; i<tag_ajax.responseJSON.tags.length; i++)
                {
                    $('.M_tag_list').append(
                        '<div class="M_tag_list_item">'+
                        '# <div class="M_tag_name" style="display:inline;">' + tag_ajax.responseJSON.tags[i] + ' </div>'+
                        '<i onclick="delete_modify_tag($(this))" class="fas fa-trash-alt M_tag_icon_delete"></i>'+
                        '<i onclick="modify_tag($(this))" class="fas fa-pencil-alt M_tag_icon_fixed"></i>'+
                        '<i onclick="cancel_modify_tag($(this))" style="display: none;" class="far fa-times-circle M_tag_icon_cancel"></i>'+
                        '<i onclick="accept_modify_tag($(this))" style="display: none;" class="fas fa-check M_tag_icon_check"></i>'+
                        '</div>'
                    )
                }
            });
        } else {
            snackbar("태그 삭제에 실패하였습니다.");
        }
    });
}

function modify_tag(tag) {
    let prev_value = tag.prev().prev().text();
    let input_tag =  document.createElement('input');
    input_tag.setAttribute('type', 'text');
    input_tag.classList.add('M_setting_tag_change_input');
    input_tag.setAttribute('placeholder', prev_value);
    tag.prev().prev().replaceWith($(input_tag));
    $(input_tag).focus();
    tag.parent().css('border-bottom', '1.5px solid #c30e2e');
    tag.next('i').css('display', 'inline-block');
    tag.next('i').next('i').css('display', 'inline-block');
    tag.css('display', 'none');
}

function cancel_modify_tag(tag) {
    let tag_name_value = tag.prev().prev().prev().attr('placeholder');
    let tag_name = document.createElement('div');
    tag_name.classList.add('M_tag_name');
    tag_name.style.display = 'inline';
    tag_name.append(tag_name_value);
    tag.prev().prev().prev().replaceWith($(tag_name));
    tag.next('i').css('display', 'none');
    tag.prev('i').css('display', 'inline-block');
    tag.css('display', 'none');
    tag.parent().css('border-bottom', '1.5px solid #e2e2e2');
}

function plus_tag_button(tag) {
    let reader = '<div class="M_tag_list_item" style="border-bottom: 1.5px solid rgb(195, 14, 46);">#'+
                '<input type="text" class="M_setting_tag_change_input2" placeholder="태그명을 입력해주세요.">'+
                '<i onclick="plus_tag_delete($(this))" class="far fa-times-circle M_tag_icon_cancel"></i>'+
                '<i onclick="plus_tag_append($(this))" class="fas fa-check M_tag_icon_check"></i>'+
                '</div>';
    $('.M_tag_list').append(reader);
    $('.M_tag_list').children().last().children('input').focus();
}

function plus_tag_append(tag) {
    let value = tag. prev().prev().val();
    if (value == ""){
        snackbar("태그명을 입력해주세요.");
        tag.focus();
    } else {
        let send_data = new FormData();
        send_data.append('tag', value);
        let a_jax = A_JAX_FILE(TEST_IP+'input_tag', "POST", null, send_data);
        $.when(a_jax).done(function(){
            let json = a_jax.responseJSON;
            console.log(json);
            if (json['result'] == 'success'){
                snackbar("태그가 추가되었습니다.");
                $('.M_tag_list').empty();
                let tag_ajax = A_JAX(TEST_IP+'get_access_tags', 'GET', null, null);
                $.when(tag_ajax).done(function() {
                    for (let i=0; i<tag_ajax.responseJSON.tags.length; i++)
                    {
                        $('.M_tag_list').append(
                            '<div class="M_tag_list_item">'+
                            '#<div class="M_tag_name" style="display:inline;">' + tag_ajax.responseJSON.tags[i] + ' </div>'+
                            '<i onclick="delete_modify_tag($(this))" class="fas fa-trash-alt M_tag_icon_delete"></i>'+
                            '<i onclick="modify_tag($(this))" class="fas fa-pencil-alt M_tag_icon_fixed"></i>'+
                            '<i onclick="cancel_modify_tag($(this))" style="display: none;" class="far fa-times-circle M_tag_icon_cancel"></i>'+
                            '<i onclick="accept_modify_tag($(this))" style="display: none;" class="fas fa-check M_tag_icon_check"></i>'+
                            '</div>'
                        )
                    }
                });
            } else {
                snackbar("태그 추가에 실패하였습니다.");
            }
        }); 
    }
}

function plus_tag_delete(tag) {
    tag.parent().remove();
}

function upload_logo() {
    $('#M_logo_upload').trigger('click');
}

let image;
function image_preview(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();

        reader.onload = function(e) {
            $('#M_image_preview').attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
        image = input.files;
    }
}

function profile_pic_upload(id) {
    let target = $('#M_principle_profile_upload-'+id);
    target.trigger('click');
}

function profile_change(target, id) {
    let image = $('#M_principle_profile_pic-'+id);
    target = target[0];
    if (target.files && target.files[0]) {
        let reader = new FileReader();
        reader.onload = function(e) {
            image.attr('src', e.target.result);
        };
        reader.readAsDataURL(target.files[0]);
    }
}

let image_updated = false;
let name_updated = false;
let subtitle_updated = false;
let main_bio_updated = false;
let contacts_updated = false;

$('#M_logo_upload').change(function () {
   image_preview(this);
   image_updated = true;
});

$('#M_union_name').change(()=>{
    name_updated = true;
});

$('#M_union_subtitle').change(()=>{
    subtitle_updated = true;
});

$('#M_union_info_wrapper_introduce_textarea').change(()=>{
    main_bio_updated = true;
});

$('#M_union_info_wrapper_phonenumber_textarea').change(()=>{
    contacts_updated = true;
});

function submit_bio() {
    if (image_updated === true)
    {
        let img_data = new FormData();
        img_data.append('img', image[0]);
        let img_ajax = A_JAX_FILE(TEST_IP+'change_logo', 'POST', localStorage.getItem('modakbul_token'), img_data);
        $.when(img_ajax).done(()=>{
            location.reload();
        })
    }
    if (name_updated === true)
    {
        let div = $('#M_union_name');
        let new_name = div.val();
        let name_data = {'key': '학생회이름', 'value': div.val()};
        let name_ajax = A_JAX(TEST_IP+'variable_update', 'POST', null, name_data);
        $.when(name_ajax).done(()=>{
            div.val('');
            div.attr('placeholder', new_name);
        });
        snackbar('적용되었습니다.');
    }
    if (subtitle_updated === true)
    {
        let div = $('#M_union_subtitle');
        let new_subtitle = div.val();
        let subtitle_data = {'key': '학생회부제', 'value': div.val()};
        let subtitle_ajax = A_JAX(TEST_IP+'variable_update', 'POST', null, subtitle_data);
        $.when(subtitle_ajax).done(()=>{
            div.val('');
            div.attr('placeholder', new_subtitle);
        });
        snackbar('적용되었습니다.');
    }
    if (main_bio_updated === true)
    {
        let introduce_textarea_value; // 학생회 소개 textarea
        let tmp;
        tmp =  $('#M_union_info_wrapper_introduce_textarea').val();
        introduce_textarea_value = tmp.replace(/\n/g, "<br />");

        let main_bio_data = {'key': '총인사말', 'value': introduce_textarea_value};
        let main_bio_ajax = A_JAX(TEST_IP+'variable_update', 'POST', null, main_bio_data);
        $.when(main_bio_ajax).done(()=>{
            $('#M_union_info_wrapper_introduce_textarea').val('');
            $('#M_union_info_wrapper_introduce_textarea').attr('placeholder', tmp);
        });
        snackbar('적용되었습니다.');
    }
    if (contacts_updated === true)
    {
        let contacts_textarea_value; // 학생회 소개 textarea
        let tmp;
        tmp =  $('#M_union_info_wrapper_phonenumber_textarea').val();
        contacts_textarea_value = tmp.replace(/\n/g, "<br />");

        let contacts_data = {'key': '연락처', 'value': contacts_textarea_value};
        let contacts_ajax = A_JAX(TEST_IP+'variable_update', 'POST', null, contacts_data);
        $.when(contacts_ajax).done(()=> {
            $('#M_union_info_wrapper_phonenumber_textarea').val('');
            $('#M_union_info_wrapper_phonenumber_textarea').attr('placeholder', tmp);
        });
        snackbar('적용되었습니다.');
    }
}
function settingsPage_check_admin() {
    let a_jax = A_JAX(TEST_IP+"get_userinfo", "GET", null, null);
    $.when(a_jax).done(function(){
        let json = a_jax.responseJSON;
        if (json['result'] == "success"){
            //You are admin!
        } else {
            alert("접근 권한이 없습니다.");
            location.href = "/";
        }
    });
    $.when(a_jax).fail(function(){
        alert("접근 권한이 없습니다.");
        location.href = "/";
    });
}
function search_user() {
    let search = $('.M_user_search').val();
    if (search == ""){
        $('#M_user_info').empty();
        return;
    }
    let ajax = A_JAX(TEST_IP+"get_user_search", "POST", null, {'search': search});
    let result_html = '';
    $.when(ajax).done(()=>{
        if (ajax.responseJSON.result === 'user is not defined') {
            snackbar('사용자가 없습니다.')
        }
        else {
            snackbar(ajax.responseJSON.user.length+" 명이 검색되었습니다.");
            for (let i = 0; i < ajax.responseJSON.user.length; i++){
                let major = '';
                for (let j=0; j<DEPARTMENTS.length; j++){
                    if (ajax.responseJSON.user[i].tags.indexOf(DEPARTMENTS[j]) !== -1) {
                        major = DEPARTMENTS[j];
                        break;
                    }
                }
                result_html +=
                    '<div class="M_user_info_container">'+
                    '<div style="background-color: ' +  ajax.responseJSON.user[i].user_color + '" class="M_setting_user_tag"></div>'+
                    '<div class="M_setting_subtitle_name">'+
                    ' ' + ajax.responseJSON.user[i].user_name + ' ' + ajax.responseJSON.user[i].user_id + ' '+ major +
                    '</div>'+
                    '<div onclick="black_user($(this).parent())" class = "M_setting_black_button"> 블랙</div></div><br>';
            }
            $('#M_user_info').empty();
            $('#M_user_info').append(result_html);
        }
    })
}

$('.M_user_search').keypress(function (e) {
    let key = e.which;
    if(key === 13)
    {
        search_user();
    }
});

function black_user(div) {
    let ajax = A_JAX(TEST_IP+"user_black_apply", "POST", null, {'target_id': div[0].childNodes[1].innerText.split(' ')[1]});
    $.when(ajax).done(()=>{
        if (ajax.responseJSON.result === 'success'){
            snackbar("블랙리스트에 추가하였습니다.");
            $('.M_setting_blacklist').empty();
            black_list();
        }
        else if (ajax.responseJSON.result === 'already blacklist') {
            snackbar('이미 블랙리스트에 추가된 사용자 입니다.');
        }
        else {
            snackbar("블랙리스트 추가에 실패하였습니다.");
            $('#M_user_info').empty();
        }
    })
}
function white_user(div) {
    let ajax = A_JAX(TEST_IP+"user_black_cancel", "POST", null, {'target_id': div.parent()[0].childNodes[1].innerText.split(' ')[1]});
    $.when(ajax).done(()=>{
        if (ajax.responseJSON.result === 'no blacklist') {
            snackbar('이미 블랙리스트에서 제거된 사용자 입니다.');
        }
        $('.M_setting_blacklist').empty();
        black_list();
    })
}
function change_password() {
    let prev_pw = $('#prev_pw').val();
    let new_pw = $('#new_pw').val();
    let new_pw_confirm = $('#new_pw_confirm').val();

    if (prev_pw === '') {
        snackbar('이전 비밀번호를 입력해주세요.');
        $('#prev_pw').focus();
        return;
    }
    else if (new_pw === '') {
        snackbar('새 비밀번호를 입력해주세요.');
        $('#new_pw').focus();
        return;
    }
    else if (new_pw_confirm === '') {
        snackbar('비밀번호 재확인을 입력해주세요.');
        $('#new_pw_confirm').focus();
        return;
    }

    let data = {'old_pw': prev_pw, 'new_pw_1': new_pw, 'new_pw_2': new_pw_confirm};

    let ajax = A_JAX(TEST_IP+"change_pw", "POST", null, data);
    $.when(ajax).done(()=>{
        if (ajax.responseJSON.result === 'success'){
            snackbar("비밀번호 변경에 성공하였습니다.");
            setTimeout(function() {
                location.reload();
            }, 400);
        }
        else if (ajax.responseJSON.result === 'not same pw') {
            snackbar('새 비밀번호가 일치하지 않습니다.');
             $('#new_pw').focus();
        }
        else if (ajax.responseJSON.result === 'wrong old pw') {
            snackbar('이전 비밀번호가 일치하지 않습니다.');
            $('#prev_pw').focus();
        }
    })

}

function update_bio(type) {
    let list = [];

    if (type === 0) {
        for (let i=0; i< $('#M_student_introduce_target')[0].childNodes.length; i++){
            if ($('#M_student_introduce_target')[0].childNodes[i].className === 'M_bio_wrapper') list.push($('#M_student_introduce_target')[0].childNodes[i]);
        }
    }
    else {
        for (let i=0; i< $('#M_student_introduce_target_2')[0].childNodes.length; i++){
            if ($('#M_student_introduce_target_2')[0].childNodes[i].className === 'M_bio_wrapper') list.push($('#M_student_introduce_target_2')[0].childNodes[i]);
        }
    }

    for (let i=0; i<list.length; i++) {
        let image = $(list[i].children[0].children[2])[0].files[0];
        let name = $(list[i].children[1].children[1].children[0]).val();
        let info =$(list[i].children[1].children[3].children[0]).val();
        let bio = $(list[i].children[1].children[5].children[0]).val();
        let id = $(list[i].children[0].children[2])[0].id.split('-')[1];
        bio = bio.replace(/\n/g, "<br />");
        console.log(name);
        console.log(info);
        console.log(bio);
        console.log(id);
        console.log(image);

        let data = new FormData();

        data.append('dm_id', id);
        data.append('dm_name', name);
        data.append('dm_chairman', info);
        data.append('dm_intro', bio);
        data.append('dm_type', type);
        data.append('dm_img', image);

        let ajax = A_JAX_FILE(TEST_IP+"department_update", "POST", null, data);
        $.when(ajax).done(()=>{
            if (ajax.responseJSON.result === 'img is not defined') {
                snackbar('새로운 국장 소개를 추가할 때는 사진을 필수로 업로드해야합니다.')
            }
            else if (ajax.responseJSON.result === 'wrong extension') {
                snackbar('이미지 확장자가 옳바르지 않습니다.')
            }
            else if (ajax.responseJSON.result === 'file save fail') {
                alert('일시적인 오류입니다. 다시시도해주세요.');
                location.reload();
            }
        });
    }
    snackbar('적용되었습니다.');
}

function add_intro() {
    console.log(bio_cnt);
    $('#M_student_introduce_target_2').append(
        '            <div class="M_bio_wrapper" style="overflow-y: scroll;height: 85%;">\n' +
        '                <div class="M_setting_subtitle_wrapper3">\n' +
        '                    <div class="M_settings_subtitle_wrapper">\n' +
        '                        <div class="M_setting_tag"></div>\n' +
        '                        <div class="M_setting_subtitle">사진</div>\n' +
        '                    </div>\n' +
        '                    <img id="M_principle_profile_pic-'+ bio_cnt +'" onclick="profile_pic_upload(\'' + bio_cnt + '\')\" src="/static/images/' + '#'+ '" class="M_setting_introduce_image">\n' +
        '                    <input onchange="profile_change($(this), '+ bio_cnt +')" id="M_principle_profile_upload-'+ bio_cnt +'" type="file" style="display: none;">\n' +
        '                    <div class="M_image_warning_introduce">\n' +
        '                    대표 사진을 업로드해주세요!\n' +
        '                    </div>\n' +
        '                </div>\n' +
        '                <div class="M_setting_subtitle_wrapper4">\n' +
        '                    <div class="M_settings_subtitle_wrapper">\n' +
        '                        <div class="M_setting_tag"></div>\n' +
        '                        <div class="M_setting_subtitle">직책</div>\n' +
        '                    </div>\n' +
        '                    <div class="M_position">\n' +
        '                        <input class="M_bio_input" type="text">'+
        '                    </div>\n' +
        '                    <div class="M_settings_subtitle_wrapper">\n' +
        '                        <div class="M_setting_tag"></div>\n' +
        '                        <div class="M_setting_subtitle">정보</div>\n' +
        '                    </div>\n' +
        '                    <div class="M_manager">\n' +
        '                        <input class="M_bio_input" type="text" value="">\n' +
        '                    </div>\n' +
        '                    <div class="M_settings_subtitle_wrapper">\n' +
        '                        <div class="M_setting_tag"></div>\n' +
        '                        <div class="M_setting_subtitle">소개</div>\n' +
        '                    </div>\n' +
        '                    <div class="M_manager_bio">\n' +
        '                        <textarea class="M_bio_input" style="height: 100px; margin-bottom: 0;" type="text"></textarea>' +
        '                    </div>'+
        '              </div>'+
        '<div onclick="delete_intro($(this))" class="M_setting_introduce_delete_button">'+
        '<i class="fas fa-trash-alt"></i>'+
        '</div>'+
        '</div>'
    );
    bio_cnt++;
    change_setting_theme();
}

function delete_intro(target, id) {
    console.log(target.parent());
    target.parent().remove();

    if (id === undefined){
        bio_cnt--;
        return;
    }

    let intro_ajax2 = A_JAX(TEST_IP+'department_delete/'+id, 'GET', null, null);
    $.when(intro_ajax2).done(()=>{
            update_bio(1);
    });
}










