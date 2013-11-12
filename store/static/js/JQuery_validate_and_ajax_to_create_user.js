
function validate_form(){
var user_name =   document.form.login.value;

        if (user_name == ""){
                $(".error_user_name").html("'User Name is required field.'").css({'color':'red'});
                $(".user_name").toggleClass("errorList");
                $(".user_name").click(function(){

                $(".error_user_name").html("");
                $(".user_name").removeClass("errorList")

                     });
            return false;
            }
        else if (user_name.length > 50){
            $(".error_user_name").html("field max length = 50 characters").css({'color':'red'});
                $(".user_name").toggleClass("errorList");
                $(".user_name").click(function(){

                $(".error_user_name").html("");
                $(".user_name").removeClass("errorList")
                });
            return false;

        }
        else {
var regV_user_name = /^[0-9a-zA-Zа-яА-Я]+$/;
var result_user_name = user_name.match(regV_user_name);
        if(!result_user_name){
        $(".error_user_name").html("'User Name should contain only alphanumerical characters'").css({'color':'red'});
                $(".user_name").toggleClass("errorList");
                $(".user_name").click(function(){

                $(".error_user_name").html("");
                $(".user_name").removeClass("errorList")
                });
            return false;

    }

        }

 var first_name =   document.form.first_name.value;
        if (first_name == ""){
        $(".error_first_name").html("'First Name is required field.'").css({'color':'red'});
                $(".first_name").toggleClass("errorList");
                $(".first_name").click(function(){

                $(".error_first_name").html("");
                $(".first_name").removeClass("errorList")

                });
            return false;
    }


var last_name =   document.form.last_name.value;
       if (last_name == ""){
       $(".error_last_name").html("'Last Name is required field.'").css({'color':'red'});
                $(".last_name").toggleClass("errorList");
                $(".last_name").click(function(){

                $(".error_last_name").html("");
                $(".last_name").removeClass("errorList")

                });
            return false;
    }

var password =   document.form.password.value;
       if (password == ""){
       $(".error_password").html("'Password is required field.'").css({'color':'red'});
                $(".password").toggleClass("errorList");
                $(".password").click(function(){

                $(".error_password").html("");
                $(".password").removeClass("errorList")

                });
            return false;
    }
       else if (password.length >20){
       $(".error_password").html("'Password max length = 20 characters.'").css({'color':'red'});
                $(".password").toggleClass("errorList");
                $(".password").click(function(){

                $(".error_password").html("");
                $(".password").removeClass("errorList")

                });
        return false;
    }
var confirm =   document.form.confirm.value;
        if (confirm != password){
        $(".error_confirm").html("'Password and Confirmation should be equal.'").css({'color':'red'});
                $(".confirm").toggleClass("errorList");
                $(".confirm").click(function(){

                $(".error_confirm").html("");
                $(".confirm").removeClass("errorList")

                });
            return false;
        }

var email =   document.form.email.value;
var regV_email = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,})+$/;
var result_email = email.match(regV_email);
        if (email == ""){
        $(".error_email").html("'Email is required field.'").css({'color':'red'});
                $(".email").toggleClass("errorList");
                $(".email").click(function(){

                $(".error_email").html("");
                $(".email").removeClass("errorList")

                });
            return false;
        }
         else {


        if (!result_email){   $(".error_email").html("'Invalid email format'").css({'color':'red'});
                $(".email").toggleClass("errorList");
                $(".email").click(function(){

                $(".error_email").html("");
                $(".email").removeClass("errorList")

                });
            return false;
      }

    }
var region =   document.form.region.value;

        if (region == ""){
        $(".error_region").html("'You must select a region'").css({'color':'red'});
                $(".region").toggleClass("errorList");
                $(".region").click(function(){

                $(".error_region").html("");
                $(".region").removeClass("errorList")

                });
            return false;
    }





    $.ajax({
        dataType: 'json',
        type: "POST",
        url: "/user",
        data:JSON.stringify({
                login:$('input[name="login"]').val(),
                first_name: $('input[name="first_name"]').val(),
                last_name: $('input[name="last_name"]').val(),
                password: $('input[name="password"]').val(),
                email: $('input[name="email"]').val(),
                region_id: $('#region').val(),
                role_id: $( 'input:radio[name=role_id]:checked' ).val()
               }),
        contentType: 'application/json;',


        success: function(data){

      var view =   $("#result").text(data.result);
      var view = data.length,
        element = null;
            for (var i = 0; i < view; i++) {
        element = arr[i];

}


                                }
                     });






















}




