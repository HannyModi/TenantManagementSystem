// Function to handle the agents status on the click of agent-act button.
$('.agent-act').click(function () {
    var ag_id;
    var act;
    ag_id = $(this).attr("data-id");
    act = $(this).attr("data-act");
    $.get('/Admin/agent_action/', { id: ag_id, is_active: act }, function (data) {
    });
    if (act == "0") {
        $("#td" + ag_id).html("Retired")
        $(this).attr("data-act", "1");
        $(this).val("Activate");
        $(this).removeClass("btn-danger").addClass("btn-success");
    }
    else {
        $("#td" + ag_id).html("Active")
        $(this).attr("data-act", "0");
        $(this).val("Retire");
        $(this).removeClass("btn-success").addClass("btn-danger");
    }
});

// Allocating property to agent if he is active
$('.agent-allocate').live("click", function () {
    var ag_id = $(this).attr("data-id");
    location.href = '/Admin/allocate_master_property/?agent='+ag_id;
});

// Searching in Agent request on search textbox
$('#search').keyup(function () {
    var query;
    query = $(this).val();
    $.get('/Admin/agent_request_search/', { suggestion: query }, function (data) {
        $('#tbl_agents').html(data);
    });
});

// Searching in Agent request on search textbox
$('#searchAgents').keyup(function () {
    var query;
    query = $(this).val();
    $.get('/Admin/active_agent_search/', { suggestion: query }, function (data) {
        $('#tbl_agents').html(data);
    });
});

// Enabling User to create clone 
// Showing user clone_div area to create clone
$("#create_clone").change(function () {
    if ($(this).attr("checked")) {
        $("#clone_div").removeClass("hidden");
    }
    else {
        $("#clone_div").addClass('hidden');
    }

});

// Creating the list of clones.
$('#clone_no').keyup(function () {
    var no = $(this).val();
    if (Number(no) > 50) {
        $('#clone_list').html("<strong> Can not create more than 50 clones</strong>");
    }
    else {
        $.get('/Admin/master_clone_list/', { clone_no: no }, function (data) {
            $('#clone_list').html(data);
        });
    }
});


// Showing Admin clone list while allocating Agent to Property.
$("#msp_list").change(function () {
    if ($(this).val() == "Select Property") {
        $("#property").addClass('hidden');
    }
    else {
        $("#property").removeClass("hidden");
        $.get('/Admin/property_clone_list/', { msp: $(this).val() }, function (data) {
            $('#property').html(data);
            $('#msp_list3').select2();
        });
    }
});

//Unallocated master Property list
$("#msp_list2").change(function () {
    if ($(this).val() == "Select Property") {
        $("#property").addClass('hidden');
    }
    else {
        $("#property").removeClass("hidden");
        $.get('/Admin/unallocated_clone_list/', { msp: $(this).val() }, function (data) {
            $('#property').html(data);
            $('#msp_list3').select2();
        });
    }
});

$('.allocate_clone').live('click',function () {
    var msp = $(this).attr('data-msp');
    var cln = $(this).attr('data-id');
    location.href = '/Admin/allocate_master_property/?msp='+msp+'&cln='+cln;
});

// Showing more textboxes when user clicks plus button
$("#add_address").click(function () {
    var num = $("#num").val();
    // var new_html = '<input type="text" required name="pr_address'+num+'"/><a class="icon-minus-sign remove_address" ></a>';
    var new_html = '<div class="input-append" style="display:flex;" ><input class="span2" id="appendedInputButton" name="pr_address' + num + '" type="text"><button class="btn btn-theme remove_address" id="add_address" type="button"><i class="icon-minus"></i></button></div>'
    var new_num = Number(num) + 1;
    $("#num").val(new_num);
    $("#addresses").append(new_html);
    $("#addresses").find('input').last().focus();
});

// Removing the textbox on click of minus button
$(".remove_address").live("click", function () {
    $(this).parent().remove();
    $(this).remove();

});

$('.decimal_input').keyup(function () {
    var $this = $(this);

    // Get the value.
    var input = $this.val();

    var input = input.replace(/[\D\s\._\-]+/g, "");
    // input = input ? parseInt( input, 10 ) : 0;

    $this.val(function () {
        return (input === 0) ? "" : input.toLocaleString("en-IND");
    });
});

// Searching in Agent request on search textbox
$('#abc').keyup(function () {
    var query;
    query = $(this).val();
    $.get('/Agent/tenant_search_list/', { suggestion: query }, function (data) {
        $('#tbl_tenants').html(data);
    });
});

$('.pimg').click(function () {
    $('#imgDiv').css('display', "block");
    $('#img01').attr('src', $(this).attr('src'));
    $('#caption').html($(this).attr('alt'));
});

