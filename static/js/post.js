    $.ajax({
       type: 'GET',
       url: '/usertoken',
       data: {},
       async : false,
       success: function (response) {
           console.log(response['username']);


       }
   });

function postDiary() {
    let title = $('#title').val()
    let content = $('#content').val()
    let emoticon = $('#emoticon').val()
    let username = console.log(response['username']);


    let date = new Date();



    $.ajax({
        type: 'POST',
        url: '/postDiary',
        data: {
            title_give: title,
            content_give: content,
            date: Date,
            emoticon_give: emoticon,
            username_give : username

        },

        success: function (response) {
            alert(response['msg'])
            window.location.href = '/'

        }
    });
}







