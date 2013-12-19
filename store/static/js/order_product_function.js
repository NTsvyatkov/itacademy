 function create_grid(count_tr, count_td,table_id)
 {
     var table_grid = document.getElementById(table_id);
     for (var i=1; i<=count_tr;i++ )
        {
            tr1 = document.createElement('TR');
            table_grid.appendChild(tr1);
            if (i % 2 == 0) tr1.style.background = "#efddba"; /* .className = 'tr_style' */
            for (var j=0; j<=count_td; j++)
             {
              tr1.appendChild(document.createElement('TD'));
             }
        }
 }

 function deleting_grid(table_id)
 {
    var table_grid = document.getElementById(table_id);
    for (var n=table_grid.rows.length ; n>=2; n--)
      {
       table_grid.removeChild(table_grid.childNodes[n]);
      }

 }

 function include_pagination(page,json)
 {
   records_amount=(json.records_amount);
   records_per_page=(json.records_per_page);
   pages_amount = Math.ceil(records_amount/records_per_page);
   if (pages_amount <1){
       pages_amount = 1
   }
   document.getElementById("page").innerHTML = page;
   document.getElementById("pages_amount").innerHTML = pages_amount;

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