

$('.likeClick').click(function () {
    let contentId = $('#contentId').val();
    let userId = $('#userId').val();
    let liked = $('.likeClick').text();
    console.log('liked : '+liked)
    let url = '';

    console.log(contentId + ' ::: ' + userId)
    if(liked == "❤"){
        url = '/delLike';
    }else{
        url = '/addLike';
    }

    $.ajax({
        type: 'POST',
        url: url,
        data: {userId: userId, contentId : contentId},
        success: function (response) {
        }
    });

    $.ajax({
        type: 'GET',
        url: '/searchLike',
        data: {},
        success: function (response) {
            console.log(response)
            if(response['click'] == false){
                $('.likeClick').text('🤍')
            }else{
                $('.likeClick').text('❤')
            }
            $('#likeCount').text(response['count'])
        }
    });
})


$('#contentModi').click(function(){

})

$('#contentDel').click(function(){
    let contentId = $('#contentId').val();
    /*
    $.ajax({
        type: 'POST',
        url: '/deleteContent',
        data: {contentId : contentId},
        success: function (response) {

        }
    });*/
    alert('del click')

})

