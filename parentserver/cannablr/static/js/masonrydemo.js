var posts = document.querySelectorAll('.grid_4');

$(document).ready(function() {
  $('.container').masonry({
   itemSelector: '.grid_4',
   isFitWidth: true,
   gutter: 3
  }).imagesLoaded( posts, function() {
   $('.container').masonry('reloadItems');
  });

});