$('#save').click(function () {
    $.get('/Admin/edit_property/', {
        id: $("#id").val(),
        rent: parseFloat($("#pr_rent").val()),
        deposite: parseFloat($("#pr_deposite").val()),
        description: $("#pr_description").val()
    }, function (data) {
        if (data == '1') {
            alert("Data updated Successfully")
            $tr.children('.pr_rent').html(parseFloat($("#pr_rent").val()).toFixed(2))
            $tr.children('.pr_deposite').html(parseFloat($("#pr_deposite").val()).toFixed(2))
            $tr.children('.pr_description').html($("#pr_description").val())
            $('#myModal').css('display', 'none')
        }
        else {

            alert("Data not updated Successfully")
        }
    });
});

$('.delete_master').live('click',function () {
    var $this = $(this);
    $.get('/Admin/delete_master_property/',{id: $(this).attr('data-id')},function(data){
        if(data=='1'){
            // location.reload('/admin/view_master_property/');
            $this.parent().parent().next().remove();
            $this.parent().parent().remove();
            alert('Property Sold and Removed from system ');
        }
        else{
            alert('Error accured while Deleting Property.')
        }
    })
});

$('.close').click(function () {
    $('#myModal').css('display', 'none');
    $('#imgDiv').css('display','none');

});

$('#close').click(function () {
    $('#myModal').css('display', 'none')
});



$(document).ready(function () {
    //get it if Status key found
    var str;
    if (localStorage.getItem("Status")) {
        str = localStorage.getItem("Status")
        $.notify(str, "success");
        localStorage.clear();
    }
});

$(".allocate_tenant").click(function () {
    if($(this).attr('data-pid')){
        pid = $(this).attr('data-pid');
        location.href='/Agent/get_Tenant_list/?pid='+pid+'&page='+'pdetails';   
    }
    if($(this).attr('data-tid')){
        tid=$(this).attr('data-tid');
        location.href='/Agent/get_Tenant_list/?tid='+tid+'&page='+'tdetails';   
    }    
});

$('.deallocate_tenant').click(function () {
    tid = $(this).attr('data-tid');
    $.get('/Agent/deallocate_property/', { tenant: tid }, function (data) {
        if (data){
            status = "Property Deallocated";
            localStorage.setItem("Status", status);
            location.reload('/Agent/ViewTenants/');         
    }
    });
});


$(function () {
    $("select").select2();
});

$('#id_user_permissions_add_link').click(function(e) {
    move_selection(e, this, SelectBox.move, field_id + '_from', field_id + '_to');
  });

  $('.show_data').click(function () {
    var id = $(this).attr('data-id');
    var hidden = $(this).attr('data-hidden');
    var act = $(this).attr('data-act');

    if (hidden == '1') {
        $(this).parent().siblings().children(
            '.show_data').html('<i class="icon-angle-down"></i>');
        $(this).parent().siblings().children(
            '.show_data').attr('data-hidden', '1');
        $("#tr" + id).removeClass("hidden");
        $(this).html('<i class="icon-angle-up"></i>');
        $(this).attr('data-hidden', '0');
        $.get('/Admin/show_data/', { id: id, act: act }, function (data) {
            $('#tbldisp').removeClass('fixed_header');
            $('#td' + id).html(data);
        });
    }
    else if (hidden == '0') {
        $("#tr" + id).addClass("hidden");
        $(this).html('<i class="icon-angle-down"></i>');
        $(this).attr('data-hidden', '1');
    }
});

$('.edit_property').live('click', function () {
    $('#myModal').css('display', 'block');
    $tr = $(this).parent().parent();
    $("#id").val($(this).attr('data-id'))
    $("#pr_address").val($tr.children('.pr_address').html())
    $("#pr_clone").val($tr.children('.pr_clone').html())
    $("#pr_status").val($tr.children('.pr_status').html())
    $("#pr_rent").val($tr.children('.pr_rent').html())
    $("#pr_deposite").val($tr.children('.pr_deposite').html())
    $("#pr_description").val($tr.children('.pr_description').html())
    // alert($tr.children('.pr_address').html())
    // $('#pr_address').val();
    $ref = $tr;
})

$('.deallocate_clone').live('click',function () {
    $.get('/Admin/deallocate_clone/',{id: $(this).attr('data-id')},function(data){
        if(data=='1'){
            alert('Property deallocated ');
            location.reload('/Admin/view_master_property/');
        }
        else{
            alert('Error accured while deallocating Property.')
        }
    })
});

$('.sold_property').live('click',function(){
$.get('/Admin/property_soldout',{pr_id:$(this).attr('data-id')},function(data){
    if(data=="1"){
        status = "Properties Are Alocated";
        localStorage.setItem("Status", status);
        location.reload('/Admin/view_master_property/');
    }}
);
});

$('.addvisit').live('click',function(){
    location.href='/Agent/add_visit/?tid='+$(this).attr('data-tid');

});