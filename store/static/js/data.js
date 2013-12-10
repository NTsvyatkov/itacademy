
function data(){
     // global variable
   var data_role;
   // Variable from url
   var get = location.search;
        if(get != '')
        {
	       var id = (get.substr(1));
            id.split();

        }
$.ajax(
    {
        dataType: "json",
        url: '/api/users/'+id,
        type: 'GET',
        contentType: "application/json",
        success: function(data)
                    {

                       $('#login').val(data.users.login);
                       $('#first_name').val(data.users.first_name);
                       $('#last_name').val(data.users.last_name);
                       $('#email').val(data.users.email);
                       $('#region').val(data.users.region_id);
                       data_role = data.users.role_id;
                    }

    });
    return false;
}