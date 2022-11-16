<<<<<<< HEAD
=======
$(document).ready(function () {
  $('.gridContainer').empty()
  list_diary()
})

function list_diary() {
  $.ajax({
    type: 'GET',
    url: '/list',
    data: {},
    success: function (response) {
      let rows = response['list_diary']
      for (let i = 0; i < rows.length; i++) {
        let contentId = rows[i]['contentId']
        let title = rows[i]['title']
        let content = rows[i]['content']
        let username = rows[i]['username']
        let date = rows[i]['date']
        let emoticon = rows[i]['emoticon']
        let temp_html = `
        <div>
        {% if username %}
        <div class="item" onclick="location.href ='/contentId=${contentId}'" >
        {% endif %}
        {% if not username %}
        <div class="item" onclick="location.href ='/login'" >
        </div>
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
>>>>>>> a2c9d827f440d7bd00d76732e9af20c6393085b4
