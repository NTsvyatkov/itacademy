$(document).ready(function() {
    var tr = [];
    var count_tr=$('#table_size').val();
    var th = ['Item Number','Item Name','Item Description','Dimension','Price','Quantity','Price per Line'];
    var count_td= th.length-1;
    var page = 1;
    var detector;
    var counter;
    var sort_by = "product_name";
    var order_sort_by = "asc";
    var table_grid = document.getElementById('grid');

  /* Creating table of products (size = count_tr Х count_td)  */

    tr[0] = document.createElement('TR');
    table_grid.appendChild(tr[0]);
    for (var j=0; j<=count_td; j++)
    {
          tr[0].appendChild(document.createElement('TH'));
          tr[0].cells[j].innerHTML=th[j];
    }


  /* Get order id from url*/
  var pathArray = window.location.pathname.split( '/' );
  var order_id = pathArray[2];


  function create_grid(count_tr, count_td)
    {
        for (var i=1; i<=count_tr;i++ )
        {
            tr[i] = document.createElement('TR');
            table_grid.appendChild(tr[i]);
            tr[i].id=i;
            for (var j=0; j<=count_td; j++)
             {
              tr[i].appendChild(document.createElement('TD'));
             }
        }
       $( "tr:even" ).css( "background-color", "#E8E8E8" );
    }

   create_grid(count_tr,count_td);
  /*End of creating table*/


 function deleting_grid()
  {
    for (var n=table_grid.rows.length ; n>=2; n--)
      {
       table_grid.removeChild(table_grid.childNodes[n]);
      }

  }

  function grid_pagination()
   {
    $.ajax({
        dataType: "json",
        url: '/api/order_details/?page='+page+'&table_size='+count_tr+'&order_id='+order_id+'&sort_by='+sort_by+
                '&order_sort_by='+order_sort_by,
        type: 'GET',
        success: function(json)
        {
           ajax_success(json);

           all_items=(json.all_items);
           items_per_page=(json.items_per_page);
           pages_amount = Math.ceil(all_items/items_per_page);
           if (pages_amount <1){pages_amount = 1}
           $("#page").text(page);
           $("#pages_amount").text(pages_amount);

           if (page==1){
               $('#prev, #first').prop('disabled', true);
               $('#prev, #first').addClass("button_disable");
           } else {
               $('#prev, #first').prop('disabled', false);
               $('#prev, #first').removeClass("button_disable");
           }

           if (page==pages_amount){
               $('#next, #last').prop('disabled', true);
               $('#next, #last').addClass("button_disable");
           } else {
               $('#next, #last').prop('disabled', false);
               $('#next, #last').removeClass("button_disable");
           }

         }
      })
     }

 function ajax_success(json)
  {
           deleting_grid();
           create_grid(json.orders.products.length,count_td);

           /*Create table with new products list */
           var k=0;
            for (var product_k in json.orders.products)
                {
                 k++;

                 tr[k].cells[0].innerHTML = json.orders.products[product_k].product_id;
                 tr[k].cells[1].innerHTML = json.orders.products[product_k].product_name;
                 tr[k].cells[2].innerHTML = json.orders.products[product_k].product_description;
                 tr[k].cells[3].innerHTML = json.orders.products[product_k].product_dimension;
                 tr[k].cells[4].innerHTML = "$" + json.orders.products[product_k].product_price;
                 tr[k].cells[5].innerHTML = json.orders.products[product_k].product_quantity;
                 tr[k].cells[6].innerHTML = "$" + (json.orders.products[product_k].product_price_per_line);
                }
          $('#customer_name').text(json.orders.customer_name);
          $('#customer_type').text(json.orders.customer_type);
          $('#order_number').text(json.orders.order_id);
          $('#total_amount').text("$" + json.orders.total_price);
          $('#quantity_of_items').text(json.orders.quantity_of_items);
          $('#assignee').text(json.orders.assignee);
          $('#date_of_ordering').text(formatDate(json.orders.order_date));
            if (json.orders.preferable_delivery_date == "None"){$('#preferable_delivery_date').text("Wasn't defined by customer")}
            else {$('#preferable_delivery_date').text(formatDate(json.orders.preferable_delivery_date));}
          $('#status').text(json.orders.order_status);
          $('#delivery_date').text(formatDate(json.orders.delivery_date));
          if (!(json.orders.gift)){
              $('#gift').text("No");
          }
          else{
              $('#gift').text("Yes");
          }

          var session_role = json.orders.session_role;
          var order_status = json.orders.order_status



     if (session_role=="Merchandiser"){
         if (order_status !== "Delivered") {
         $('#status').replaceWith('<input type="checkbox" id="order_status" value="Delivered"> Delivered<br>');
         $('#delivery_date').replaceWith( '<input type="text" id="datepicker">' );
         $("#datepicker").attr('disabled', true);
         $('#gift').replaceWith( '<input type="checkbox" id="gift_value" value="Gift"><br>' );
          }
         else {
             $("#button").remove();
         }

         if (json.orders.gift===true){
              $('#gift_value').attr('checked', true);
         }

     }
     if (session_role=="Customer"){
         $("#button").remove();
         if (json.orders.order_status !== "Delivered"){
                 $('#delivery_date').text("Not delivered")
             }

     }
     $("#order_status").click(function(){
         if ($('#order_status').prop('checked')!==true) {
             $("#datepicker").attr('disabled', true);
         }
         else {
             $("#datepicker").attr('disabled', false);
             $("#datepicker").val(CurrentDate());
         }
     });

    /*Add date picker*/
    $("#datepicker .ui-datepicker-calendar").prop("display","block");
    $("#datepicker").datepicker();

     /*Function for validation delivery date */
     function validateDeliveryDate(){
//         var a = $("#date_of_odering").innerText;
//         alert(a);
//         alert(Date.parse(a));
     var dateOfOrdering = Date.parse(formatDate(json.orders.order_date));
     var objDateOfOrdering = new Date(dateOfOrdering);
     var deliveryDate = Date.parse($("#datepicker").val());
     var objDeliveryDate = new Date(deliveryDate);
     var re = /(0[1-9]|1[012])[\/](0[1-9]|[12][0-9]|3[01])[\/](20)\d\d/;
     if ($('#order_status').prop('checked')===true){
         if (re.exec($("#datepicker").val()) && objDeliveryDate >= objDateOfOrdering) {
             return true
         }
         else {
             return false
           }
     }
     else {
         return true
     }
     }

    function send_data() {
    $.ajax({

        type: "PUT",
        url: "/api/order_details/",
        data:JSON.stringify({
                id: order_id,
                gift:$('#gift_value').prop('checked'),
                status: $('#order_status').prop('checked'),
                delivery_date: $("#datepicker").val()
               }),
        contentType: 'application/json;',
        success : function (resp){
            alert('Order has been successfully updated');
            location.reload(); }
    });
  }

  /*Event on click Save button*/
     $("#save").click(function(){
      if (validateDeliveryDate() === false) {
           alert("Invalid delivery date!");
      }
      else {
          send_data();
      }
     });

  /*Event on click Cancel button*/
        $("#cancel").click(function(){
            window.location.href = '/manage_orders'
        });

  }

    if (page==1) {grid_pagination()}


    /*Function for format date to mm-dd-yyyy */
    function formatDate(date){
        var date_array = date.split('-');
        return date_array[1] + '/' + date_array[2] + '/' + date_array[0]
    }


    /*Function to get current date in mm-dd-yyyy */
    function CurrentDate(){
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1;
        var yyyy = today.getFullYear();
        if(dd<10){dd='0'+dd}
        if(mm<10){mm='0'+mm}
        today = mm+'/'+dd+'/'+yyyy;
        return today
      }


  /*Sorting in columns */
  $("th").click(function(){
      $("th").removeClass("asc desc");
      var entry = this.innerHTML;

      switch (entry)
          {
          case "Item Number":
            sort_by="product_id";
            break;
          case "Item Name":
            sort_by="product_name";
            break;
          case "Item Description":
            sort_by="product_description";
            break;
          case "Dimension":
            sort_by="product_dimension";
            break;
          case "Price":
            sort_by="price";
            break;
          case "Quantity":
            sort_by="quantity";
            break;
          case "Price per Line":
            sort_by="product_price_per_line";
            break;
          }
      if (detector===entry){
          counter+=1;
      }
      else {
          detector=entry;
          counter=0;
      }
      if (counter%2==0){
          order_sort_by = "asc";
          $(this).addClass("asc")
      }
      else {
          order_sort_by = "desc";
          $(this).addClass("desc")
      }
        grid_pagination();
    }
    );


  /*Pagination buttons events*/
    $('#next').click(function(){
        if (page*items_per_page>=all_items){page=page}
        else {page=page+1}
        grid_pagination()
    });

    $('#prev').click(function(){
    page=page-1;
        if (page<=1){
        page=1;
    }
    grid_pagination()
    });

    $('#first').click(function(){
    page=1;
    grid_pagination()
    });

    $('#last').click(function(){
        page=pages_amount;
        grid_pagination()
    });

  /* Change table size select event*/

    $('#table_size').change(function() {
        $("th").removeClass("asc desc");
        page=1;
        count_tr=$('#table_size').val();
        pages_amount = $("#table_size option:selected").val();
        grid_pagination();
    });
});
