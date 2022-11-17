function login() {
    $.ajax({
        type: "POST",
        url: "/api/login",
        data: {id_give: $('#userid').val(), pw_give: $('#userpw').val()},
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token']);
                alert('로그인 완료!')
                window.location.href = '/'
            } else {
                alert(response['msg'])
            }
        }
    })
}