function sign_up()
{
    var first_name_value=$("#first_name").val();
    var second_name_value=$("#second_name").val();
    var phone_number_value=$("#phone_number").val();
    var email_value=$("#email").val();
    var password_value=$("#password").val();
    var birthday_value=$("#birthday").val();
    $.ajax({
        url:'/user',
        type:'post',
        data:{'first_name':first_name_value,
            'second_name':second_name_value,
            'birthday':birthday_value,
            'phone_number':phone_number_value,
            'email':email_value,
            'password':password_value,
        },
        success: function(resp)
        {
            window.location.href='/login';
            console.log(resp);
        }
    });
}