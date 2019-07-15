function A_JAX(url, type, token, data){
    var ajax_;
    var json_data = data;
    if(token == null)
    {
        ajax_ = $.ajax({
            type: type,
            url: url,
            data: json_data,
            dataType : "json",
            success: function(res){
            },
            error: function(res){
            }
        });
    }
    else
    {
        ajax_ = $.ajax({
            type: type,
            url: url,
            headers: {"Authorization": 'Bearer ' + token },
            data: json_data,
            processData: false,
            contentType: false,
            dataType : "json",
            success: function(res){},
            error: function(res){
            }
        });
    }
    return ajax_;
}


//로그인 버튼을 누를 시, 실행되는 함수
function user_login()
{
   var login_ID = $('#user_id').val();   // user_id 란 ID 값의 value 값 가져옴
   var login_PW = $('#user_pw').val();   // user_pw 란 ID 값의 value 값 가져옴
   
   if (login_ID.length <= 0 || login_PW.length <= 0){
      alert("아이디 및 비밀번호를 입력해주세요.");
      return;
   }

   var send_data = {id: login_ID, pw: login_PW};
   var a_jax = A_JAX('http://localhost:5000/sign-in-up', "POST", null, send_data);   //"/login" 이라는 url에 아이디/비밀번호 data 전송
   $.when(a_jax).done(function(){
      var json = a_jax.responseJSON;
      if (json['result'] == "your not Sejong"){         // result 값이 "your not Sejong" 이라면 실행
         alert("로그인에 실패하였습니다.");
      }
      else if (json['result'] == "password incorrect"){   // result 값이 "password incorrect" 이라면 실행
         alert("비밀번호를 다시 입력해주세요.");
      }
      else if (json['result'] == "success"){            // result 값이 "success" 이라면 실행
         // 로그인 성공 token 생성
         localStorage.setItem('modakbul_token', json['access_token']);
         alert("로그인 성공");
         /* 로그인 성공 시, 취할 액션 집어넣기 */
      }
      else {
         alert("일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.");
      }
   });
}

function getuserinfo()
{
    var a_jax = A_JAX('http://localhost:5000/userinfo', "GET", localStorage.getItem('modakbul_token'));
   $.when(a_jax).done(function(){
      var json = a_jax.responseJSON;
      console.log(json);
   });
}

function get_notice()
{
  var a_jax = A_JAX('http://localhost:5000/get-post/1', "GET");
   $.when(a_jax).done(function(){
      var json = a_jax.responseJSON;
      console.log(json);
   });
}