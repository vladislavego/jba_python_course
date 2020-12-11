$(document).ready(function() {

    csrf = $('input[name="csrfmiddlewaretoken"]').val()

    $("#show_contacts").click(function(){ 
        $.ajax({
            type: "GET",
            url: "",
            data: {
                action: "show"
            },
            success: function(response){
                $("#contacts_table").html(response.contacts_table);
            }
        })
    });

    $("#hide_contacts").click(function(){ 
        $.ajax({
            type: "GET",
            url: "",
            data: {
                action: "hide"
            },
            success: function(response){
                $("#contacts_table").html(response.contacts_table);
            }
        })
    })

    $("#add_contact").click(function() {
        var data = $("#new_contact").serialize();
        $.ajax({
            type: "POST",
            url: "",
            data: data,
            success: function(response){
                if (response.contact_description){
                    $("#contacts_table").append(response.contact_description);
                    $("#new_contact").html(response.contact_form);
                }else{
                    $("#new_contact").html(response.contact_form);
                }
            }, 
        });
    });

});


