function log_out()
{
    console.log('logging out');
    $.ajax({
        url:'/log_out',
        type:'post',
        data:{},
        success: function(resp)
        {
            window.location.href='/login';
        }
    });
}