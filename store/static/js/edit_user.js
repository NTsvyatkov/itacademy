
function validate_form_and_edit_user(){

    var login =   document.form.login.value;
    var regV_login = /^[0-9a-zA-Zа-яА-Я]+$/;
    var result_login = login.match(regV_login);
        if (login == ""){
                $(".error_login").html("User Name is required field.").css({'color':'red'});
                $(".login").toggleClass("errorList");
                $(".login").click(function(){

                $(".error_login").html("");
                $(".login").removeClass("errorList")

                     });
            return false;
            }
        else if  (!result_login)

        {
        $(".error_login").html("User Name should contain only alphanumerical characters").css({'color':'red'});
                $(".login").toggleClass("errorList");
                $(".login").click(function(){

                $(".error_login").html("");
                $(".login").removeClass("errorList")
                });
            return false;

    }
        else if (login.length > 50){
            $(".error_login").html("Field max length = 50 characters").css({'color':'red'});
                $(".login").toggleClass("errorList");
                $(".login").click(function(){

                $(".error_login").html("");
                $(".login").removeClass("errorList")
                });
            return false;

        }






 var first_name =   document.form.first_name.value;
        if (first_name == ""){
        $(".error_first_name").html("First Name is required field.").css({'color':'red'});
                $(".first_name").toggleClass("errorList");
                $(".first_name").click(function(){

                $(".error_first_name").html("");
                $(".first_name").removeClass("errorList")

                });
            return false;

    }
        else if (first_name.length > 50){
            $(".error_first_name").html("Field max length = 50 characters").css({'color':'red'});
                $(".first_name").toggleClass("errorList");
                $(".first_name").click(function(){

                $(".error_first_name").html("");
                $(".first_name").removeClass("errorList")
                });
            return false;

        }
var last_name =   document.form.last_name.value;
       if (last_name == ""){
       $(".error_last_name").html("Last Name is required field.").css({'color':'red'});
                $(".last_name").toggleClass("errorList");
                $(".last_name").click(function(){

                $(".error_last_name").html("");
                $(".last_name").removeClass("errorList")

                });
            return false;

    }
      else if (last_name.length > 50)

       {
       $(".error_last_name").html("Field max length = 50 characters").css({'color':'red'});
                $(".last_name").toggleClass("errorList");
                $(".last_name").click(function(){

                $(".error_last_name").html("");
                $(".last_name").removeClass("errorList")

                });
            return false;

    }

var password =   document.form.password.value;



       if (password.length >10){
       $(".error_password").html("Password max length = 10 characters.").css({'color':'red'});
                $(".password").toggleClass("errorList");
                $(".password").click(function(){

                $(".error_password").html("");
                $(".password").removeClass("errorList")

                });
        return false;
    }

    else if (  /\s/.test(password)  ){
       $(".error_password").html("Spaces are not allowed").css({'color':'red'});
                $(".password").toggleClass("errorList");
                $(".password").click(function(){

                $(".error_password").html("");
                $(".password").removeClass("errorList")

                });
        return false;
    }
    else if (  password.length < 4){
       $(".error_password").html("  Password should contain at least 4 characters").css({'color':'red'});
                $(".password").toggleClass("errorList");
                $(".password").click(function(){

                $(".error_password").html("");
                $(".password").removeClass("errorList")

                });
        return false;
    }
var confirm =   document.form.confirm.value;
        if (confirm != password){
        $(".error_confirm").html("Password and Confirmation should be equal.").css({'color':'red'});
                $(".confirm").toggleClass("errorList");
                $(".confirm").click(function(){

                $(".error_confirm").html("");
                $(".confirm").removeClass("errorList")

                });
            return false;
        }

var email =   document.form.email.value;
var regV_email = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,100})+$/;
var result_email = email.match(regV_email);

        if (email == ""){
        $(".error_email").html("Email is required field.").css({'color':'red'});
                $(".email").toggleClass("errorList");
                $(".email").click(function(){

                $(".error_email").html("");
                $(".email").removeClass("errorList")

                });
            return false;
        }
        else if (email.length >100)
        {   $(".error_email").html("Password max length = 100 characters.").css({'color':'red'});
                $(".email").toggleClass("errorList");
                $(".email").click(function(){

                $(".error_email").html("");
                $(".email").removeClass("errorList")

                });
            return false;
      }

        else if  (!result_email)


        {   $(".error_email").html("Invalid email format").css({'color':'red'});
                $(".email").toggleClass("errorList");
                $(".email").click(function(){

                $(".error_email").html("");
                $(".email").removeClass("errorList")

                });
            return false;
      }


var region =   document.form.region.value;

        if (region == ""){
        $(".error_region").html("You must select a region").css({'color':'red'});
                $(".region").toggleClass("errorList");
                $(".region").click(function(){

                $(".error_region").html("");
                $(".region").removeClass("errorList")

                });
            return false;
    }
 var get = location.search;
            if(get != '')
            {
	            var id = (get.substr(2));
	            id.split();
            }

    $.ajax(
{
    url: '/api/user',
    type: 'PUT',
    contentType: "application/json",
    data:JSON.stringify(
        {
            login:$('input[name="login"]').val(),
            first_name: $('input[name="first_name"]').val(),
            last_name: $('input[name="last_name"]').val(),
            password: $('input[name="password"]').val(),
            email: $('input[name="email"]').val(),
            region_id:Number( $('select#region').val()),
            role_id:Number( $('input[name=role]:checked', '#roles').val()),
            user_id:Number(id)

        }),
    success: function(data)
                    {
                       alert('User has been successfully update');
                       parent.location = 'search_user';
                    }

})

}
