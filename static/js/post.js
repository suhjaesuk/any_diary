$.ajax({
    type: 'GET',
    url: '/usertoken',
    data: {},
    async: false,
    success: function (response) {
        console.log(response['username']);


    }
});

function postDiary() {

    check_contents()

    let title = $('#title').val()
    let content = $('#content').val()
    let emoticon = $('#emoticon').val()
    let username = document.getElementById('username').innerText
    let date = new Date();

    // if(content == null || content==""){
    //     alert('일기를 입력해주세요.');
    //     document.forms[0].content.focus();
    //     return false;
    // }
    //
    // if(emoticon == "오늘의 기분" || content==""){
    //     alert('이모티콘을 선택해주세요.');
    //     document.forms[0].emoticon.focus();
    //     return false;
    // }



    $.ajax({
        type: 'POST',
        url: '/postDiary',
        data: {
            title_give: title,
            content_give: content,
            date_give: Date,
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



