
$(document).ready(function() {
    var tr = [];
    var count_tr=$('#table_size').val();
    var th = ['id','Product name','Description','Price','Dimension','Edit','Delete'];
    var count_td= th.length-1;
    var page = 1;
    var table_grid = document.getElementById('grid');
    var filter_query='';


  /* Creating table of products (size = count_tr Х count_td)  */

    tr[0] = document.createElement('TR');
    table_grid.appendChild(tr[0]);
    for (var j=0; j<=count_td; j++)
    {
          tr[0].appendChild(document.createElement('TH'));
          tr[0].cells[j].innerHTML=th[j];
    }

  function create_grid(count_tr, count_td)
    {
        for (var i=1; i<=count_tr;i++ )
        {
            tr[i] = document.createElement('TR');
            table_grid.appendChild(tr[i]);
            tr[i].id=i;
            if (i % 2 == 0) tr[i].style.background = "#c0c0c0"; /* .className = 'tr_style' */
            for (var j=0; j<=count_td; j++)
             {
              tr[i].appendChild(document.createElement('TD'));
             }
        }
      $( "tr:even" ).css( "background-color", "#c0c0c0" );
    }

   create_grid(count_tr,count_td);
  /*End of creating table*/


  function clearing_tr(i)
  {
      for (var j=0; j<=6; j++)
      {
          tr[i].cells[j].innerHTML='';
      }
  }

 function clearing_grid()
  {
    for (var n=2 ; n<=count_tr; n++)
    {
      clearing_tr(n);
    }
  }

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
        url: '/api/products/?page='+page+'&table_size='+count_tr+ filter_query,
        type: 'GET',
        success: function(json)
        {
           ajax_success(json);

           records_amount=(json.records_amount);
           records_per_page=(json.records_per_page);
           pages_amount = Math.ceil(records_amount/records_per_page);
           document.getElementById("page").innerHTML = page;
           document.getElementById("pages_amount").innerHTML = pages_amount

           if (page==1){
               $('#prev').css({ "opacity":"0.4"});
               $('#first').css({ "opacity":"0.4"});
           } else {$('#prev').css({ "opacity": "1"});
               $('#first').css({ "opacity": "1"});
           }

           if (page==pages_amount){
               $('#next').css({ "opacity": "0.4"});
               $('#last').css({ "opacity": "0.4"});
           } else {$('#next').css({ "opacity": "1"});
               $('#last').css({ "opacity": "1"});
           }
         }
      })
     }

 function delete_id(id)
  {
   $.ajax({
       dataType: "json",
        url: '/api/product/'+id,
        type: 'DELETE',
        success: function(json)
                    {
                        if (json.message == 'success')
                         {
                          alert('The product has been successfully deleted');
                          grid_pagination();
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

 function ajax_success(json)
  {
           deleting_grid();
           create_grid(json.products.length,count_td);
           /*Create table with new products list */
           var k=0;
            for (var product_k in json.products)
                {
                 k++;

                 tr[k].cells[0].innerHTML = json.products[product_k].id;
                 tr[k].cells[1].innerHTML = json.products[product_k].name;
                 tr[k].cells[2].innerHTML = json.products[product_k].description;
                 tr[k].cells[3].innerHTML = json.products[product_k].price.toFixed(2);
                 tr[k].cells[4].innerHTML = json.products[product_k].dimension;
                 tr[k].cells[5].innerHTML = "<img src='static/images/Text Edit.png' class='edit_img' alt=" + k + ">";
                 tr[k].cells[6].innerHTML = "<img src='static/images/delete.png' class='delete_img'  alt=" + k + ">";
                 tr[k].cells[5].abbr=k;
                 tr[k].cells[6].abbr=k;
                 tr[k].cells[5].onclick = function edit_tr2()
                                      {
                                       alert ('Edit '+tr[this.abbr].cells[1].innerHTML+'');
                                      }
                 tr[k].cells[6].onclick= function delete_tr2()
                                      {
                                        var str = tr[this.abbr].cells[1].innerHTML
                                        var id_tr = tr[this.abbr].cells[0].innerHTML
                                        if (confirm('Are you sure you want to delete product '+ str +' '+id_tr+'?'))
                                        {
                                          delete_id(id_tr)
                                        }
                                       }
                }

            /*End creating table*/

  }


  if (page==1)
  {
  grid_pagination();
  }

  /*Pagination buttons events*/

   $('#next').click(function(){
    if (page*records_per_page>=records_amount){page=page}
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

    $('#table_size').change(function () {
     page=1;
     count_tr=$('#table_size').val();
     $( "#table_siz option:selected" ).each(grid_pagination())
     })

  /* Update and delete table button*/

    var check= true;
    var error='';
    $('#apply_button').click(function(){
      if ((!( $('#name_options').val() != 0 && $('#name_input').val() )) && (!( $('#name_options').val() == 0 && !($('#name_input').val()) )))
         {
          check = false;
          error = 'If you set value for Name select, you should set value for Name input. And conversely!<br>';
         }

      if ((!( $('#description_options').val() != 0 && $('#description_input').val() )) && (!( $('#description_options').val() == 0 && !($('#description_input').val()) )))
         {
          check = false;
          error = error + 'If you set value for Description select, you should set value for Description input. And conversely!<br>';
         }

      if  ((!( $('#price_options').val() != 0 && $('#price_input').val() )) && (!( $('#price_options').val() == 0 && !($('#price_input').val()) )))
         {
          check = false;
          error = error +  'If you set value for Price select, you should set value for Price input. And conversely!<br>';
         }
      var val = $('#price_input').val();
      if(!(val/val)&&(val!=0))
      {
       check = false;
        error = error + 'Price is not number'
      }

      if (check)
       {
        var name_options = '&name_options='+ $('#name_options').val()+'&name='+ $('#name_input').val();
        var d_op = '&description_options='+$('#description_options').val()+'&description='+$('#description_input').val();
        var price_options = '&price_options='+$('#price_options').val()+'&price='+$('#price_input').val();
        filter_query = name_options +d_op+price_options;
        grid_pagination();
        $('#error_div').empty();
       }
      else
      {
        $('#error_div').empty();
        $('#error_div').html(error);
        error ='';
      }
     });

    $('#clr').click(function(){
      $('#name_options').val(0);
      $('#name_input').val('');
      $('#description_options').val(0);
      $('#description_input').val('');
      $('#price_options').val(0);
      $('#price_input').val('');
      $('#error_div').empty()
    });


});

