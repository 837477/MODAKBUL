var user_color_output;
var color_selector_scrollTop;
function rgb2hex(rgb) {
     if (  rgb.search("rgb") == -1 ) {
          return rgb;
     } else {
          rgb = rgb.match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+))?\)$/);
          function hex(x) {
               return ("0" + parseInt(x).toString(16)).slice(-2);
          }
          return "#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]); 
     }
}

var user_color_selected;
$(document).ready(function(){
    picker = new jQuery.ColorPicker('#colorpicker', {
        color: '#d8d8d8',
        imagepath: '',
        change: function(hex) {
          $('.user_color_selected_change').css('background-color', hex);
          user_color_output = hex;
          user_color_selected = hex;
        }
    });
});
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-36251023-1']);
_gaq.push(['_setDomainName', 'jqueryscript.net']);
_gaq.push(['_trackPageview']);
(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();

function user_color_select_ok() {
  $('html, body').removeClass('M_modal_open_fixed');
  $('html').animate( { scrollTop : color_selector_scrollTop }, 400 );
  $('#M_user_color_selector_container_modal').addClass('display_none');
  $('#M_user_color_selector_container').addClass("fadeOutUp");
  setTimeout(function(){
    $('#M_user_color_selector_container').addClass("display_none");
  }, 400);
  var send_data = new FormData();
  send_data.append('new_color', user_color_output.toString());
  var token = localStorage.getItem('modakbul_token');
  if (token == null){
    snackbar("올바르지 않은 접근입니다.");
  } else {
    try {
      var a_jax = A_JAX_FILE(TEST_IP+"user_color", "POST", token, send_data);
    } catch(e) {
      snackbar("일시적인 오류로 변경을 실패하였습니다.");
    }
    $.when(a_jax).done(function(){
      var json = a_jax.responseJSON;
      if (json['result'] == "success"){
        snackbar("라벨 색 변경 완료!");
        var color = $('#M_user_img');
        color.css("background-color", user_color_output);
      }
      else if (json['result'] == 'bad request'){
        snackbar("일시적인 오류로 변경을 실패하였습니다.");
      }
      else{
        snackbar("일시적인 오류로 변경을 실패하였습니다.");
      }
    });
  }
}
function user_color_select_cancel() {
  $('html, body').removeClass('M_modal_open_fixed');
  $('html').animate( { scrollTop : color_selector_scrollTop }, 400 );
  $('#M_user_color_selector_container_modal').addClass('display_none');
  $('#M_user_color_selector_container').removeClass('fadeInDown');
  $('#M_user_color_selector_container').addClass("fadeOutUp");
  setTimeout(function(){
    $('#M_user_color_selector_container').addClass("display_none");
  }, 400);
}

function user_color_select_label() {
  var user_color = $('#M_user_img').css('background-color');
  var hex_color = rgb2hex(user_color);
  $('.user_color_selected_change').css('background-color', hex_color);
}

function user_color_select_page_open() {
  color_selector_scrollTop = $(window).scrollTop();
  user_color_select_label();
  $('html').animate( { scrollTop : 0 }, 400 );
  setTimeout(function() {
    $('html, body').addClass('M_modal_open_fixed');
    $('#M_user_color_selector_container_modal').removeClass('display_none');
    $('#M_user_color_selector_container').removeClass("fadeOutUp");
    $('#M_user_color_selector_container').addClass("fadeInDown");
    $('#M_user_color_selector_container').removeClass('display_none');
    $('#user_color_selector_info_content_name').empty();
    $('#user_color_selector_info_content_name').append($('#M_user_content_name').text());  
  }, 400);
}