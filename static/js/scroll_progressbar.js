var progressIndicator = '<div id="i-am-progress-indicator"></div>';
$('body').append(progressIndicator);

$(window).on('scroll', function(){
    var currentPercentage = ($(window).scrollTop() / ($(document).outerHeight() - $(window).height())) * 100;
  $('#i-am-progress-indicator').width(currentPercentage+'%');
});