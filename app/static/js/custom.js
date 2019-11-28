$(document).ready(function(){

    $(document).on('click', '#delete', function(){
        
        let deleteItem = $(this).attr('class');

        console.log(deleteItem);

        req = $.ajax({
            url: '/delete',
            type: 'POST',
            data: { id : deleteItem }            
        });

        req.done(function(data){

            $('#todoList').html(data);
        })
    })
    
    $('.updateButton').on('click',function () {
        
       let todo = $('#todoInput').val();

        req = $.ajax({
            url: '/newtodo',
            type: 'POST',
            data: { todo : todo }
        });

        req.done(function(data){

            $('#todoList').html(data);
            $('#todoInput').val('');
        })
        event.preventDefault();
    });
});