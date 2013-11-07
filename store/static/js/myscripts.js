$(document).ready(function(){

    $("#info").validate({
        
       rules:{ 
        
            name:{
                required: true,
                maxlength: 100
            },
            
            price:{
                required: true

            },
            id:{
                required: true
           }
       },
       
       messages:{
        
            name:{
                required: "Name is required field",
                maxlength: "max length = 100"
            },
            
            price:{
                required: "Price is required field",
                number: "Price value should be a valid decimal"
            },
            id:{
               required: "Dimension is required field"
           }
        
       }
        
    });



}); //end of ready
