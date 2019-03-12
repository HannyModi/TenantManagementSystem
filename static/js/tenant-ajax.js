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
    location.href = '/Admin/allocate_master_property/?agent=' + ag_id;
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

$('.allocate_clone').live('click', function () {
    var msp = $(this).attr('data-msp');
    var cln = $(this).attr('data-id');
    location.href = '/Admin/allocate_master_property/?msp=' + msp + '&cln=' + cln;
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
$('.search_tenant').live('keyup',function () {
    var status=$(this).attr('data-status');  
    var query;
    query = $(this).val();
    $.get('/Agent/tenant_search_list/', { suggestion: query,status: status }, function (data) {
        console.log(data);
        $('#tbl_active_tenants').html(data);       
    });
});


$('.pimg').live('click', function () {
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

$('.delete_master').live('click', function () {
    var $this = $(this);
    $.get('/Admin/delete_master_property/', { id: $(this).attr('data-id') }, function (data) {
        if (data == '1') {
            // location.reload('/admin/view_master_property/');
            $this.parent().parent().next().remove();
            $this.parent().parent().remove();
            alert('Property Sold and Removed from system ');
        }
        else {
            alert('Error accured while Deleting Property.')
        }
    })
});

$('.close').live('click', function () {
    $('#myModal').css('display', 'none');
    $('#imgDiv').css('display', 'none');

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
    if ($(this).attr('data-pid')) {
        pid = $(this).attr('data-pid');
        location.href = '/Agent/get_Tenant_list/?pid=' + pid + '&page=' + 'pdetails';
    }
    if ($(this).attr('data-tid')) {
        tid = $(this).attr('data-tid');
        location.href = '/Agent/get_Tenant_list/?tid=' + tid + '&page=' + 'tdetails';
    }
});

$('.deallocate_tenant').click(function () {
    if ($(this).attr('data-tid')) {
        tid = $(this).attr('data-tid');
        $.get('/Agent/deallocate_property/', { tenant: tid }, function (data) {
            if (data == "1") {
                status = "Property Deallocated";
                localStorage.setItem("Status", status);
                location.reload('/Agent/ViewTenants/');
            }
            else{
                $.notify("Error occured while Deallocation","error")

            }
        });
    }
    if ($(this).attr('data-pid')) {
        pid = $(this).attr('data-pid');
        $.get('/Agent/deallocate_property/', { property: pid }, function (data) {
            if (data) {
                status = "Property Deallocated";
                localStorage.setItem("Status", status);
                location.reload('/Agent/Agent_Properties/');
            }
            else{
                
                $.notify("Error occured while Deallocation","error")

            }

        });
    }
});


$(function () {
    $("select").select2();
});

//Make class visible for old tenants in insert tenant view
$('#old_tenant').click(function(){
    var response;
    $.get('/Agent/get_deactivated_tenant/',function(data){
         
        if (data != 0){
            console.log(data);     
      response = '<select id="selected_tenant" style="width:100%;" name="tn_id">'+
      '<option value="" selected>Select Tenant to make him active.</option>';
      $.each(data,function(item,value){
          $.each(value,function(i,v){
        console.log("Id = "+v.id)
        console.log("Name = "+v.tn_name)
        response+='<option value='+v.id+'>'+v.tn_name+'</option>';
          });
        });
        response+='</select>';
      }
      else{
          response='<strong id="selected_tenant">No Deactiavted tenant Found.</strong>'
      }
      console.log(response)
      $('#id_tn_name').replaceWith(response);
      $('#selected_tenant').select2();
    });
   
    // $('#id_tn_name').insertAfter(response);
    $('#id_tn_name').addClass('hidden');
    $('#Add_agent_again').removeClass("hidden");
    $('#Add_new_agent').addClass("hidden");
    $('#Add_agent_again').append("<input type='hidden' id='updatehide' name='update' value='update'></input>")

   
});

$('#new_tenant').click(function(){
    $('#selected_tenant').select2('destroy');
    $('#selected_tenant').replaceWith("<input type='text' name='tn_name' maxlength='25' id='id_tn_name'>");
   
    $('selected_tenant').addClass('hidden');
    
    $('#Add_agent_again').addClass("hidden");
    $('#Add_new_agent').removeClass("hidden");
    $('#id_tn_contact').val("");
    $('#updatehide').remove();
    $('#tenentimage').addClass('hidden');
    $('#id_tn_permanent_address').text("");
    $('#id_tn_reference_name').text("");
    $('#id_tn_reference_address').val("");
    $('#id_tn_reference_name').val("");
    $('#id_tn_document_description').val("");
    $('#select2-id_tn_document_description-container').text("Select");
    $('#id_tn_document').attr('required')
    $('#id_tn_profile').attr('required')
   });
   
$('#selected_tenant').live('change',function(){
 tid=$(this).val()
 $.get('/Agent/activate_tenant/',{tid:tid},function(data){
    $('#id_tn_contact').val(data.tn_contact);
    $('#id_tn_name').val(data.tn_name);
    $('#id_tn_permanent_address').text(data.tn_permanent_address);
    $('#id_tn_reference_name').text(data.tn_reference_name);
    $('#id_tn_reference_address').val(data.tn_reference_address);
    $('#id_tn_reference_name').val(data.tn_reference_name);
    $('#id_tn_document_description').val(data.tn_document_description);
    $('#select2-id_tn_document_description-container').text($('#id_tn_document_description option:selected').text());  
    var url='/media/';
    $('#tenant_profile').attr('src',url+data.tn_profile)
    $('#tenant_document').attr('src',url +data.tn_document)
    $('#tenentimage').removeClass('hidden')
    $('#id_tn_document').removeAttr('required')
    $('#id_tn_profile').removeAttr('required')
 })
});

$('#property').change(function(){
//    alert($(this).val());
$.get('/Agent/getrent/',{pid:$(this).val()},function(data){
    $('#rent').html("Rent is " + data);
    $('#rent').removeClass("hidden"); 
});
})


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

$('.deallocate_clone').live('click', function () {
    $.get('/Admin/deallocate_clone/', { id: $(this).attr('data-id') }, function (data) {
        if (data == '1') {
            alert('Property deallocated ');
            location.reload('/Admin/view_master_property/');
        }
        else {
            alert('Error accured while deallocating Property.')
        }
    })
});

$('.sold_property').live('click', function () {
    $.get('/Admin/property_soldout', { pr_id: $(this).attr('data-id') }, function (data) {
        if (data == "1") {
            status = "Properties Are Alocated";
            localStorage.setItem("Status", status);
            location.reload('/Admin/view_master_property/');
        }
    }
    );
});

$('.addvisit').live('click', function () {
    location.href = '/Agent/add_visit/?tid=' + $(this).attr('data-tid');

});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    $('#move_to').select2('destroy')
  });

$('.change_status').live('click',function(){
    $("#id").val($(this).attr('data-id'));
    $("#tn_name").val($(this).attr('data-tnname'));
    $("#tn_status").val($(this).attr('data-status'));
    $('#select2-tn_status-container').html($(this).html())
    $('#myModal').css('display', 'block');

});

$('#save_tenant_status').live('click',function(){
    id=$('#id').val()
    status=$('#tn_status').val()
    // alert("Id is :"+id+"Status is :"+status);
    $.get('/Agent/tenant_status_change',{id:id,status:status},function(data){
        if(data == '1')
        {
            status = "Status Changed Successfully";
            localStorage.setItem("Status", status);
            location.reload('/Agent/ViewTenants/');
        }
        else{
            $.notify("Error occured while updatinf Tenant Status","error")
        }
    });
});

$('.move_from').live('click', function () {
    // alert($('#move_from option:selected'))
    // $('#move_from').select2(destroy);
    $('#move_from option:selected').remove().appendTo('#move_to');
    $('#move_to option').attr('selected', 'selected');

});

$('.move_to').live('click', function () {
    // alert($('#move_from option:selected'))
    $('#move_to option:selected').remove().appendTo('#move_from');
    $('#move_to option').attr('selected', 'selected');

});

$('.move_all_from').live('click', function () {
    // alert($('#move_from option:selected'))
    $('#move_from option').remove().appendTo('#move_to');
    $('#move_to option').attr('selected', 'selected');

});

$('.move_all_to').live('click', function () {
    // alert($('#move_from option:selected'))
    $('#move_to option').remove().appendTo('#move_from');
    $('#move_to option').attr('selected', 'selected');

});

function check_existance(){
    $('#move_to option').each(function(){
        $('#move_from option[value='+($(this).val())+']').remove();
    }); 
      
}


// Showing user clone_div area to create clone
$("#msp").change(function () {
    if ($(this).val() == "") {
        $("#property").addClass('hidden');
    }
    else {
        $("#property").removeClass("hidden");
        $.get('/Admin/move_to_clone_list/', { msp: $(this).val() }, function (data) {
            $('#property').html(data);
            $('#to_clone').select2();
        });
    }


});

// Showing user clone_div area to create clone
$("#msp_create_clone").change(function () {
    if ($(this).val() == "") {
        $("#property").addClass('hidden');
    }
    else {
        $("#property").removeClass("hidden");       
    }
});


// Showing user clones for selecting property
$("#to_clone").live('change', function () {

    $("#manage_by_property").removeAttr('checked')
    if ($(this).val() == "") {
        $("#clone_div").addClass("hidden");
    }
    else {
        $("#clone_div").removeClass("hidden");
        $("#property_list").addClass('hidden');
        $('#clone_list').removeClass('hidden');
        $.get('/Admin/move_from_clone_list/', {
            msp: $('#msp').val(),
            cln: $('#to_clone').val()
        }, function (data) {
            $('#clone_list').html(data);
            $('#from_clone').select2();
        });
    }


});

// Showing user clones for selecting property
$("#from_clone").live('change', function () {
    if ($(this).val() == "") {
        $("#property_list").addClass("hidden");
    }
    else {
        $('#property_list').removeClass("hidden");
        $.get('/Admin/show_properties/', {
            id: $('#from_clone').val(),
            is_master: false
        }, function (data) {
            $('#property_select').html(data);
            check_existance();
        });
    }


});

// Showing user properties area to create clone
$("#manage_by_property").change(function () {
    if ($(this).attr("checked")) {
        $("#clone_list").addClass('hidden');
        $('#property_list').removeClass("hidden");
        $.get('/Admin/show_properties/', {
            id: $('#msp').val(),
            cln: $('#to_clone').val(),
            is_master: true
        }, function (data) {
            $('#property_select').html(data);
            check_existance();
        });
    }
    else {
        $("#property_list").addClass('hidden');
        $('#clone_list').removeClass('hidden');
        $.get('/Admin/move_from_clone_list/', {
            msp: $('#msp').val(),
            cln: $('#to_clone').val()
        }, function (data) {
            $('#clone_list').html(data);
            $('#from_clone').select2();
        });
    }

});


// Showing Admin clone list while allocating Agent to Property.
$("#msp_list").change(function () {
   
    if ($(this).val() == "Select item") {
        $("#property").addClass('hidden');
     
    }
    else {
        $("#property").removeClass("hidden");
        // if(){
        //     alert($(this).attr('data-unallocated'))}
        $.get('/Admin/property_clone_list/', {
            msp: $(this).val(),
            unallocated: $(this).attr('data-unallocated')
        }, function (data) {
            $('#property').html(data);
            $('#cln_list').select2();
            $('#msp_list3').select2();
        });
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

$('.deactivate').live('click',function(){
    var id=$(this).attr('data-id')
    $.get('/Agent/activation_change_tenant/',{id:id,change:'deactivate'},function(data){
        if(data == "Done")
        {
            status="Tenant Dectivated";
            localStorage.setItem("Status", status);
            location.reload('/Agent/ViewTenants/');
        }
        else
        $.notify('Error occured during deactivation','error');
    })
})

$('.activate').live('click',function(){
    var id=$(this).attr('data-id')
    $.get('/Agent/activation_change_tenant/',{id:id,change:'activate'},function(data){
        if(data == 'Done')
        {
            status="Tenant Activated";
            localStorage.setItem("Status", status);
            location.reload('/Agent/ViewTenants/');
        }
        else
        $.notify('Error occured during deactivation','error');
    })
})

// $(document).ready(function(){
//     $('input[type="date"]').click(function(){
//         alert(this.value);         //Date in full format alert(new Date(this.value));
//         var inputDate = new Date(this.value);
//     });
// });

function validatedate(){
var startdate=$('#agreement_start_date').val();
var enddate=$('#agreement_end_date').val();
console.log("Satrt Date = "+ $('#agreement_start_date').val());
console.log("End Date = "+ $('#agreement_end_date').val());
if(Date.parse(enddate) <= Date.parse(startdate))
{
$.notify("End date should be bigger than start date","info")
return false
}
else{
    return true
}
};


// $('#agreement_start_date').change(function() { 
// var datearray = $('#agreement_start_date').val().split("-");
// var montharray = ["Jan", "Feb", "Mar","Apr", "May", "Jun","Jul", "Aug", "Sep","Oct", "Nov", "Dec"];
// var year = "20" + datearray[2];
// var month = montharray.indexOf(datearray[1])+1;
// var day = datearray[0];
// var minDate = (year +"-"+ month +"-"+ day);
// $('#agreement_end_date').attr('min',minDate); 
// });

    