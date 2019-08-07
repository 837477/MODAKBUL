$(document).ready(()=>{
    let ajax = A_JAX(TEST_IP+'get_value/학생회로고', 'GET', null, null);

    $.when(ajax).done(()=>{
        $('#M_nav_bar_logo_image_img').attr('src', '../static/image/'+ajax.responseJSON.value);
    })
});