$(document).ready(function() {
    $.ajax({
        url: "http://meerkat.eng.vmware.com:80/availability/fitness"
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
        url: "http://meerkat.eng.vmware.com:80/availability/tennis"
    }).then(function(data) {
		var className = 'unknown';
		
    	if(data == 'true'){
			className = "available";
		} else if (data === 'false'){
			className = "unavailable";
		}
		
		$("#tennis-img").attr('class', className);;
    });

	$.extend(Chart.defaults.global, {
		defaultFontColor : "white",
		responsive: true,
		legend: {
			display: false
		}
	});

	$.ajax({
		url: "js/chart/data/fitness-availability-daily.json"
	}).then(function (chartConfig) {
		var element = document.getElementById("fitness-availability-daily").getContext("2d");
		new Chart(element, chartConfig);
	});

	$.ajax({
		url: "js/chart/data/tennis-availability-daily.json"
	}).then(function (chartConfig1) {
		var element = document.getElementById("tennis-availability-daily").getContext("2d");
		new Chart(element, chartConfig1);
	});

	$.ajax({
		url: "js/chart/data/fitness-availability-weekly.json"
	}).then(function (chartConfig) {
		var element = document.getElementById("fitness-availability-weekly").getContext("2d");
		window.myLine = new Chart(element, chartConfig);
	});

	$.ajax({
		url: "js/chart/data/tennis-availability-weekly.json"
	}).then(function (chartConfig) {
		var element = document.getElementById("tennis-availability-weekly").getContext("2d");
		window.myLine = new Chart(element, chartConfig);
	});
});