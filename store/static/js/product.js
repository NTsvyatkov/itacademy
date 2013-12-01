function validate_form2(){
var product_name =   document.form.product_name.value;

        if (product_name == ""){
                $(".error_product_name").html("'Name is required field'").css({'color':'red'});
                $(".product_name").toggleClass("errorList2");
                $(".product_name").click(function(){

                $(".error_product_name").html("");
                $(".product_name").removeClass("errorList2")

                     });
            return false;
            }

var price =   document.form.price.value;
var regV_price = /^\d+(?:\.\d{0,2})?$/;
var result_price = price.match(regV_price);
        if (price == ""){
        $(".error_price").html("'Price is required field'").css({'color':'red'});
                $(".price").toggleClass("errorList2");
                $(".price").click(function(){

                $(".error_price").html("");
                $(".price").removeClass("errorList2")

                });
            return false;
        }
         else {


        if (!result_price){   $(".error_price").html("'Price has invalid decimal value'").css({'color':'red'});
                $(".price").toggleClass("errorList2");
                $(".price").click(function(){

                $(".error_price").html("");
                $(".price").removeClass("errorList2")

                });
            return false;
      }

    }




    $.ajax({
        dataType: 'json',
        type: "POST",
        url: "/api/product",
        data:JSON.stringify({
                name:$('input[name="product_name"]').val(),
                description: $('textarea[name="description"]').val(),
                price: $('input[name="price"]').val()
               }),
                contentType: 'application/json;',
                success : function (resp){
                            alert('The product has been successfully added')
                }
    });  }






