$(document).ready(function () {
  list_diary('/list')
  $('#searchAll').click(function () {
    list_diary('/list')
  })
  $('#searchMine').click(function () {
    list_diary('/mylist')
  })
})