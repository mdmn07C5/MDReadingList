function getReadingList() {
    $.ajax({
        type: "GET",
        // url: "{% url 'main:return_reading_list_json' %}",
        url: "/return_reading_list_json",
        success: function(data) {
            $("#list_container").html(data.content);
        },
        complete: function() {
            alert("IT'S READY YA GIT");
            $("#download_button").removeClass("disabled");
            $("#download_button").addClass("pulse");
        }
    }).then(function() {
        // alert("Done!");
        // do some shit with button/csv download here
    }); 
}

function disablePulse() {
    $("#download_button").removeClass("pulse");       
}