$.ajax({
    type: 'GET',
    url: '/usertoken',
    data: {},
    async: false,
    success: function (response) {
        console.log(response['username']);
        console.log(response['userId']);
        $('#userId').val(response['userId'])
        $('#username').val(response['username'])
    }
});

function postDiary() {
    let check_content = document.getElementById("content");
    let title = $('#title').val()
    // let content = $('#content').val().replace(/\n/g, "<br>")
    let content = $('#content').val()
    let emoticon = $('input[name="chk_info"]:checked').val()
    let userId = $('#userId').val()
    let username = $('#username').val()
    // let username = document.getElementById('username').innerText
    let date = new Date();

    if (check_content.value == "") {
        alert("내용을 입력해주세요.");
        return false;
    } else {
        check_contents()
        $.ajax({
            type: 'POST',
            url: '/postDiary',
            data: {
                title_give: title,
                content_give: content,
                date_give: Date,
                userId_give: userId,
                emoticon_give: emoticon,
                username_give: username
            },

            success: function (response) {
                alert(response['msg'])
                window.location.href = '/'

            }
        });
    }
}


function check_contents() {
    let check_content = document.getElementById("content");
    if (check_content.value == "") {
        alert("내용을 입력해주세요.");
        return false;
    }
}



