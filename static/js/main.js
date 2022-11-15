$(document).ready(function () {
  $('.gridContainer').empty()
  show_diary()
})

function show_diary() {
  $.ajax({
    type: 'GET',
    url: '/list',
    data: {},
    success: function (response) {
      let rows = response['show_diary']
      for (let i = 0; i < rows.length; i++) {
        let contentId = rows[i]['contentId']
        let title = rows[i]['title']
        let content = rows[i]['content']
        let username = rows[i]['username']
        let date = rows[i]['date']
        let emoticon = rows[i]['emoticon']
        let temp_html = `
        <div class="item" onclick="location.href ='/contentId=${contentId}'" >
        <h3 class="title">${title}</h3>
        <hr><br>
        <p class="content">${content}</p><br>
        <p class="username">${username}</p>
        <p class="date">${date}</p>
        <p class="emoticon">${emoticon}</p>
    </div>
      `
        $('.gridContainer').prepend(temp_html)
      }
    }
  })
}
