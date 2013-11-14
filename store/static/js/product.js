function validate_form2(){
var product_name =   document.form.product_name.value;

        if (product_name == ""){
                $(".error_product_name").html("'Name is required field.'").css({'color':'red'});
                $(".product_name").toggleClass("errorList");
                $(".product_name").click(function(){

                $(".error_product_name").html("");
                $(".product_name").removeClass("errorList")

                     });
            return false;
            }

 var price =   document.form.price.value;
        if (price == ""){
                $(".error_price").html("'Price is required field.'").css({'color':'red'});
                $(".price").toggleClass("errorList");
                $(".price").click(function(){

                $(".error_price").html("");
                $(".price").removeClass("errorList")

                });
            return false;
    }


var id =   document.form.id.value;
       if (id == ""){
       $(".error_id").html("'dimension is required field.'").css({'color':'red'});
                $(".id").toggleClass("errorList");
                $(".id").click(function(){

                $(".error_id").html("");
                $(".id").removeClass("errorList")

                });
            return false;
    }



    $.ajax({
        dataType: 'json',
        type: "POST",
        url: "/api/product",
        data:JSON.stringify({
                name:$('input[name="product_name"]').val(),
                description: $('textarea[name="description"]').val(),
                price: $('input[name="price"]').val(),
                id: $('select[name="id"]').val()
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




