 function create_grid(count_tr, count_td)
 {
     var table_grid = document.getElementById('grid');
     for (var i=1; i<=count_tr;i++ )
        {
            tr1 = document.createElement('TR');
            table_grid.appendChild(tr1);
            if (i % 2 == 0) tr1.style.background = "#c0c0c0"; /* .className = 'tr_style' */
            for (var j=0; j<=count_td; j++)
             {
              tr1.appendChild(document.createElement('TD'));
             }
        }
 }

 function deleting_grid()
 {
    var table_grid = document.getElementById('grid');
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
   document.getElementById("page").innerHTML = page;
   document.getElementById("pages_amount").innerHTML = pages_amount;

   if (page==1)
   {
      $('#prev').prop('disabled', true);
      $('#first').prop('disabled', true);
   }
   else
   {
       $('#prev').prop('disabled', false);
       $('#first').prop('disabled', false);
   }

   if (page==pages_amount)
   {
     $('#next').prop('disabled', true);
     $('#last').prop('disabled', true);
   }
   else
   {
    $('#next').prop('disabled', false);
    $('#last').prop('disabled', false);
    }



 }