
$(document).ready(function() {


    var count_tr=$('#table_size').val();
    var th = ['id','Product name','Description','Price','Edit','Delete'];
    var count_td= th.length-1;
    var page = 1;
    var table_grid = document.getElementById('grid');
    var filter_query='';

    /* Creating table of products (size = count_tr Х count_td)  */
    var tr1 = document.createElement('TR');
    table_grid.appendChild(tr1);
    for (var j=0; j<=count_td; j++)
    {
        tr1.appendChild(document.createElement('TH'));
        tr1.cells[j].innerHTML=th[j];
    }


    /*----------------End of creating table-------------------------------*/
    create_grid(count_tr,count_td,'grid');



    function grid_pagination()
    {
        $.ajax({
            dataType: "json",
            url: '/api/products/?page='+page+'&table_size='+count_tr+ filter_query,
            type: 'GET',
            success: function(json)
            {
                ajax_success(json);
                include_pagination(page,json);
            }
        })
    }
    function delete_id(id,grid_length)
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
                    if (grid_length==1)
                    {
                        if (page!=1)
                        {page=page-1;}
                    }
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
        deleting_grid('grid');
        var grid_length = json.products.length;
        create_grid(grid_length,count_td,'grid');
        /*-------------Create table with new products list-------------------- */
        var k=0;

        for (var product_k in json.products)
        {
            k++;

            tr=table_grid.rows[k];
            id_product=json.products[product_k].id;
            tr.cells[0].innerHTML = '<span class = product_id>'+id_product+'</span>';
            tr.cells[1].innerHTML = '<span class=name>'+json.products[product_k].name+'</span>';
            tr.cells[2].innerHTML = json.products[product_k].description;
            tr.cells[3].innerHTML = '$'+json.products[product_k].price;
            tr.cells[4].innerHTML = "<img src='static/images/Text Edit.png' class='edit_img' alt=" + id_product + ">";
            tr.cells[5].innerHTML = "<img src='static/images/delete.png' class='delete_img'  alt=" + id_product + ">";
            tr.cells[4].abbr=k;
            tr.cells[5].abbr=k;

        }

        $('.delete_img').click(function(){
            var tr= $(this).closest('tr');
            var product_id = this.alt;
            var product_name=tr.children('td').children('.name').text();
            if(confirm('Are you sure you want to delete product '+ product_name +' ?'))
            {
                delete_id(product_id,grid_length);
            }
        })

        $('.edit_img').click(function(){
                var tr= $(this).closest('tr');
                var product_id = tr.children('td').children('.product_id').text();
                var product_name=tr.children('td').children('.name').text();
                if(confirm('Edit '+ product_name +' ?')){
                    document.location.href = 'product/'+product_id+'';
                }
            }
        );

        /*---------------------End creating table------------------------------------*/

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
    /*--------------------------*/

    /*Change table size select event*/
    $('#table_size').change(function () {
        page=1;
        count_tr=$('#table_size').val();
        $( "#table_siz option:selected" ).each(grid_pagination())
    })
    /*----------------------------------------*/

    /*------- Update and clear table's buttons----------------------------*/

    $('#apply_button').click(function()
    {
        var check= true;
        var error='';
        var name_options;
        var d_op;
        var price_options;
        /*------------------------Checking filter options-------------------------------*/
        if ((!( $('#name_options').val() != 0 && $('#name_input').val() )) &&
            (!( $('#name_options').val() == 0 && !($('#name_input').val()) )))
        {
            check = false;
            error = 'If you set value for Name select, you should set value for Name input. And conversely!<br>';
        }

        if ((!( $('#description_options').val() != 0 && $('#description_input').val() )) &&
            (!( $('#description_options').val() == 0 && !($('#description_input').val()) )))
        {
            check = false;
            error = error + 'If you set value for Description select, you should set value \
                                                                       for Description input. And conversely!<br>';
        }

        if  ((!( $('#price_options').val() != 0 && $('#price_input').val() ))
            && (!( $('#price_options').val() == 0 && !($('#price_input').val()) )))
        {
            check = false;
            error = error +  'If you set value for Price select, you should set value for Price input. \
                                                                                           And conversely!<br>';
        }
        var val = $('#price_input').val();


        if(!(val/val)&&(val!=0))  /*Check on numeric */
        {
            check = false;
            error = error + 'Price is not numeric'
        }
        /*--------------------------------------------------------------------------------------------------*/
        if (check)
        {
            name_options = '&name_options='+ $('#name_options').val()+'&name='+ $('#name_input').val();
            d_op = '&description_options='+$('#description_options').val()+'&description='+$('#description_input').val();
            price_options = '&price_options='+$('#price_options').val()+'&price='+$('#price_input').val();
            filter_query = name_options +d_op+price_options;
            page=1;
            grid_pagination();
            $('.error_div').empty();
        }
        else
        {
            $('.error_div').empty();
            $('.error_div').html(error);
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
        $('.error_div').empty();
        error ='';

    });
    /*----------------------------End  Update and clear table's button------------------------*/

});

