$(document).ready(function() {

  $(document).on('submit', 'form', function() {
    // Here you get the values:
    var todo_body = $('#todo').val();

    // OR
    // you have a simpler option:
    // var data = this.serialize();

    $.ajax({
      type: 'POST',
      data: {
        body: todo_body
      },
      // OR
      // data: data, // if you use the form serialization above
      url: "/todos",
      success: added,
      error: showError
    });
  });
});