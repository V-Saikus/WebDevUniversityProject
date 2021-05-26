function login()
{
    var phone_number_value=$("#phone_number").val();
    var password_value=$("#password").val();
    $.ajax({
        url:'/login',
        type:'post',
        data:{'phone_number':phone_number_value,
            'password':password_value},
        success: function(resp)
        {
            window.location.href='/audiences';
            console.log(resp);
        }
    });
}