$(document).ready(function(){
    $("img.roll-image").on('click', function(){
        var $td = $(this).closest('td');
        var field_name = $td.attr("data-roll-field");
        var roll_type = $td.attr("data-roll-type");
        var creature_id = $(this).closest('table.table').attr("data-creature-id");
        $.ajax({
            type: "POST",
            url: "http://localhost:8000/api/roll/",
            headers: { "Authorization": "Token " + AUTH_TOKEN },
            data: {
                "creature_id": creature_id,
                "field_name": field_name,
                "roll_type": roll_type,
                "roll_scope": "individual"
            },
        }).done(function(data){
            var first_roll = data["results"][creature_id][field_name][0];  // These might be string or int indices, keep in mind
            var second_roll = data["results"][creature_id][field_name][1];
            $td.siblings("td[data-roll-output-field]").html(`<div class="roll-result">${first_roll}</div><div class="roll-result">${second_roll}</div>`);
        }).fail(function(err){
            console.log(err);
        });

    });

    $("img.group-roll-image").on('click', function(){
        var $parentTable = $(this).closest('table.table');
        var encounter_id = $parentTable.attr('data-encounter-id');
        var $th = $(this).closest('th')
        var field_name = $th.attr('data-roll-field');
        var roll_type = $th.attr('data-roll-type');

        $.ajax({
            type: "POST",
            url: "http://localhost:8000/api/roll/",
            headers: { "Authorization": "Token " + AUTH_TOKEN },
            data: {
                "encounter_id": encounter_id,
                "field_name": field_name,
                "roll_type": roll_type,
                "roll_scope": "group"
            },
        }).done(function(data){
            console.log(data);
        }).fail(function(err){
            console.log(err);
        });
    });
})