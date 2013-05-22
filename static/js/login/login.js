
$(function(){

    function add_error(txt){
        $('#login_err').html("There was a problem! The server said: " + txt);
	$('#login_err').show();
    }

    function manage_return(data){
	var status = data.status;
	var txt    = data.text;
	if(status == 200){
	    // Be sure to hide the errors if need
	    $('#login_err').hide()
	    // OK go to the root page now
	    window.location = '/';
	    return;
	}
	if(status == 400){
	    add_error(txt);
            return;
        }
	
	// How are you here?
	$('#login_err').html("There was a problem! The server said:" + status + "," + txt);
    }


    $('#login').on('submit', function() {
        // appel Ajax
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