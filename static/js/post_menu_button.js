$(document).ready(function(ev) {
  var toggle = $('#ss_toggle');
  var menu = $('#ss_menu');
  var rot;
  
  $('#ss_toggle').on('click', function(ev) {
    rot = parseInt($(this).data('rot')) - 180;
    menu.css('transform', 'rotate(' + rot + 'deg)');
    menu.css('webkitTransform', 'rotate(' + rot + 'deg)');
    if ((rot / 180) % 2 == 0) {
      //Moving in
      toggle.parent().addClass('ss_active');
      toggle.addClass('close');
    } else {
      //Moving Out
      toggle.parent().removeClass('ss_active');
      toggle.removeClass('close');
    }
    $(this).data('rot', rot);
  });

  menu.on('transitionend webkitTransitionEnd oTransitionEnd', function() {
    if ((rot / 180) % 2 == 0) {
      $('#ss_menu div i').addClass('ss_animate');
    } else {
      $('#ss_menu div i').removeClass('ss_animate');
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