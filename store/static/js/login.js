function validate_login(){
var name = document.form.name.value;

        if (name == ""){
                $(".error_name").html("Enter your login ").css({'color':'red'});
               // $(".name").toggleClass("errorList2");
                $(".name").click(function(){

                $(".error_name").html("");
                $(".name").removeClass("errorList2")
                    });
            return false;
            }


var password = document.form.password.value;

        if (password == ""){
                $(".error_password").html("Enter your password").css({'color':'red'});
               // $(".password").toggleClass("errorList2");
                $(".password").click(function(){

                $(".error_password").html("");
                $(".password").removeClass("errorList2")

                   });
            return false;
            }

var c = $("#check");


   if(c.is(":checked")){
     var u = $("#name").val();
         $.cookie("name", u, { expires: 10 });
   }
}

function load(){
   var u = $.cookie("name");

   $("#name").val(u);

}

