$(document).ready(function () {
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie("csrftoken");

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

  
  // LIKE POST.
  $('.like-btn').click(function(e) {
    e.preventDefault();
    let a = $(this);
    let slug = a.attr('data-slug');
    let url = `/blog/${slug}/like/`;

    $.ajax({
      url: url,
      type: 'POST',
      success: function(data, status) {
        if (data.result === 'user-not-authenticated') {
          window.location.href = data.url
        } else {
          a.html(`<i class="fa${data.post_liked ? 's':'r'} fa-heart ${data.post_liked ? 'text-danger':''}"></i> ${ data.likes } Like${ data.likes == 1 ? '' : 's'}`);
        }
      },
      error: function() {
        console.log('error')
      }
    });
  });

  // LIKE REPLY.
  $('.like-reply-btn').click(function(e) {
    e.preventDefault();
    let a = $(this);
    let id = a.attr('data-id');
    let url = `/reply/${id}/like/`;

    $.ajax({
      url: url,
      type: 'POST',
      success: function(data, status) {
        if (data.result === 'user-not-authenticated') {
          window.location.href = data.url
        } else {
          a.html(`<i class="fa${data.reply_liked ? 's':'r'} fa-heart ${data.reply_liked ? 'text-danger':''}"></i> ${ data.likes } Like${ data.likes == 1 ? '' : 's'}`);
        }
      },
      error: function() {
        console.log('error')
      }
    });
  });
});
