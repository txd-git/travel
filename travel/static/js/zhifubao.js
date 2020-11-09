function zhifubao() {
    var token = window.localStorage.getItem('dnblog_token');
    var username = window.localStorage.getItem('dnblog_user');
    $.ajax({
        url: "/hotel/bao_pay/",
        type: "post",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(post_data),
        beforeSend: function (request) {
            request.setRequestHeader("Authorization", token);
        },
        success: function (result) {
            if (result.code==200) {
                window.location = result.pay_url
            } else {
                // alert(result.error);
                window.location.href = '/user/login'
            }
        },
        error: function (errors) {
            console.log("错误");
            console.log(errors)
        }
    })
}