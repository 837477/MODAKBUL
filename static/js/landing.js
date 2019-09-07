$(document).ready(()=>{
    let name_ajax = A_JAX(TEST_IP+'get_value/학생회이름', 'GET', null, null);

    $.when(name_ajax).done(()=>{
        $('#M_name').text(name_ajax.responseJSON.value);

        if (localStorage.getItem('modakbul_theme') === 'dark') animateTitles_dark();
        else animateTitles_white();
    })

    let subtitle_ajax = A_JAX(TEST_IP+'get_value/학생회부제', 'GET', null, null);
    $.when(subtitle_ajax).done(()=>{
        $('#M_subtitle').text(subtitle_ajax.responseJSON.value);
    })
})