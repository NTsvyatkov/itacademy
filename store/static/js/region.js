/**
 * Created by toha on 25.12.13.
 */

   var count_tr=10;
   var tr = [];


  $(document).ready(function() {
   var table_grid = document.getElementById('grid');
   function creat_grid(count){
       for (var i=1; i<=count;i++ ){
         tr[i] = document.createElement('TR');
         table_grid.appendChild(tr[i]);
         tr[i].id=i;
         if (i % 2 == 0) tr[i].style.background = "#E8E8E8";
             for (var j=0; j<=3; j++){
                 tr[i].appendChild(document.createElement('TD'));}
       }

     }
    creat_grid(count_tr);

  function clearing_tr(i){
      for (var j=0; j<=3; j++){
          tr[i].cells[j].innerHTML='';}
  }

  function clearing_grid(){
      for (var n=2 ; n<=count_tr; n++){
          clearing_tr(n);}
  }

  function deleting_grid(){
    for (var n=table_grid.rows.length ; n>=2; n--){
       table_grid.removeChild(table_grid.childNodes[n]);}
  }
  create_entity();

  function create_entity(){
      $.ajax({
      dataType: "json",
      url: '/api/regions',
      type: 'GET',
      contentType: "application/json",
      success: function(json)
        {
            ajax_success(json);
        }
              })
  }

  function delete_id(id)
  {
  if (id=='') id=0;
   $.ajax({
   dataType: "json",
   url: '/api/regions/'+id,
   type: 'DELETE',
   contentType: "application/json",
   success: function(json)
                {
                if (json.message == 'success'){
                    alert('The region has been successfully deleted');
                    create_entity();
                    }
                else
                     alert (json.message);
                    },

                    error: function(e){
                       error = JSON.parse(e.responseText);
                       alert(error.message);
                    }
    })
    }

  var k=0
  function ajax_success(json){
      deleting_grid()
      creat_grid(json.regions.length)
      document.getElementById('add_button').style.display='inline'
      document.getElementById('edit_button').style.display='none'
      for (var region_k in json.regions){
          k++;
          tr[k].cells[0].innerHTML = json.regions[region_k].region_id;
          tr[k].cells[1].innerHTML = json.regions[region_k].name;
          tr[k].cells[2].innerHTML = "<input type='button' value='Edit' id='edit_region'  alt=" + k + ">";
          tr[k].cells[3].innerHTML = "<input type='button' value='Delete' id='delete_region'  alt=" + k + ">";
          tr[k].cells[2].abbr=k;
          tr[k].cells[3].abbr=k;
          tr[k].cells[2].onclick = function edit_region(){
          var str = tr[this.abbr].cells[1].innerHTML
          var id_tr = tr[this.abbr].cells[0].innerHTML
          document.getElementById('region_name').value=str
          region=id_tr
          document.getElementById('add_button').style.display='none'
          document.getElementById('edit_button').style.display='inline'
          }
          tr[k].cells[3].onclick= function delete_region(){
          var str = tr[this.abbr].cells[1].innerHTML
          var id_tr = tr[this.abbr].cells[0].innerHTML
          if (confirm('Are you sure you want to delete region '+ str +' '+id_tr+'?')){
              delete_id(id_tr)}
          }
      }
  k=0;
  }

  $('#add_button').click(function(){
  add();
    });
  $('#edit_button').click(function(){
  update();
    });
  $('#cancel').click(function(){
  cancel();
    });

 function add() {
   form_value = {name : $( name = $('#region_name').val())}

   $.ajax({
   data : JSON.stringify({'name' : name}) ,
   dataType: "json",
   url: '/api/regions',
   type: 'POST',
   contentType: "application/json",
   success:function(json) {
                    }})
   create_entity();
   document.getElementById('info').reset();
  }

 function update() {
     form_value = {name : $( name = $('#region_name').val())}
     region_id=~~region
     $.ajax({
     dataType: "json",
     url: '/api/regions',
     type: 'PUT',
     data : JSON.stringify({'region_id': region_id, 'name':name}),
     contentType: "application/json",
     success:function(json){ }
         });
     create_entity();
     document.getElementById('info').reset();
 }
 function cancel(){
    document.getElementById('add_button').style.display='inline'
    document.getElementById('edit_button').style.display='none'
  }
  })