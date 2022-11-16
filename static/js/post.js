function postDiary() {
    let title = $('#title').val()
    let content = $('#content').val()
    let emoticon = $('#emoticon').val()

    let date = new Date();

    $.ajax({
        type: 'POST',
        url: '/postDiary',
        data: {
            title_give: title,
            content_give: content,
            date: Date,
            emoticon_give: emoticon
        },
        success: function (response) {
            alert(response['msg'])
            window.location.href = '/'

        }
    });
}





