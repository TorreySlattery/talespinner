$(document).ready(function(){
    $("img.roll-image").on('click', function(){
        var data_stat = $(this).attr('data-target');
        var $parentTable = $(this).closest('table.table')
        var data_creature_id = $parentTable.attr('data-creature-id')
        $.ajax({
            type: "POST",
            url: "http://localhost:8000/api/roll/",
            headers: { "Authorization": "Token " + AUTH_TOKEN },
            data: { "creature_id": data_creature_id, "field_name": data_stat},
        }).done(function(data){
            var first_roll = data["result"][0];
            var second_roll = data["result"][1];
            var el = $parentTable.find("td[data-stat='" + data_stat + "']");
            el.html(`<div class="roll-result">${first_roll}</div><div class="roll-result">${second_roll}</div>`);
        }).fail(function(err){
            console.log(err);
        });

    });
})