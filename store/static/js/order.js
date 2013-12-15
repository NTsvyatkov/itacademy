/* JQueri UI  - Datapicker options*/
$(function () {
    var dateReg = /^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$/;
    $("#expire_date").click(function () {
        $('.ui-datepicker-calendar').hide()
    });
    $("#expire_date").datepicker({
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,
        dateFormat: 'yy/mm',
        onClose: function (dateText, inst) {
            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
            $(this).datepicker('setDate', new Date(year, month, 1));
        }
    });
    $("#expire_date").focus(function () {
        $(".ui-datepicker-calendar").hide();
        $("#ui-datepicker-div").position({
            my: "center top",
            at: "center bottom",
            of: $(this)
        });
    });
    $("#start_date").click(function () {
        $('.ui-datepicker-calendar').hide()
    });
    $("#start_date").datepicker({
        changeMonth: true,
        changeYear: true,
        disabled: true,
        showButtonPanel: true,
        dateFormat: 'yy/mm',
        onClose: function (dateText, inst) {
            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
            $(this).datepicker('setDate', new Date(year, month, 1));
        }
    });
    $("#start_date").focus(function () {
        $(".ui-datepicker-calendar").hide();
        $("#ui-datepicker-div").position({
            my: "center top",
            at: "center bottom",
            of: $(this)
        });
    });
    $("#preferable_date").datepicker(
        {
            dateFormat: 'dd/mm/yy',
            onClose: function () {
                if (!dateReg.test($(this).val())) {
                    $(this).datepicker('setDate', new Date());
                }
                var dateTypeVar = $(this).datepicker('getDate');
                var tt = $.datepicker.formatDate('yy-mm-dd', dateTypeVar);
                $('#hidden_preferable_date').val(tt)
            }
        }
    );
});
/*--------------------------*/

