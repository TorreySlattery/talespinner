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
            var first_roll = data["results"][creature_id][0];
            var second_roll = data["results"][creature_id][1];
            $td.siblings("td[data-roll-output-field]").html(
            `
                <div class="roll-result">${first_roll["total"]}</div>
                <div class="roll-result">${second_roll["total"]}</div>
            `
            );
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
            results = data["results"]
            for (var creature_id in results){
                if (results.hasOwnProperty(creature_id)) {
                    var $tr = $parentTable.find(`tr[data-creature-id='${creature_id}']`);
                    var first_roll = data["results"][creature_id][0];
                    var second_roll = data["results"][creature_id][1];
                    var $td = $tr.find(`td[data-roll-field='${field_name}']`);
                    $td.html(`
                        <div class="roll-result">${first_roll["total"]}</div>
                        <div class="roll-result">${second_roll["total"]}</div>
                    `)
                }
            }
        }).fail(function(err){
            console.log(err);
        });
    });

    $("a[data-roll-type='attack']").on('click', function(e){
        e.preventDefault();
        var creature_id = $(this).closest("div[data-creature-id]").attr("data-creature-id")
        var field_name = $(this).attr('data-roll-field');
        var roll_type = $(this).attr('data-roll-type');
        var $outputTable = $(this).closest("div.row").find("table.attack-roll-output-table");

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
            var rolls = data["results"][creature_id];
            var tdExtraClass1 = rolls[0]["base"] == 20 ? "critical-success" : "";
            tdExtraClass1 = rolls[0]["base"] == 1 ? "critical-failure" : tdExtraClass1;
            var tdExtraClass2 = rolls[1]["base"] == 20 ? "critical-success" : "";
            tdExtraClass2 = rolls[1]["base"] == 1 ? "critical-failure" : tdExtraClass2;
            $outputTable.find("td[data-attack-roll-1]").html(rolls[0]["total"]).removeClass("critical-success critical-failure").addClass(tdExtraClass1);
            $outputTable.find("td[data-attack-dmg-1]").html(rolls[0]["damage"]["total"]);
            $outputTable.find("td[data-attack-avg-1]").html(rolls[0]["damage"]["avg"]);

            $outputTable.find("td[data-attack-roll-2]").html(rolls[1]["total"]).removeClass("critical-success critical-failure").addClass(tdExtraClass2);
            $outputTable.find("td[data-attack-dmg-2]").html(rolls[1]["damage"]["total"]);
            $outputTable.find("td[data-attack-avg-2]").html(rolls[1]["damage"]["avg"]);
        }).fail(function(err){
            console.log(err);
        });
    });
})