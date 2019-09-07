history.replaceState(null, null, "#list");
$(window).bind("hashchange", function(){
  if (is_postmodal_open == 1){
  	postmodal_close();
  	//history.replaceState(null, null, "");
  	//history.replaceState(null, null, "#list");
  }
  else {
  	history.go(-1);
  }
  //postmodal_hashchange();
});