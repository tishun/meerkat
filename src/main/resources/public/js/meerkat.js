$(document).ready(function() {
    $.ajax({
        url: "http://10.23.8.174:8080/availability/fitness"
    }).then(function(data) {
		var className = 'unknown';
		
    	if(data == 'true'){
			className = "available";
		} else if (data === 'false'){
			className = "unavailable";
		}
		
		$("#fitness-img").attr('class', className);;
    });
	
	$.ajax({
        url: "http://10.23.8.174:8080/availability/tennis"
    }).then(function(data) {
		var className = 'unknown';
		
    	if(data == 'true'){
			className = "available";
		} else if (data === 'false'){
			className = "unavailable";
		}
		
		$("#tennis-img").attr('class', className);;
    });
	
});