function A_JAX(url, type, token, data){
    var ajax_;
    ajax_ = $.ajax({
        type: type,
        url: url,
        data: data,
        dataType : "json",
        success: function(res){
        },
        error: function(res){
            snackbar("일시적인 오류로 정보를 가져오지 못하였습니다.");
        }
    });

    $.ajaxSetup({
        beforeSend: function (xhr)
        {
            let token = localStorage.getItem('modakbul_token');
            if (token)
            {
                xhr.setRequestHeader("Authorization", "Bearer "+token);
            }
        }
    });
    return ajax_;
}

function A_JAX_FILE(url, type, token, data){
    var ajax_;
    ajax_ = $.ajax({
        type: type,
        url: url,
        data: data,
        dataType : "json",
        processData : false,
        contentType : false,
        success: function(res){
        },
        error: function(res){
            snackbar("일시적인 오류로 정보를 가져오지 못하였습니다.");
        }
    });

    $.ajaxSetup({
        beforeSend: function (xhr)
        {
            let token = localStorage.getItem('modakbul_token');
            if (token)
            {
                xhr.setRequestHeader("Authorization", "Bearer "+token);
            }
        }
    });
    return ajax_;
}