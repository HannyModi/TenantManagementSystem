// Function to handle the agents status on the click of agent-act button.
$('.agent-act').click(function () {
    var ag_id;
    var act;
    ag_id = $(this).attr("data-id");
    act = $(this).attr("data-act");
    $.get('/Admin/agent_action/', { id: ag_id, is_active: act }, function (data) {
    });
    if(act=="0")
    {
        $("#td"+ag_id).html("Retired")
        $(this).attr("data-act","1");
        $(this).val("Activate");
        $(this).removeClass("btn-danger").addClass("btn-success");
    }
    else
    {   
        $("#td"+ag_id).html("Active")
        $(this).attr("data-act","0");
        $(this).val("Retire");
        $(this).removeClass("btn-success").addClass("btn-danger");
    }
});

// Searching in Agent request on search textbox
$('#search').keyup(function () {
    var query;
    query = $(this).val();
    $.get('/Admin/agent_request_search/', { suggestion: query }, function (data) {
        $('#tbl_agents').html(data);
    });
});

// Enabling User to create clone 
// Showing user clone_div area to create clone
$("#create_clone").change(function () {
    if($(this).attr("checked"))
    {
        $("#clone_div").removeClass("hidden");
    }
    else
    {
        $("#clone_div").addClass('hidden');
    }
    
});

// Creating the list of clones.
$('#clone_no').keyup(function () {  
    var no = $(this).val();
    if(Number(no)>50)
    {
        $('#clone_list').html("<strong> Can not create more than 50 clones</strong>");
    }
    else
    {
        $.get('/Admin/master_clone_list/', { clone_no: no}, function (data) {
            $('#clone_list').html(data);
        });
    }
});


// Showing Admin clone list while allocating Agent to Property.
$("#msp_list").change(function () {
    if($(this).val()=="Select item")
    {
        $("#property").addClass('hidden');
    }
    else
    {   
        $("#property").removeClass("hidden");
        $.get('/Admin/property_clone_list/', { msp: $(this).val()}, function (data) {
            $('#property').html(data);
        });
    }
    
});




// Showing more textboxes when user clicks plus button
$("#add_address").click(function () {
    var num = $("#num").val();
    // var new_html = '<input type="text" required name="pr_address'+num+'"/><a class="icon-minus-sign remove_address" ></a>';
    var new_html = '<div class="input-append" style="display:flex;" ><input class="span2" id="appendedInputButton" name="pr_address'+num+'" type="text"><button class="btn btn-theme remove_address" id="add_address" type="button"><i class="icon-minus"></i></button></div>'
    var new_num = Number(num)+1;
    $("#num").val(new_num);
    $("#addresses").append(new_html);
    $("#addresses").find('input').last().focus();
});

// Removing the textbox on click of minus button
$(".remove_address").live("click", function(){
    $(this).parent().remove();
    $(this).remove();
    
});



$('.decimal_input').keyup(function () {
    var $this = $( this );
            
            // Get the value.
            var input = $this.val();
            
            var input = input.replace(/[\D\s\._\-]+/g, "");
                    // input = input ? parseInt( input, 10 ) : 0;

                    $this.val( function() {
                        return ( input === 0 ) ? "" : input.toLocaleString( "en-IND" );
                    } );
});


// function mycall() 
// {
//    alert("aaya");
//    var num = $(this).attr("data-num");
//     $(this).prev('input').remove();
// }