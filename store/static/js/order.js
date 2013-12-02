
/* JQueri UI  - Datapicker options*/
	$(function() {
		$( "#expire_date" ).datepicker({
          changeMonth: true,
          changeYear: true,
          showButtonPanel: true,
          dateFormat: 'yy/mm',
          onClose: function(dateText, inst) {
            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
            $(this).datepicker('setDate', new Date(year, month, 1));
        }
		});

		$( "#start_date" ).datepicker({
          changeMonth: true,
          changeYear: true,
          disabled: true,
          showButtonPanel: true,
          dateFormat: 'yy/mm',
          onClose: function(dateText, inst) {
            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
            $(this).datepicker('setDate', new Date(year, month, 1));
        }
		});
	});
/*--------------------------*/



$(document).ready(function() {
    var order_id=0;
    var maestro_card = false;
    var th = ['Product name','Description','Dimension','Price $','Quantity','Amount $','Delete'];
    var count_td= th.length-1;
    var count_tr=$('#table_size').val();
    var tr = [];
    var page = 1;
    var error_list =[];
    var table_grid = document.getElementById('grid');
    $('#issue_number').attr('readonly',true);
    $('#issue_number').css('background-color','#e2e2e2');

    /* Change table size <select> event*/
    $('#table_size').change(function () {
       $( "#table_siz option:selected" ).each(ajax_pull('GET','data'))
     })
    /*---------------------------------*/

    /*Default value for select card type*/
    $('#credit_card_options').val(1);
    /*----------------------------------*/

  /* Creating table of products (size = count_tr Х count_td)  */
    var tr1 = document.createElement('TR');
    table_grid.appendChild(tr1);
    for (var j=0; j<=count_td; j++)
    {
          tr1.appendChild(document.createElement('TH'));
          tr1.cells[j].innerHTML=th[j];
    }
   create_grid(count_tr,count_td);
  /*----------------End of creating table-------------------------------*/

  /* Ajax function for all-  put and all - get methods*/
   function ajax_pull(type_options,data){
       $.ajax({
        dataType: "json",
        url: '/api/order_product/?page='+page+'&table_size='+count_tr,
        type: type_options,
        contentType: "application/json",
        data:data,
        success: function(json)
        {
          if (type_options == 'GET'){
           ajax_success(json);
           include_pagination(page,json);
          }
          else {
              alert('Order successfully issued');
              window.location.replace("/my_orders");
              ajax_pull('GET','data');
              }
         },
         error: function(e)
          {
            error = JSON.parse(e.responseText);
             alert(error.message);
          }
      })
   }
/*------------------------------------------*/
 ajax_pull('GET','data');

 /*-------------Update quantity in row------------------*/
 function update_quantity(json_data,object_quantity,object_amount,old_quantity,price,quantity){
       $.ajax({
        dataType: "json",
        url: '/api/update/',
        type: 'PUT',
        contentType: "application/json",
        data:json_data,
        success: function(json)
          {
             var sum = +price*+quantity;
             object_amount.text(sum.toFixed(2));
             $('#total_amount').text('Total amount: ' + get_total_amount().toFixed(2)+'$');
          },

        error: function(e)
          {
            error = JSON.parse(e.responseText);
            alert(error.message);
            object_quantity.val(old_quantity);
          }
      })
   }
/*--------------------------------------------------*/


  function delete_id(product_id, dimension_id,grid_length)
  {
   $.ajax({
       dataType: "json",
        url: '/api/order_product/'+product_id+'/'+order_id+'/'+dimension_id,
        type: 'DELETE',
        contentType: "application/json",
        success: function(json)
                    {
                      if (json.message == 'success')
                        {
                          alert('The product has been successfully deleted from the cart');
                           /* checking that grid is not empty*/
                          if (grid_length==1)
                           {
                               if (page!=1)
                                {
                                    page=page-1;
                                }
                           }
                            /*--------------------------------*/
                            ajax_pull('GET','data');
                        }
                        else
                         alert (json.message);
                    },

        error: function(e)
                    {
                       error = JSON.parse(e.responseText);
                       alert(error.message);
                    }

  })
 }
 /*Function ajax_success parse Json and add values in table - grid  */
  function ajax_success(json){
           deleting_grid();
           var grid_length=json.order.length;
           create_grid(grid_length,count_td);
           var k=0;
           var amount=0;
           var input;
           var tr;
           /*Create table with new order_products list */
            for (var product_k in json.order)
               {
                 k++;
                 tr=table_grid.rows[k];
                 order_id=json.order[product_k].order_id;
                 product_name =json.order[product_k].name;
                 id_product =json.order[product_k].id;
                 tr.cells[0].innerHTML =product_name;
                 tr.cells[1].innerHTML = json.order[product_k].description;
                 tr.cells[2].innerHTML = json.order[product_k].dimension +
                         '<input class="dimension" value="'+json.order[product_k].dimension_id+'" type="hidden">'+
                         '<input class="old_quantity" value="'+json.order[product_k].quantity+'" type="hidden">';

                 tr.cells[3].innerHTML = "<span class='price'>"+json.order[product_k].price.toFixed(2)+"</span>";

                 input = "<input type='text' class='quantity' value='"+json.order[product_k].quantity+"'\
                        alt='"+json.order[product_k].id+"' style='width:60px'>\
                        <img  alt='refresh' class='update_amount' src='static/images/refresh_32.png'> \
                         <b class='error_div'></b>";

                 tr.cells[4].innerHTML = input;
                 if (json.order[product_k].quantity) quant= Math.round(json.order[product_k].quantity); else quant= 0;
                 amount= (+json.order[product_k].price * +quant).toFixed(2);
                 tr.cells[5].innerHTML = "<span class='amount'>"+amount+"</span>";
                 tr.cells[6].innerHTML = "<img src='static/images/delete.png' class='delete_img'\
                 id='"+product_name+"' alt=" + json.order[product_k].id + " >";
               }
                $('#total_amount').text('Total amount: ' + get_total_amount().toFixed(2)+'$');
            /*--------------------------------End creating table------------------------------------*/

                $('.delete_img').click(function(){
                  var tr= $(this).closest('tr');
                  var dimension_id = tr.children('td').children('.dimension').val();
                  var product_id = this.alt;
                  if(confirm('Are you sure that you want to remove '+ this.id +' from the cart?'))
                  {
                    delete_id(product_id,dimension_id,grid_length);
                   }
                 })

                $('tr img.update_amount').click(function(){
                   var tr= $(this).closest('tr');
                   var price = tr.children('td').children('.price').text();
                   var dimension_id = tr.children('td').children('.dimension').val();
                   var old_quantity = tr.children('td').children('.old_quantity').val();
                   var product_id=tr.children('td').children('.delete_img').attr('alt');
                   var sum=0;
                   var quantity = Math.round($(this).prev().val());
                   var object_quantity=$(this).prev();
                   var object_amount =tr.children('td').children('.amount');
                   if(!(quantity/quantity)||(quantity==0)){  /*Check on numeric */
                      $(this).next('.error_div').empty();
                      $(this).next('.error_div').html('Quantity should be numeric and not 0');
                      $(this).prev().val(old_quantity);
                     }
                    else{
                     $(this).next('.error_div').empty();
                       json_value = JSON.stringify({'quantity':quantity,'product_id':product_id,
                                                   'dimension_id':dimension_id, 'price':price,
                                                   'order_id' :order_id });
                       update_quantity(json_value,object_quantity,object_amount,old_quantity,price,quantity);
                     }
                })


  }
/*----------------------------END of ajax_success ------------------------------------*/


  function get_total_amount()
  {
   var total =0;
   for( var i=0, total=0; i<$('.amount').size(); i++)
   {
    total = +$('.amount:eq('+i+')').text() + +total;
   }
   return total;
  }


  $('#add_order').click(function(){

     var error='';
     var no_error = true
     var clear_list;
     var object1;
    /* Clear error and border-color*/
      if(error_list)
      {
          for (i in error_list)
           {
             object1=error_list[i].id;
             object1.css('border-color','#999');
             object1.next('.error_div').remove();
           }
          error_list=[];
      }
     /*---------------------------------*

      /* String length validation */
       if  (($('#input_address').val().length >50) || ($('#input_address').val().length == 0))
       {
        no_error = false;
        error ='Address string should be less then 50 characters , but not 0 character';
        error_list.push({id:$('#input_address'), error:error});
       }
       if  ($('#input_comments').val().length >1500)
       {
        no_error = false;
        error ='Comment string should be less then 1500 characters';
        error_list.push({id:$('#input_comments'), error:error});
       }

       for( var i=0, total=0, k=0; i<$('.quantity').size(); i++)
        {
          quantity = $('.quantity:eq('+i+')').val();

          if((!(quantity/quantity)||(quantity==0)) && k != 1 )
          {  /*Check on numeric */
              error = 'Quantity should be numeric and not 0';
              k= 1;
              no_error = false;
              error_list.push({id:$('#order_error'), error:error});
          }
        }

      /*-----------End of Strings length validation---------*/

      /*Credit card numbers validation*/
       r_e=/^[0-9]{16}$/;
       credit_number = $('#credit_card_number').val();

       if (r_e.test(credit_number)){}
       else
       {
         no_error = false;
         error = 'The credit card number should be a 16-digit number.';
         error_list.push({id: $('#credit_card_number'), error:error});
       }

       r_e_ccv2=/^[0-9]{3}$/;
       cvv2_number = $('#cvv2_number').val();

      if (r_e_ccv2.test(cvv2_number)) {}
      else
       {
          no_error=false;
          error='The CVV2 number should be a 3-digit number.';
          error_list.push({id:$('#cvv2_number'), error:error});
       }

      issue_number =$('#issue_number').val();
      if  ((maestro_card == true) && (issue_number ))
      {
       r_e_issue_number=/^[0-9]{1}$/;
       if (r_e_issue_number.test(issue_number)){}
       else
       {
         no_error=false;
         error='Issue number format is wrong. it should be one digit or none!';
         error_list.push({id:$('#issue_number'), error:error});
       }
      }

      /*Credit card date validation*/

      date_expire= $('#expire_date').val().replace('/', '-')+'-01';

       if (!Date.parse(date_expire))
         {
             no_error = false;
             error='Expire date have wrong format, please use calendar';
             error_list.push({id:$('#expire_date'), error:error});
         }

      if (maestro_card == true)
      {
          date_start= $('#start_date').val().replace('/', '-') + '-01';

         if (Date.parse(date_start) > Date.parse(date_expire))
         {
             no_error = false;
             error='Start date of card can not be more then Expire date';
             error_list.push({id:$('#start_date'), error:error});
         }
          if (!Date.parse(date_start))
         {
             no_error = false;
             error='Start date have wrong format, please use calendar';
             error_list.push({id:$('#start_date'), error:error});
         }

      }

      /*--------------------End of Credit card validation----------------------*/
       if (no_error){

          /*Clear error message*/
         $('.error_div').empty();
          /*-----------------*/

         /*add all quantity and product_id in array */
         var product_arr=[];
         for( var i=0, total=0; i<$('.quantity').size(); i++)
         {
         product_arr[i]= {'quantity':+$('.quantity:eq('+i+')').val(),'product_id':+$('.quantity:eq('+i+')').attr('alt'),
                          'dimension_id':$('.dimension:eq('+i+')').val()}
         }
        /*------------------*/

         form_value = { order_id:order_id, delivery_type:$('#delivery_options').val(),
                        delivery_address: $('#input_address').val(), comment:$('.comments_area').val(),
                        credit_card_options:$('#credit_card_options').val(),
                        credit_card_number:$('#credit_card_number').val(),
                        cvv2_number:$('#cvv2_number').val(), expire_date:$('#expire_date').val(),
                        start_date:$('#start_date').val(), issue_number:$('#issue_number').val(),
                        product_quantity:product_arr};

         /* Json for put on server*/
         json_value = JSON.stringify(form_value);
         /*-----------------------*/
         ajax_pull('PUT',json_value);
       }
        else
        {
            $('.product_filter_in .error_div').empty();
           for (i in error_list)
           {
             object1=error_list[i].id;
             object1.closest('div').append('<p class=error_div>'+error_list[i].error+'');
             object1.css('border-color','#b81900');

           }

        }
   })
 /* Car select-or event change*/

  $('#credit_card_options').change(function () {
      if ($('#credit_card_options').val() != 4)
      {
         $('#start_date').datepicker( "option", "disabled", true );
         $('#issue_number').attr('readonly',true);
         $('#issue_number').css('background-color','#e2e2e2');

      }
      else
      {
          $('#start_date').datepicker( "option", "disabled", false );
          $('#issue_number').attr('readonly',false);
          $('#issue_number').css('background-color','white');
          maestro_card = true;

      }
  })

 /*-----------------------------------*/


  /*Pagination buttons events*/

   $('#next').click(function(){
     if (page*records_per_page>=records_amount){page=page}
     else
     {
         page=page+1;
     }
     ajax_pull('GET','data');
    });

    $('#prev').click(function(){
      page=page-1;
      if (page<=1)
      {
       page=1;
      }
      ajax_pull('GET','data');
    });

    $('#first').click(function()
    {
     page=1;
     ajax_pull('GET','data');
    });

    $('#last').click(function()
    {
     page=pages_amount;
     ajax_pull('GET','data');
    });
   /*------------------------------------*/

 /* What is this CVV2 --- alert  */
  $('#cvv2_info').click(function()
  {

    alert('The CVV2 code stands for Card Verification Value 2. The CID code stands for Card Identification.'+
          'It is a security feature on credit cards used to improve the security of transactions. It consists of ' +
          'a 3 or 4 digit number printed, but not raised, on the back of the credit card.');
  })
 /*---------------------------*/

})
