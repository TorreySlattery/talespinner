$(document).ready(function(){
    $("img.roll-image").on('click', function(){
        var $rollOutputField = $(this).closest('td').siblings("td[data-roll-field]")
        var $parentTable = $(this).closest('table.table')
        var creature_id = $parentTable.attr('data-creature-id')
        var field_name = $rollOutputField.attr("data-roll-field")
        $.ajax({
            type: "POST",
            url: "http://localhost:8000/api/roll/",
            headers: { "Authorization": "Token " + AUTH_TOKEN },
            data: { "creature_id": creature_id, "field_name": field_name},
        }).done(function(data){
            var first_roll = data["result"][0];
            var second_roll = data["result"][1];
            $rollOutputField.html(`<div class="roll-result">${first_roll}</div><div class="roll-result">${second_roll}</div>`);
        }).fail(function(err){
            console.log(err);
        });

    });
})