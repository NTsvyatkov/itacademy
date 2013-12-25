 var tr = [];
            $(document).ready(function() {
            var count_tr=$('#table_size').val();
            var count_td=6;
            var sort_by = "order_id";
            var order_sort_by = "asc";
            var page = 1;
            var detector;
            var table_grid = document.getElementById('grid');
 /* Creating table (size = count_tr Х count_td)  */

            function createGrid(count){
                for (var i=1; i<=count;i++ ){
                    tr[i] = document.createElement('TR');
                    table_grid.appendChild(tr[i]);
                    tr[i].id=i;
                    if (i % 2 == 0) tr[i].style.background = "#E8E8E8";
                    for (var j=0; j<=6; j++){
                        tr[i].appendChild(document.createElement('TD'));
                    }
                }
            }
 /*----------------End of creating table-------------------------------*/

            function deleteGrid(){
                for (var n=table_grid.rows.length ; n>=2; n--){
                    table_grid.removeChild(table_grid.childNodes[n]);
                }
            }


            function listOrders(json){
                deleteGrid();
                createGrid(json.orders.length);

  /*-------------Create table with new orders list-------------------- */

                var grid_length = json.orders.length;
                /*Create table */
                for (var order_k in json.orders){
                    k++;
                        tr[k].cells[0].innerHTML = json.orders[order_k].order_id
                        tr[k].cells[1].innerHTML = json.orders[order_k].order_number
                        tr[k].cells[2].innerHTML = json.orders[order_k].user;
                        tr[k].cells[3].innerHTML = json.orders[order_k].orderStatus;
                        tr[k].cells[4].innerHTML = "$ "+json.orders[order_k].total_price;
                        tr[k].cells[5].innerHTML = json.orders[order_k].role;
                        tr[k].cells[6].innerHTML = "<img src='static/images/Text Edit.png' class='edit_img' alt=" +k+ ">";
                        tr[k].cells[6].abbr=k;
                        tr[k].cells[6].onclick= function()
                            {
                                window.location.replace("order/"+tr[this.abbr].cells[0].innerHTML)
                            }

                    }
                    k=0;
 /*---------------------End creating table------------------------------------*/
            }

            var k=0;
            form_value = {id : $('#name_form').val(), name : $('#product_name').val()};
            json_value = JSON.stringify(form_value);

              $('#apply_button').click(function(){
                createTableOrders()
              });

            function createTableOrders(){
                var status_options = document.getElementById('status_options').value;
                var orders_options = document.getElementById('orders_options').value;
                var name_input = document.getElementById('name_input').value;
                $.ajax({
                dataType: "json",
                url: '/api/manage_orders/?page='+page+'&table_size='+count_tr+
                '&status_option='+status_options+'&order_option='+orders_options+
                '&name_input='+name_input+''+'&sort_by='+sort_by+
                '&order_sort_by='+order_sort_by,
                type: 'GET',
                success: function(json)
                    {
                        listOrders(json);
                        records_amount=(json.records_amount);
                        records_per_page=(json.records_per_page);
                        pages_amount = Math.ceil(records_amount/records_per_page);
                        document.getElementById("page").innerHTML = page;
                        document.getElementById("pages_amount").innerHTML = pages_amount

 /*Pagination buttons events*/

                        if (page==1){
                            $('#prev').prop('disabled', true);
                            $('#first').prop('disabled', true);
                            $('#prev').addClass("button_disable");
                            $('#first').addClass("button_disable");
                        } else {
                            $('#prev').prop('disabled', false);
                            $('#first').prop('disabled', false);
                            $('#prev').removeClass("button_disable");
                            $('#first').removeClass("button_disable");
                            $('#prev').removeAttr("disabled");
                            $('#first').removeAttr("disabled");
                        }

                        if (page==pages_amount){
                            $('#next').prop('disabled', true);
                            $('#last').prop('disabled', true);
                            $('#next').addClass("button_disable");
                            $('#last').addClass("button_disable");
                        } else {
                            $('#next').prop('disabled', false);
                            $('#last').prop('disabled', false);
                            $('#next').removeClass("button_disable");
                            $('#last').removeClass("button_disable");
                            $('#next').removeAttr("disabled");
                            $('#last').removeAttr("disabled");
                        }
                    }
                })
            }

            if (page==1){
                createTableOrders();
            }

            $('#next').click(function(){
            if (page*records_per_page>=records_amount){page=page}
            else {page=page+1}
            createTableOrders()
            });

            $('#prev').click(function(){
            page=page-1;
            if (page<=1){
            page=1;
            }
            createTableOrders()
            });

            $('#first').click(function(){
            page=1;
            createTableOrders()
            });

            $('#last').click(function(){
            page=pages_amount;
            createTableOrders()
            });

 /* Change table size select event*/

                $('#table_size').change(function () {
                $(".index").removeClass("asc");
                $(".index").removeClass("desc");
                count_tr=$('#table_size').val();
                $( "#table_siz option:selected" ).each(createTableOrders())
  });

 /*--------------------------*/

 /*Sorting in columns */

           $(".index").click(function(){
                $(".index").removeClass("asc");
                $(".index").removeClass("desc");
                var entry = this.innerHTML;
                entry = entry.replace(/\s/g, '');
                switch (entry){
                    case "OrderID":
                        sort_by="order_id";
                        break;
                    case "OrderNumber":
                        sort_by="order_number";
                        break;
                    case "Customer":
                        sort_by="user";
                        break;
                    case "Status":
                        sort_by="orderStatus";
                        break;
                    case "Amount":
                        sort_by="total_price";
                        break;
                    case "Assignee":
                        sort_by="role";
                        break;

                }
                if (detector===entry){
                    counter +=1;
                }
                else{
                    detector=entry;
                    counter= 0;
                }
                if (counter%2==0){
                    order_sort_by = "asc";
                    $(this).addClass("asc")
                }
                else{
                    order_sort_by = "desc";
                    $(this).addClass("desc")
                }
                    createTableOrders();

           });
  });