var json;
$(document).ready(function () {
    var order_id = get_order_id;
    var maestro_card = false;
    var th = ['Item Number', 'Item Name', 'Item Description', 'Dimension', 'Price', 'Quantity',
               'Price per Line', 'Edit', 'Delete'];
    var count_td = th.length - 1;
    var count_tr = $('#table_size').val();
    var tr = [];
    var page = 1;
    var error_list = [];
    var table_grid = document.getElementById('grid');
    var total_price;
    var order_date;
    var save_button = 0;
    var uniq_order = false;

    var deleted_order_product = [];
     /*-----Default values---------------*/
    $('#issue_number').attr('readonly', true);
    $('#issue_number').css('background-color', '#e2e2e2');
    $('#start_date').css('background-color', '#e2e2e2');
    $('#start_date').val('');
    $('#add_order').prop('disabled', true);
    $('#add_order').addClass("button_disable");
    $('#credit_card_options').val(1);
    /*----------------------------------*/

    /* Creating table of products (size = count_tr Х count_td)  */
    var tr1 = document.createElement('TR');
    table_grid.appendChild(tr1);
    for (var j = 0; j <= count_td; j++) {
        tr1.appendChild(document.createElement('TH'));
        tr1.cells[j].innerHTML = th[j];
    }
    create_grid(count_tr, count_td);
    if (get_order_id){
        ajax_pull('GET', 'data','');
        pagination_slice(page, count_tr);
    }

    /*----------------End of creating table-------------------------------*/

    /* Ajax function for put,get,post methods*/
    function ajax_pull(type_options, data ,button) {
        $.ajax({
            dataType: "json",
            url: '/api/order_product/?order_id='+get_order_id +'+&page=' + page + '&table_size=' + count_tr,
            type: type_options,
            contentType: "application/json",
            data: data,
            async: false,
            success: function (json_val) {
                if (type_options == 'GET') {
                    json = json_val;
                    $('#order_status').val(json.order_status);
                    pagination_slice(page, count_tr);
                }
                if (type_options == 'PUT'){
                    if (button=='Order'){
                      alert('Order successfully issued');
                      /*window.location.replace("/orders");*/
                    }
                    if (button=='Save'){
                      alert('Order saved and update');
                    }
                }
            },
            error: function (e) {
                error = JSON.parse(e.responseText);
                alert(error.message);
            }
        })
    }

    /*------------------------------------------*/


    /* ----------Function for copy object-----------------*/
    function clone(obj) {
        if (obj == null || typeof(obj) != 'object') {
            return obj;
        }
        var temp = {};
        for (var key in obj) {
            temp[key] = clone(obj[key]);
        }
        return temp;
    }


    function get_total_amount() {
        var total_sum = 0;
        var total_items = 0;
        var result = [];
        for (var i in json.order) {
            total_sum = total_sum + +json.order[i].price * +json.order[i].dimension_number * +json.order[i].quantity;
            total_items = total_items + +json.order[i].dimension_number * +json.order[i].quantity;
        }
        result.push(total_sum);
        result.push(total_items);
        return result;
    }

  var fill_field={"description": "bad apple", "dimension": "Items",
                  "dimension_id": 1, "dimension_number": 1,
                  "name": "pineapple", "price": "2.50", "product_id": 3,
                  "quantity": 4};

    $('#add_item').click(function(){
    /*--------------Modal window event-----------------------*/
       $('#exampleModal').arcticmodal();
    /*-------------------------------------------------------*/
       if (json){
           json.order.push(fill_field)
       }else{
           var order=[]
           order.push(fill_field);
           json={order:order}
       }
       pagination_slice(page,count_tr);
    })
    $('#close_modal').click( function(){
        $.arcticmodal('close');
       }
    )


    function pagination_slice(page, count_tr) {
        var total_items;
        var get_total = [];
        get_total = get_total_amount();
        total_price = get_total[0];
        total_items = get_total[1];
        $('#total_items').val(total_items);
        $('#total_amount').val(total_price.toFixed(2) + '$');
        var stop = page * count_tr
        var start = stop - count_tr
        var order_slice = json.order.slice(start, stop);
        var json_slice = clone(json);
        delete json_slice['order'];
        json_slice['order'] = order_slice;
        fill_grid(json_slice);
        records_per_page = count_tr;
        records_amount = json.order.length;
        pages_amount = Math.ceil(records_amount / records_per_page);
        document.getElementById("page").innerHTML = page;
        document.getElementById("pages_amount").innerHTML = pages_amount;

        if (page == 1) {
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

        if (page == pages_amount) {
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



    /*-------------Update quantity in row------------------*/
    function update_quantity(product_id, dimension_id, object_quantity, old_quantity, price, quantity, tr, dim) {

        for (var i in json.order) {
            if ((json.order[i].product_id == product_id) && (json.order[i].dimension_id == dimension_id ) &&
                (json.order_id == order_id)) {
                json.order[i].quantity = quantity;
            }
        }
        var sum = +price * +quantity * dim;
        tr.children('td').children('.amount').text(sum.toFixed(2));
        tr.children('td').children('.old_quantity').val(quantity);
        total_amount = total_price - (+old_quantity * +price * dim) + (+quantity * +price * dim);
        total_price = total_amount;
        $('#total_amount').val(total_amount.toFixed(2) + '$');
        pagination_slice(page, count_tr);

    }

    /*--------------------------------------------------*/

    /*------------ Check Unique Order Number in DB ------------------*/
    function unique_order_number(json_data) {
        $.ajax({
            dataType: "json",
            url: '/api/unique_order_number/',
            type: 'PUT',
            contentType: "application/json",
            data: json_data,
            success: function (json) {
                var unique_number_error = [];
                if (json.message == 'not unique') {
                    var error = 'Order Number is not unique. Rename it. ';
                    unique_number_error.push({id: $('#order_error'), error: error});
                    $('#order_number').val('');
                }
                else {
                    $('#order_number').val(json.unique_order_number);
                    order_id=json.order_id
                    $('#order_number').attr('readonly', true);
                    $('#order_number').css('background-color', '#e2e2e2');
                    $('#order_number').css('background-color', '#e2e2e2');
                    uniq_order = true;
                    ajax_pull('POST',creat_json(),'Save')
                    $('#order_status').val('Created');
                }
                validation(unique_number_error);
            }
        })
    }

    /*--------------------------------------------------*/


    function delete_id(product_id, dimension_id, grid_length) {
        var status = false;
        /* Searching order_product dictionary for keys product_id , dimension_id*/
        for (var i in json.order) {
            if ((json.order[i].product_id == product_id) && (json.order[i].dimension_id == dimension_id ) &&
                (json.order_id == order_id)) {
                deleted_order_product.push(json.order[i]);
                json.order.splice(i, 1);
                alert('The product has been successfully deleted from the cart');
                status = true;
            }
        }
        if (status) {
            if (grid_length == 1) {
                if (page != 1) {
                    page = page - 1;
                }
            }
            pagination_slice(page, count_tr);
        }
    }

    function date_format(unix_time) {
        var dt = new Date(unix_time);
        var date_format = dt.getDate() + '/' + (dt.getMonth() + 1) + '/' + dt.getFullYear();
        return date_format;
    }

    /*Function fill_grid  - put values in table  */
    function fill_grid(json) {
        var grid_length = json.order.length;
        var k = 0;
        var amount = 0;
        var input;
        var tr;
        if (json.delivery_date) {
            var delivery_date = json.delivery_date * 1000;
            $('#delivery_date').val(date_format(delivery_date));
        }
        else {
            $('#delivery_date').val('/ /');
        }
        if (json.order_date) {
            var order_date = json.order_date* 1000;
            $('#order_date').val(date_format(order_date));
        }
        else {
            $('#order_date').val('/ /');
        }

        deleting_grid();
        create_grid(grid_length, count_td);
        /*Create table with new order_products list */
        for (var product_k in json.order) {
            k++;
            tr = table_grid.rows[k];
            order_id = json.order_id;
            product_name = json.order[product_k].name;
            id_product = json.order[product_k].product_id;
            product_price = +json.order[product_k].price;
            tr.cells[0].innerHTML = id_product;
            tr.cells[1].innerHTML = product_name;
            tr.cells[2].innerHTML = json.order[product_k].description;
            tr.cells[3].innerHTML = json.order[product_k].dimension +
                '<input class="dimension" value="' + json.order[product_k].dimension_id + '" type="hidden">' +
                '<input class="old_quantity" value="' + json.order[product_k].quantity + '" type="hidden">';
            tr.cells[4].innerHTML = "<span class='price'>" + product_price.toFixed(2) + "</span>";
            input = "<input type='text' class='quantity' value='" + json.order[product_k].quantity + "'\
                     alt='" + json.order[product_k].id + "' style='width:60px'>\
                     <img  alt='refresh' class='update_amount' src='/static/images/refresh_32.png'> \
                      <b class='error_div'></b>";
            tr.cells[5].innerHTML = input;
            if (json.order[product_k].quantity) quant = Math.round(json.order[product_k].quantity); else quant = 0;
            amount = (product_price * +quant * +json.order[product_k].dimension_number).toFixed(2);
            tr.cells[6].innerHTML = "<span class='amount'>" + amount + "</span>";
            tr.cells[7].innerHTML = "<img src='/static/images/Text Edit.png' class='edit_img'>";
            tr.cells[8].innerHTML = "<img src='/static/images/delete.png' class='delete_img'\
                 id='" + product_name + "' alt=" + id_product + " >";
        }

        /*--------------------------------End of filling table------------------------------------*/

        $('.delete_img').click(function () {
            var tr = $(this).closest('tr');
            var dimension_id = tr.children('td').children('.dimension').val();
            var product_id = this.alt;
            if (confirm('Are you sure that you want to remove ' + this.id + ' from the cart?')) {
                delete_id(product_id, dimension_id, grid_length);
            }
        })


        $('.update_amount').click(function () {
            var tr = $(this).closest('tr');
            var price = tr.children('td').children('.price').text();
            var dimension_id = tr.children('td').children('.dimension').val();
            var old_quantity = tr.children('td').children('.old_quantity').val();
            var product_id = tr.children('td').children('.delete_img').attr('alt');
            var sum = 0;
            var dim = 1;
            var quantity = Math.round($(this).prev().val());
            var object_quantity = $(this).prev();
            var object_amount = tr.children('td').children('.amount');
            if (!(quantity / quantity) || (quantity == 0)) {  /*Check on numeric */
                $(this).next('.error_div').empty();
                //$(this).next('.error_div').html('Quantity should be numeric and not 0');
                alert('Quantity should be numeric and not 0');
                $(this).prev().val(old_quantity);
            }
            else {
                $(this).next('.error_div').empty();

                if (dimension_id == 1) {
                    dim = 1;
                }
                if (dimension_id == 2) {
                    dim = 5;
                }
                if (dimension_id == 3) {
                    dim = 10;
                }
                update_quantity(product_id, dimension_id, object_quantity, old_quantity, price, quantity, tr, dim);
            }
        })

    }


    /*----------------------------END of fill_grid ------------------------------------*/

    /*---------------------------------Validation function-----------------------------------*/
    function validation(unique_number_error) {
        var error = '';
        var clear_list;
        var object1;
        var dt;
        var month;
        var year;
        var now_date;
        var preferable_date;
        var form_value;
        var quantity;
        var credit_number;
        var no_error = true;
        var order_number;

        /* Clear error and border-color*/
        if (error_list) {
            for (i in error_list) {
                object1 = error_list[i].id;
                object1.css('border-color', '#999');
                object1.next('.error_div').remove();
            }
            error_list = [];
        }
        if (unique_number_error.length != 0) {
            no_error = false;
            error_list = unique_number_error.concat()
        }
        /*---------------------------------*

         /* String length validation */
        for (var i = 0, total = 0, k = 0; i < $('.quantity').size(); i++) {
            quantity = $('.quantity:eq(' + i + ')').val();
            if ((!(quantity / quantity) || (quantity == 0)) && k != 1) {  /*Check on numeric */
                error = 'Quantity should be numeric and not 0';
                k = 1;
                no_error = false;
                error_list.push({id: $('#order_error'), error: error});
            }
        }

        order_number = $('#order_number').val();
        if (order_number.length > 6) {
            error = 'Order number should be <=6 characters';
            no_error = false;
            error_list.push({id: $('#order_error'), error: error});
        }

        /*-----------End of Strings length validation---------*/

        /*Credit card numbers validation*/
        r_e = /^[0-9]{16}$/;
        credit_number = $('#credit_card_number').val();

        if (r_e.test(credit_number)) {
        }
        else {
            no_error = false;
            error = 'The credit card number should be a 16-digit number.';
            error_list.push({id: $('#credit_card_number'), error: error});
        }

        r_e_ccv2 = /^[0-9]{3}$/;
        cvv2_number = $('#cvv2_number').val();

        if (r_e_ccv2.test(cvv2_number)) {
        }
        else {
            no_error = false;
            error = 'The CVV2 number should be a 3-digit number.';
            error_list.push({id: $('#cvv2_number'), error: error});
        }

        issue_number = $('#issue_number').val();
        if ((maestro_card == true) && (issue_number )) {
            r_e_issue_number = /^[0-9]{1}$/;
            if (r_e_issue_number.test(issue_number)) {
            }
            else {
                no_error = false;
                error = 'Issue number format is wrong. it should be one digit or none!';
                error_list.push({id: $('#issue_number'), error: error});
            }
        }

        /*----------Credit card date validation----------------------------*/
        date_expire = $('#expire_date').val().replace('/', '-') + '-01T00:00';
        if (!Date.parse(date_expire)) {
            no_error = false;
            error = 'Expire date have wrong format, please use calendar';
            error_list.push({id: $('#expire_date'), error: error});
        }
        dt = new Date();
        month = dt.getMonth() + 1;
        year = dt.getFullYear();
        now_date = year + '-' + month + '-01T00:00';
        if (Date.parse(date_expire) < Date.parse(now_date)) {
            no_error = false;
            error = 'Expire date less then today date!';
            error_list.push({id: $('#expire_date'), error: error});
        }

        if (maestro_card == true) {
            date_start = $('#start_date').val().replace('/', '-') + '-01T00:00';
            if (Date.parse(date_start) > Date.parse(date_expire)) {
                no_error = false;
                error = 'Start date of card can not be more then Expire date';
                error_list.push({id: $('#start_date'), error: error});
            }
            if (!Date.parse(date_start)) {
                no_error = false;
                error = 'Start date have wrong format, please use calendar';
                error_list.push({id: $('#start_date'), error: error});
            }

        }
        /*--------------------End of Credit card validation----------------------*/

        /*----------------Preferable Delivery Date validation------------------*/
        preferable_date = $('#hidden_preferable_date').val() + 'T00:00';
        if ($('#hidden_preferable_date').val()) {
            preferable_date = Date.parse(preferable_date);
            if (preferable_date < order_date) {
                no_error = false;
                error = 'Preferable Delivery Date should be goes before then Date of Ordering';
                error_list.push({id: $('#preferable_date'), error: error});
            }
        }
        /*--------------------end of Preferable Delivery Date validation-------*/

        /* ------------------------Table length validation. It should be not 0------*/
        if (json){
            if (json.order.length!=0){
            }
            else {
            no_error = false;
            error = 'For saving order ypu should add one or more product to grid.';
            error_list.push({id: $('#order_error'), error: error});
            }
        }
        else{
            no_error = false;
            error = 'For saving order you should add one or more product to grid.';
            error_list.push({id: $('#order_error'), error: error});
        }
        /*------------------------End of Table length validation---------------------*/

        if (no_error) {
            /*Clear error message*/
            $('.error_div').empty();
            /*-----------------*/
            $('#add_order').prop('disabled', false);
            $('#add_order').removeClass("button_disable");
            $('#add_order').removeAttr("disabled");
            return true;
        }
        else {
            $('.product_filter_in .error_div').empty();
            for (i in error_list) {
                object1 = error_list[i].id;
                object1.closest('div').append('<p class=error_div>' + error_list[i].error + '');
                object1.css('border-color', '#b81900');
                save_button == 0;
            }
            $('#add_order').prop('disabled', true);
            $('#add_order').addClass("button_disable");
            return false;
        }
    }

    /*-------------------------------End of Validation function ----------------------------------------*/

    function creat_json(){
        /*add all quantity and product_id in array */
        var product_arr = [];
        var preferable_date;
        var assignee;
        for (var i = 0; i < json.order.length; i++) {
            product_arr[i] = {'quantity': +json.order[i].quantity, 'product_id': +json.order[i].product_id,
                'dimension_id': +json.order[i].dimension_id,
                'dimension_number': +json.order[i].dimension_number}
        }
        /*------------------*/
        if ($('#assignee').val() == 0 ){
            assignee=1;
        }
        else {
            assignee=$('#assignee').val();
        }
        preferable_date = $('#hidden_preferable_date').val() + 'T00:00';
        preferable_date = Date.parse(preferable_date);
        form_value = { order_id: order_id, preferable_delivery_date: preferable_date,
            assignee: assignee,
            credit_card_options: $('#credit_card_options').val(),
            credit_card_number: $('#credit_card_number').val(),
            cvv2_number: $('#cvv2_number').val(), expire_date: $('#expire_date').val(),
            start_date: $('#start_date').val(), issue_number: $('#issue_number').val(),
            product_quantity: product_arr, deleted_order_product: deleted_order_product};
        /* Json for put on server*/
        json_value = JSON.stringify(form_value);
        /*-----------------------*/
        return json_value
    }


    /*----------------------------Event Click on buttons Cancel, Order, Save -------------------------*/
    $('#cancel_order').click(function () {
        if (confirm('Order was not saved. Do you want cancel order?')) {
                window.location.replace("/orders");
        }
    })

    $('#add_order').click(function () {
        var arr = [];
        if (validation(arr)) {
            var json_value = creat_json()
            ajax_pull('PUT', json_value,'Order');
        }
    })

    $('#save_order').click(function () {
        var order_number = $('#order_number').val();
        var arr_error = [];
        if (validation(arr_error)){
           if ((!uniq_order) && (order_number.length <= 6)) {
              json_value = JSON.stringify({'unique_order_number': order_number });
              unique_order_number(json_value);
           }
            else{
               ajax_pull('PUT',creat_json(),'Save');
           }
        }

    })
 /*----------------------------------------------------------------------------------------------------*/


    /* -----------Card select event change-------------------*/
    $('#credit_card_options').change(function () {
        if ($('#credit_card_options').val() != 4) {
            $('#issue_number').attr('readonly', true);
            $('#issue_number').css('background-color', '#e2e2e2');
            $('#start_date').attr('readonly', true);
            $('#start_date').css('background-color', '#e2e2e2');
            $('#start_date').val('');
            $('#start_date').datepicker("option", "disabled", true);
        }
        else {
            $('#issue_number').attr('readonly', false);
            $('#issue_number').css('background-color', 'white');
            $('#start_date').attr('readonly', false);
            $('#start_date').css('background-color', 'white');
            $('#start_date').datepicker("option", "disabled", false);
            $("#start_date").focus(function () {
                $(".ui-datepicker-calendar").hide();
                $("#ui-datepicker-div").position({
                    my: "center top",
                    at: "center bottom",
                    of: $(this)
                });
            });
            maestro_card = true;
        }
    })
    /*------------------------------------------------------------*/

    /*----------------Disable button Order on input, select changing---------------------*/
    $('input:text').keyup(function () {
        $('#add_order').prop('disabled', true);
        $('#add_order').addClass("button_disable");
    });
    $('select').change(function () {
        $('#add_order').prop('disabled', true);
        $('#add_order').addClass("button_disable");
    })
    $('.hasDatepicker').click(function () {
        $('#add_order').prop('disabled', true);
        $('#add_order').addClass("button_disable");
    })
    /*----------------------------------------------------------------------------------*/

    /* ---------------------Change table size <select> event----------------------------*/
    $('#table_size').change(function () {
        page = 1;
        count_tr = $('#table_size').val();
        $("#table_siz option:selected").each(pagination_slice(page, count_tr))
    })
    /*----------------------------------------------------------------------------------*/

    /* What is this CVV2 --- alert  */
    $('#cvv2_info').click(function () {

        alert('The CVV2 code stands for Card Verification Value 2. The CID code stands for Card Identification.' +
            'It is a security feature on credit cards used to improve the security of transactions. It consists of ' +
            'a 3 or 4 digit number printed, but not raised, on the back of the credit card.');
    })
    /*---------------------------*/

    /*--------------------------Pagination buttons events------------------------------*/
    $('#next').click(function () {
        if (page * records_per_page >= records_amount) {
            page = page
        }
        else {
            page = page + 1;
        }
        pagination_slice(page, count_tr);
    });
    $('#prev').click(function () {
        page = page - 1;
        if (page <= 1) {
            page = 1;
        }
        pagination_slice(page, count_tr);
    });
    $('#first').click(function () {
        page = 1;
        pagination_slice(page, count_tr);
    });
    $('#last').click(function () {
        page = pages_amount;
        pagination_slice(page, count_tr);
    });
    /*---------------------------------------------------------------------------------*/

})
