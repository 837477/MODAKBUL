//Send mail function
function modakbul_git_mail() {
	let title = $('#send_mail_title').val();
	let body = $('#send_mail_body').val();	
	window.open('mailto:shin10256@gmail.com?subject='+title+'&body='+body);
	//window.open('mailto:shin10256@gmail.com');
}

//return main page
function modakbul_credit_return_button() {
	location.href = "/";
}