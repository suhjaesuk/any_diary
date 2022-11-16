$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: '/usertoken',
        data: {},
        async: false,
        success: function (response) {
            console.log('1. ' + response['userId'])
            $('#userId').val(response['userId'])
            //현재 로그인 된 아이디와 글쓴이의 아이디가 같다면 버튼 보이게 함
            if (response['userId'] == $('#writerId').val()) {
                $('.buttons').show();
            } else {
                $('.buttons').hide();
            }
        }
    });

    let contentId = $('#contentId').val();
    let userId = $('#userId').val();
    console.log('contentId ' + contentId)
    console.log('userId ' + userId)
    $.ajax({
        type: 'POST',
        url: '/searchLike',
        data: {userId: userId, contentId: contentId},
        success: function (response) {

            if (response['click'] == false) {
                $('.likeClick').text('🤍')
            } else {
                $('.likeClick').text('❤')
            }
            $('#likeCount').text(response['count'])
        }
    });
});


$('.likeClick').on('click', function () {

    let contentId = $('#contentId').val();
    let userId = $('#userId').val();
    let liked = $('.likeClick').text();
    console.log('liked : ' + liked)
    let url = '';

    if (liked == "❤") {
        url = '/delLike';
    } else {
        url = '/addLike';
    }
    console.log(url)
    //db의 like값 변경
    $.ajax({
        type: 'POST',
        url: url,
        data: {userId: userId, contentId: contentId},
        async: false,
        success: function (response) {
        }
    });

    //like값이 몇개인지 재확인
    $.ajax({
        type: 'POST',
        url: '/searchLike',
        data: {userId: userId, contentId: contentId},
        success: function (response) {
            console.log(response)
            if (response['click'] == false) {
                $('.likeClick').text('🤍')
            } else {
                $('.likeClick').text('❤')
            }
            $('#likeCount').text(response['count'])
        }
    });

})


/*
$('#modiComplete').click(function () {
    let title = $('#title').val();
    let content = $('#content').val();
    let emoticon = $('#emoticon').val();
    let date = $('#date').val();
    let contentId = $('#contentId').val();
    $.ajax({
        type: 'POST',
        url: '/modiDiary',
        data: {
            contentId: contentId,
            title: title,
            content: content,
            date: date,
            emoticon: emoticon
        },
        success: function (response) {
            alert('수정완료')
            window.location.replace('/')
        }
    });
})*/
/*
$('#contentDel').click(function () {
    let contentId = $('#contentId').val();

    $.ajax({
        type: 'POST',
        url: '/deleteContent',
        data: {contentId: contentId},
        success: function (response) {
            alert(response['state'])
            window.location.replace('/')
        }
    });

})

*/