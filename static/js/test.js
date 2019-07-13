function AJAX(type_, url_, json_data)
{
    ajax_ = $.ajax({
        type: type_,
        url: url_,
        data: json_data,
        dataType : "json",
        contentType: false,
        processData: false,
        success: function(){
            alert("성공");
        },
        error: function(){
            alert("실패");
        }
    });

    return ajax_;
}

function hello()
{
    obj = new FormData();
    obj.append("name", "NB");
    obj.append("old", "23");
    obj.append("sex", "male");

    _ajax = AJAX("POST", "/info", obj);
    $.when(_ajax).done(function(){
        data = _ajax.responseJSON;
    })
}