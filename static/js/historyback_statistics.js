history.replaceState(null, null, "#list");
$(window).bind("hashchange", function(){
  if (is_votemodal_open == 1){
  	votemodal_close();
  	//history.replaceState(null, null, "");
  	//history.replaceState(null, null, "#list");
  }
  else {
  	history.go(-1);
  }
  //postmodal_hashchange();
});