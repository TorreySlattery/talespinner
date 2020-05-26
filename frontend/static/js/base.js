$(document).ready(function(){
    $("img.roll-image").on('click', function(){
        console.log("todo: add ajax call to roll endpoint")
        var response = ["19+3=22", "7+3=10"]
        var data_stat = $(this).attr('data-target')
        var el = $("td[data-stat='" + data_stat + "']");
        el.html(response[0] + "<br/>" + response[1])
    });
})