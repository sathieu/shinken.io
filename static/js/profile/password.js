
$(function(){

    function add_error(txt){
        $('#password_err').html("There was a problem! The server said: " + txt);
	$('#password_err').show();
    }

    function manage_return(data){
	var status = data.status;
	var txt    = data.text;
	if(status == 200){
	    console.log(data);
	    // Be sure to hide the errors if need
	    $('#password_err').hide()
	    // OK go to the profile page now
	    window.location = '/~';
	    return;
	}
	if(status >= 400){
	    add_error(txt);
            return;
        }
	
	// How are you here?
	$('#password_err').html("There was a problem! The server said:" + status + "," + txt);
    }


    $('#password').on('submit', function() {
        // appel Ajax
	console.log($(this).serialize());
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(), 
            success: function(data) { // je récupère la réponse du fichier PHP
		manage_return(data);
            },
	    error: function(jqXHR, textStatus, errorThrown) {
		// Ops, something when wrong....
		add_error(errorThrown);
	    }
        });
	// block the browser to submit itself
	return false; 
    });
});