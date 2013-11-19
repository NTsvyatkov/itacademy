function validate_login(){
var login1 =   document.form.login1.value;

        if (login1 == ""){
                $(".error_login1").html("'Enter your login'").css({'color':'red'});
                $(".login1").toggleClass("errorList");
                $(".login1").click(function(){

                $(".error_login1").html("");
                $(".login1").removeClass("errorList")
                    });
            return false;
            }


var password =   document.form.password.value;

        if (password == ""){
                $(".error_password").html("'Enter your password'").css({'color':'red'});
                $(".password").toggleClass("errorList");
                $(".password").click(function(){

                $(".error_password").html("");
                $(".password").removeClass("errorList")

                   });
            return false;
            }
}