$.ajax({
    type: 'GET',
    url: '/usertoken',
    data: {},
    async: false,
    success: function (response) {
        console.log(response['username']);
         console.log(response['userId']);
         $('#userId').val(response['userId'])
    }
});

function postDiary() {

    check_contents()


    let title = $('#title').val()
    let content = $('#content').val()
    let emoticon = $('input[name="chk_info"]:checked').val()
    let userId = $('#userId').val()
    let username = document.getElementById('username').innerText
    let date = new Date();


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



function check_contents() {

    let content = document.getElementById("content");

    if (content.value == "") {
        alert("내용을 입력해주세요.");

        return false;

    }

}



