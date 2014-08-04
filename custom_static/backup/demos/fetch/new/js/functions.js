/*
* Author: SIMON GOMES <busy.s.simon@gmail.com>
* Description : jQuery functions including menu functions.
* Date: August 6, 2012 
*/

// Email Validation Function
function valid_email(email){
    var pattern= new RegExp(/^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]+$/);
    return pattern.test(email);
}

function item_details() {
    $('.item-details').hide();
    $('.guest-name').click(function(){
        var $itemDetails = $(this).parent().parent().parent().find('div.item-details');
        if ($itemDetails.css('display') == 'none') {
            $(this).css( 'color', '#f9a44a');
            $('.edit').hide();
            $itemDetails.show();
        }
        else {
            $(this).css( 'color', '#66cb29');
            $('.edit').hide();
            $itemDetails.hide();
        }
        return false;
    });
    $('.item1 .add-comment').click(function(){
        $('.item1 .guest-name').css( 'color', '#f9a44a');
        $('.item1 .item-details:first').show();
        return false;
    });
}

function send_offer_response() {
    var csrftoken = $.cookie('csrftoken');
    $(".offer-response").on('click', function(event) {
        event.preventDefault();
        var pk = $(this).data('pk');
        data = {
            'csrfmiddlewaretoken': csrftoken,
            'lead_id': pk
        };
        $.ajax({
            type : "POST",
            url : "/fetch/send-offer-response/",
            data : data,
            beforeSend: function() {
                $('#loader').show();
            },
            complete: function(){
                $('#loader').hide();
                var content = "<p>Special offer has been successfully flagged.</p>";
                $('#emailSuccessId').dialog('option', 'title', 'Special Offer Template');
                $('#emailSuccessId').html(content);
                $("#emailSuccessId").dialog("open");
            },
            success: function(response) {
                if(response['success'] == 1){
                    var divClass = '.offer-response-' + pk + '';
                    var $flagSpan = $(divClass).find('span');
                    $flagSpan.removeClass('gray').addClass('yellow');

                    var divClass2 = '.emails-sent';
                    $(divClass2).html(response['emails_sent']);
                }
            }
        });
    });
}

function send_second_response() {
    var csrftoken = $.cookie('csrftoken');
    $(".second-response").on('click', function(event) {
        event.preventDefault();
        var pk = $(this).data('pk');
        data = {
            'csrfmiddlewaretoken': csrftoken,
            'lead_id': pk
        };
        $.ajax({
            type : "POST",
            url : "/fetch/send-second-response/",
            data : data,
            beforeSend: function() {
                $('#loader').show();
            },
            complete: function(){
                $('#loader').hide();
                var content = "<p>Follow up response has been successfully flagged.</p>";
                $('#emailSuccessId').dialog('option', 'title', 'Second Response Template');
                $('#emailSuccessId').html(content);
                $("#emailSuccessId").dialog("open");
            },
            success: function(response) {
                if(response['success'] == 1){
                    var divClass = '.second-response-' + pk + '';
                    var $flagSpan = $(divClass).find('span');
                    $flagSpan.removeClass('gray').addClass('blue');

                    var offerResponseLinkDivClass = '.offer-response-link-' + pk + '';
                    var link = '| <a href="#" class="offer-response" data-pk=' + pk + '>Send special offer</a><br/>';
                    $(offerResponseLinkDivClass).html(link);
                    send_offer_response();

                    var divClass2 = '.emails-sent';
                    $(divClass2).html(response['emails_sent']);
                }
            }
        });
    });
}

$(document).ready(function(){
	$('.dashboard-button').click(function(){
		window.location = "manager_dashboard.php";
	});

	/*------------ goal field function ----------*/
	$('#goal').click(function(){
		$(this).addClass('goal-click');
		$(this).removeClass('goal');
	});
	$('#goal').blur(function(){
		$(this).addClass('goal');
		$(this).removeClass('goal-click');
	});

	/*----------- Retriever comment functionalities ------------*/
	item_details();

	$('.see-them').hover(function () {
        // Do something on mouseover
        var position = $(this).offset();

        $('#bingoboard-tooltip').text($(this).data("tooltip")).css({
            position: "absolute",
            top: (position['top']+$(this).height()+15),
            left: position['left']
        }).show();
	}, function () {
        // Do something on mouseout
        $('#bingoboard-tooltip').hide();
    });
	$('.flag-legend').hover(function () {
        // Do something on mouseover
        var position = $(this).offset();
        $('#bingoboard-tooltip').text($(this).data("tooltip")).css({
            position: "absolute",
            top: (position['top']+$(this).height()+5),
            left: position['left']
        }).show();
	}, function () {
        // Do something on mouseout
        $('#bingoboard-tooltip').hide();
	});
	$('.status-flag').hover(function () {
        // Do something on mouseover
        var position = $(this).offset();

        $('#bingoboard-tooltip').text($(this).data("tooltip")).css({
            position: "absolute",
            top: (position['top']+$(this).height()+5),
            left: position['left']
        }).show();
	}, function () {
        $('#bingoboard-tooltip').hide();
	});

    (function poll(){
        $.ajax({
            url: "/fetch/get-alerts/",
            success: function(data){
                var spanAlertID = "#alert-id";
                $(spanAlertID).html(data["alerts"]);

                var spanCommentID = "#comment-alert-id";
                $(spanCommentID).html(data["comments"]);

                if(data["alerts"] != "No New Alerts") {
                    $('.alert').css( 'background-color', 'red');
                }
                else {
                    $('.alert').css( 'background-color', 'transparent');
                }
            },
            dataType: "json",
            complete: setTimeout(poll, 10000),
            timeout: 10000
        });
    })();
});
$(document).ready(function() {
    $('.goal').prop('disabled', true);
    $('.validateTips').hide();
    $('#loader').hide();
    $('#emailSuccessId').hide();
    var csrftoken = $.cookie('csrftoken');
    tinyMCE.init({
        mode : "exact",
        elements : "emailContentId",
        theme: "advanced",
        plugins: "spellchecker,directionality,paste,searchreplace"
    });
    send_second_response();
    send_offer_response();

    maxHeight = 0;
    $(".result-holder li.align").each(function() {
         maxHeight = maxHeight > $(this).height() ? maxHeight : $(this).height();
    });
    $("#fetch-booking-toolbar-add-guest").on('click', function(event) {
        event.preventDefault();
        $("#add-guest-form-id").dialog("open");
    });
    $("#add-guest-form-id").dialog({
        autoOpen : false,
        resizable: false,
        height:'auto',
        width:'auto',
        modal: true,
        buttons: {
            "Add Guest": function(event) {
                var guest_name = $('#id_guest_name').val();
                var guest_email = $('#id_guest_email').val();
                var guest_phone = $('#id_guest_phone').val();

                var property = $('#id_fetch_property').val();
                var source = $('#id_source').val();

                var arrival_month = $('#add-guest-form-id #id_arrival_month').val();
                var arrival_day = $('#add-guest-form-id #id_arrival_day').val();
                var arrival_year = $('#add-guest-form-id #id_arrival_year').val();
                var departure_month = $('#add-guest-form-id #id_departure_month').val();
                var departure_day = $('#add-guest-form-id #id_departure_day').val();
                var departure_year = $('#add-guest-form-id #id_departure_year').val();

                var adults = $('#id_adults').val();
                var children = $('#id_children').val();

                var message = $('#id_message').val();

                var data = {
                    'csrfmiddlewaretoken': csrftoken,
                    'guest_name': guest_name,
                    'guest_email': guest_email,
                    'guest_phone': guest_phone,
                    'property': property,
                    'source': source,
                    'arrival_month': arrival_month,
                    'arrival_day': arrival_day,
                    'arrival_year': arrival_year,
                    'departure_month': departure_month,
                    'departure_day': departure_day,
                    'departure_year': departure_year,
                    'adults': adults,
                    'children': children,
                    'message': message
                };

                $.ajax({
                    type : "POST",
                    url : "/fetch/add-guest/",
                    data : data,
                    beforeSend: function() {
                        $('#loader').show();
                    },
                    complete: function(){
                        $('#loader').hide();
                        var content = "<p>Guest has been successfully added.</p>";
                        $('#emailSuccessId').dialog('option', 'title', 'Add Guest');
                        $('#emailSuccessId').html(content);
                        $("#emailSuccessId").dialog("open");
                        $("#emailSuccessId").bind('dialogclose', function(event) {
                            location.reload();
                        });
                    },
                    success : function(response) {
                    }
                });
                $( this ).dialog( "close" );
            },
            Cancel: function() {
                $( this ).dialog( "close" );
                $('#id_guest_name').val('');
                $('#id_guest_email').val('');
                $('#id_guest_phone').val('');
                $('#id_fetch_property').val('');
                $('#add-guest-form-id #id_arrival_month').val('');
                $('#add-guest-form-id #id_arrival_day').val('');
                $('#add-guest-form-id #id_arrival_year').val('');
                $('#add-guest-form-id #id_departure_month').val('');
                $('#add-guest-form-id #id_departure_day').val('');
                $('#add-guest-form-id #id_departure_year').val('');
                $('#id_adults').val('');
                $('#id_children').val('');
                $('#id_message').val('');
            }
        },
        close : function() {
        }
    }).css("font-size", "16px");

    $("#emailSuccessId").dialog({

        autoOpen : false,
        resizable: false,
        height:140,
        modal: true,
        buttons: {
            Close: function() {
                $( this ).dialog( "close" );
            }
        },
        close : function() {
        }
    }).css("font-size", "16px");

    $("#fetch-send-first-response-form").dialog({
        autoOpen : false,
        resizable: true,
        height: 'auto',
        width: 'auto',
        modal: true,
        buttons: {
            "Edit Dates": function(event) {
                var available_from = $(this).data("availablefrom");
                var available_to = $(this).data("availableto");
                var lead_id = $(this).data("pk");
                $("#fetch-preview-first-response").data("lead_id", lead_id);
                var data = {
                    "csrfmiddlewaretoken": csrftoken,
                    "available_from": available_from,
                    "available_to": available_to,
                    "lead_id": lead_id
                };
                $.ajax({
                    type : "POST",
                    url : "/fetch/edit-dates/",
                    data : data,
                    beforeSend: function() {
                        $('#loader').show();
                    },
                    complete: function(){
                        $('#loader').hide();
                    },
                    success : function(response) {
                        // html for property form modal
                        if(response['success'] == 1){
                            $('#property-dates-form').html(response['form']);
                            $("#property-dates-form").dialog("open");
                        }
                    }
                });
                $( this ).dialog( "close" );
            },
            "Set Property Rates": function(event) {
                var lead_id = $(this).data('pk');
                $("#fetch-preview-first-response").data("lead_id", lead_id);
                var properties = $(this).find("select[name=property_name]").val();
                var is_available = $(this).find("input[name=is_available]").is(':checked');
                var data = {
                    'csrfmiddlewaretoken': csrftoken,
                    'lead_id': lead_id,
                    'properties': properties,
                    'is_available': is_available
                };
                $.ajax({
                    type : "POST",
                    url : "/fetch/set-property-rates/",
                    data : data,
                    beforeSend: function() {
                        $('#loader').show();
                    },
                    complete: function(){
                        $('#loader').hide();
                    },
                    success : function(response) {
                        // html for property form modal
                        if(response['success'] == 1){
                            $('#property-rates-form').html(response['formset']);
                            $("#property-rates-form").data("lead_id", response['lead_id']);
                            $("#property-rates-form").data("properties", response['properties']);
                            $("#property-rates-form").data("is_available", response['is_available']);
                            $("#property-rates-form").dialog("open");
                        }
                        else if(response['success'] == 2){
                            $('#property-rates-form').html("<h1>You have not chosen any property</h1>");
                            $("#property-rates-form").dialog("open");
                        }
                    }
                });
                $( this ).dialog( "close" );
            },
            "See Template Preview": function(event) {
                var lead_id = $(this).data("pk");
                var available_from = $(this).data("availablefrom");
                var available_to = $(this).data("availableto");
                $("#fetch-preview-first-response").data("lead_id", lead_id);
                var properties = $(this).find("select[name=property_name]").val();
                var is_available = $(this).find("input[name=is_available]").is(":checked");
                var data = {
                    "csrfmiddlewaretoken": csrftoken,
                    "available_from": available_from,
                    "available_to": available_to,
                    "lead_id": lead_id,
                    "properties": properties,
                    "is_available": is_available
                };
                $.ajax({
                    type : "POST",
                    url : "/fetch/preview-first-response/",
                    data : data,
                    beforeSend: function() {
                        $('#loader').show();
                    },
                    complete: function(){
                        $('#loader').hide();
                    },
                    success : function(response) {
                        var htmlContent = "<textarea id='emailContentId' rows='15' cols='80' style='resize:none;'>"+response+"</textarea>";
                        $(".email-content").html(htmlContent);
                        tinyMCE.init({
                            mode : "exact",
                            elements : "emailContentId",
                            theme: "advanced",
                            theme_advanced_buttons1 : "mybutton,bold,italic,underline,separator,strikethrough,justifyleft,justifycenter,justifyright, justifyfull,bullist,numlist,undo,redo,link,unlink, code",
                            width: "100%",
                            height: "200",
                            plugins : "noneditable",
                            noneditable_regexp: /\[\[[^\]]+\]\]/g
                        });
                        $("#fetch-preview-first-response").dialog("open");
                    }
                });
               $( this ).dialog( "close" );
            },
            Cancel: function() {
                $( this ).dialog( "close" );
                $(this).data("availablefrom", "");
                $(this).data("availableto", "");
                $("#id_property_name option").prop("selected", false);
            }
        },
        close : function() {
        }
    }).css("font-size", "16px");

    $("#property-dates-form").dialog({
        autoOpen : false,
        resizable: false,
        height: 'auto',
        width: 'auto',
        modal: true,
        buttons: {
            "Save Dates": function(event) {
                var form = $(this).find("#edit-dates-form");
                var data = {
                    'csrfmiddlewaretoken': csrftoken,
                    'date-form': form.serialize()
                };
                $.ajax({
                    type : "POST",
                    url : "/fetch/save-dates/",
                    data : data,
                    beforeSend: function() {
                        $('#loader').show();
                    },
                    complete: function(){
                        $('#loader').hide();
                    },
                    success : function(response) {
                        if(response["success"] == 1) {
                            $("#fetch-send-first-response-form").data("availablefrom", response["available_from"]);
                            $("#fetch-send-first-response-form").data("availableto", response["available_to"]);
                            $("#fetch-send-first-response-form").dialog("open");
                        }
                    }
                });
                $( this ).dialog( "close" );
            },

            Cancel: function() {
                $( this ).dialog( "close" );
                if($("#fetch-send-first-response-form").data("availablefrom") === "") {
                    $("#fetch-send-first-response-form").data("availablefrom", "");
                }
                if($("#fetch-send-first-response-form").data("availableto") === "") {
                    $("#fetch-send-first-response-form").data("availableto", "");
                }
                $("#fetch-send-first-response-form").dialog("open");
            }
        },
        close : function() {
        }
    }).css("font-size", "16px");

    $("#property-rates-form").dialog({
        autoOpen : false,
        resizable: false,
        height: 'auto',
        width: 'auto',
        modal: true,
        buttons: {
            "Save Rates": function(event) {
                var formset = $(this).find("#set-property-rates-form");
                var data = {
                    'csrfmiddlewaretoken': csrftoken,
                    'formset': formset.serialize()
                };
                $.ajax({
                    type : "POST",
                    url : "/fetch/save-rates/",
                    data : data,
                    beforeSend: function() {
                        $('#loader').show();
                    },
                    complete: function(){
                        $('#loader').hide();
                    },
                    success : function(response) {
                        if(response["success"] == 1) {
                            $("#fetch-send-first-response-form").dialog("open");
                        }
                    }
                });
                $( this ).dialog( "close" );
            },

            Cancel: function() {
                $( this ).dialog( "close" );
                $("#fetch-send-first-response-form").dialog("open");
            }
        },
        close : function() {
        }
    }).css("font-size", "16px");

    var mail_sent = true;
    $("#fetch-preview-first-response").dialog({
        autoOpen : false,
        resizable: true,
        height: 300,
        width: 600,
        modal: true,
        buttons: {
            "Send Email": function(event) {
                    var content = tinyMCE.activeEditor.getContent();
                    var lead_id = $(this).data("lead_id");
                    var data = {
                        'csrfmiddlewaretoken': csrftoken,
                        'content': content,
                        'lead_id': lead_id
                    };
                    $.ajax({
                        type : "POST",
                        url : "/fetch/send-first-response/",
                        data : data,
                        beforeSend: function() {
                            $('#loader').show();
                        },
                        complete: function(){
                            $('#loader').hide();
                            var content = "<p>First response has been successfully flagged.</p>";
                            $('#emailSuccessId').dialog('option', 'title', 'First Response Template');
                            $('#emailSuccessId').html(content);
                            $("#emailSuccessId").dialog("open");
                            $("#id_property_name option").prop("selected", false);
                        },
                        success : function(response) {
                            if(response['success'] == 1){
                                var divClass = '.first-response-' + lead_id + '';
                                var $flagSpan = $(divClass).find('span');
                                $flagSpan.removeClass('gray').addClass('green');
                                var secondResponseLinkDivClass = '.second-response-link-' + lead_id + '';
                                var link = '| <a href="#" class="second-response" data-pk=' + lead_id + '>Send follow up response</a>';
                                $(secondResponseLinkDivClass).html(link);
                                send_second_response();

                                var divClass2 = '.emails-sent';
                                $(divClass2).html(response['emails_sent']);

                                var commentClass = '.dash-comment-list-' + lead_id + '';
                                $(commentClass).html(response['prop_comment']);
                            }
                        }
                    });
                    mail_sent = true;
                    $( this ).dialog( "close" );
                },
                Cancel: function() {
                    mail_sent = false;
                    $( this ).dialog( "close" );
                    $("#fetch-send-first-response-form").dialog("open");
                }
           },
        close : function() {
            if (mail_sent) {
                $("#fetch-send-first-response-form").data("availablefrom", "");
                $("#fetch-send-first-response-form").data("availableto", "");
                $("#id_property_name option").prop("selected", false);
            } else {
                mail_sent = true;
            }
        }
    }).css("font-size", "16px");

    $("#add-comment-form").dialog({
        autoOpen : false,
        resizable: false,
        height:"auto",
        width:"auto",
        modal: true,
        buttons: {
            "Add Comment": function(event) {
                var comment = $('#id_fcComment').val();
                var lead_id = $(this).data('pk');
                var data = {
                    'csrfmiddlewaretoken': csrftoken,
                    'comment': comment,
                    'lead_id': lead_id
                };
                $.ajax({
                    type : "POST",
                    url : "/fetch/add-comment/",
                    data : data,
                    beforeSend: function() {
                        $('#loader').show();
                    },
                    complete: function(){
                        $('#loader').hide();
                    },
                    success : function(response) {
                        var divClass = '.dash-comment-list-' + lead_id + '';
                        $(divClass).html(response["content"]);
                        var divClass2 = '.lead-comments-'+ lead_id +'';
                        $(divClass2).html(response["comment_count"]);
                    }
                });
                $( this ).dialog( "close" );
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        },
        close : function() {
            $('#id_fcComment').val("");
        }
    }).css("font-size", "16px");

    $("#compose-email-form").dialog({
        autoOpen : false,
        resizable: false,
        height:'auto',
        width:'auto',
        modal: true,
        buttons: {
            "Send Mail": function(event) {
                var content = $('#id_email_content').val();
                var lead_id = $(this).data('pk');
                var data = {
                    'csrfmiddlewaretoken': csrftoken,
                    'content': content,
                    'lead_id': lead_id
                };
                $.ajax({
                    type : "POST",
                    url : "/fetch/reply-to-email/",
                    data : data,
                    beforeSend: function() {
                        $('#loader').show();
                    },
                    complete: function(){
                        $('#loader').hide();
                        var content = "<p>Reply email has been successfully sent.</p>";
                        $('#emailSuccessId').dialog('option', 'title', 'Reply to Email');
                        $('#emailSuccessId').html(content);
                        $("#emailSuccessId").dialog("open");
                    },
                    success : function(response) {
                        var divClass = '.dash-comment-list-' + lead_id + '';
                        $(divClass).html(response["content"]);
                        var divClass2 = '.lead-comments-'+ lead_id +'';
                        $(divClass2).html(response["comment_count"]);
                    }
                });
                $( this ).dialog( "close" );
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        },
        close : function() {
            $('#id_email_content').val("");
        }
    }).css("font-size", "16px");

    $("#property-dates-form").dialog({
        autoOpen : false,
        resizable: false,
        height: 'auto',
        width: 'auto',
        modal: true,
        buttons: {
            "Save Dates": function(event) {
                var form = $(this).find("#edit-dates-form");
                var data = {
                    'csrfmiddlewaretoken': csrftoken,
                    'date-form': form.serialize()
                };
                $.ajax({
                    type : "POST",
                    url : "/fetch/save-dates/",
                    data : data,
                    beforeSend: function() {
                        $('#loader').show();
                    },
                    complete: function(){
                        $('#loader').hide();
                    },
                    success : function(response) {
                        if(response["success"] == 1) {
                            $("#fetch-send-first-response-form").data("availablefrom", response["available_from"]);
                            $("#fetch-send-first-response-form").data("availableto", response["available_to"]);
                            $("#fetch-send-first-response-form").dialog("open");
                        }
                    }
                });
                $( this ).dialog( "close" );
            },

            Cancel: function() {
                $( this ).dialog( "close" );
                if($("#fetch-send-first-response-form").data("availablefrom") === "") {
                    $("#fetch-send-first-response-form").data("availablefrom", "");
                }
                if($("#fetch-send-first-response-form").data("availableto") === "") {
                    $("#fetch-send-first-response-form").data("availableto", "");
                }
                $("#fetch-send-first-response-form").dialog("open");
            }
        },
        close : function() {
        }
    }).css("font-size", "16px");

    $("#send-concierge-letter").dialog({
        autoOpen : false,
        resizable: false,
        height: "auto",
        width: "auto",
        modal: true,
        buttons: {
            "Yes": function(event) {
                var lead_id = $(this).data('pk');
                var data = {
                    "csrfmiddlewaretoken": csrftoken,
                    "lead_id": lead_id
                };
                $.ajax({
                    type : "POST",
                    url : "/fetch/send-concierge-letter/",
                    data : data,
                    beforeSend: function() {
                        $('#loader').show();
                    },
                    complete: function(){
                        $('#loader').hide();
                    },
                    success : function(response) {
                        if(response["success"] == 1) {
                            var content = "<p>Concierge letter has been successfully sent.</p>";
                            $('#emailSuccessId').dialog('option', 'title', 'Send Concierge Letter');
                            $('#emailSuccessId').html(content);
                            $("#emailSuccessId").dialog("open");
                        }
                    }
                });
                $( this ).dialog( "close" );
            },

            "No": function() {
                $( this ).dialog( "close" );
            }
        },
        close : function() {
        }
    }).css("font-size", "16px");

    $(".email-guest").on('click', function(event) {
        event.preventDefault();
        var pk = $(this).data('pk');
        $("#fetch-send-first-response-form").data("pk", pk);
        $("#fetch-send-first-response-form").dialog("open");
    });
    $(".add-comment").on('click', function(event) {
        event.preventDefault();
        var pk = $(this).data('pk');
        $("#add-comment-form").data("pk", pk);
        $("#add-comment-form").dialog("open");
    });
    $(".reply-to-email").on('click', function(event) {
        event.preventDefault();
        var pk = $(this).data('pk');
        $("#compose-email-form").data("pk", pk);
        $("#compose-email-form").dialog("open");
    });
    $(".get-dialogue").on('click', function(event) {
        event.preventDefault();
        var lead_id = $(this).data('pk');
        data = {
            'csrfmiddlewaretoken': csrftoken,
            'lead_id': lead_id
        };
        $.ajax({
            type : "POST",
            url : "/fetch/get-dialogue/",
            data : data,
            beforeSend: function() {
                $('#loader').show();
            },
            complete: function(){
                $('#loader').hide();
                var content = "<p>Dialogue has been successfully retrieved.</p>";
                $('#emailSuccessId').dialog('option', 'title', 'Get Dialogue');
                $('#emailSuccessId').html(content);
                $("#emailSuccessId").dialog("open");
            },
            success: function(response) {
                var divClass = '.dash-comment-list-' + lead_id + '';
                $(divClass).html(response["content"]);
                var divClass2 = '.lead-comments-'+ lead_id +'';
                $(divClass2).html(response["comment_count"]);
            }
        });
    });
    $(".flag-hot-lead").on('click', function(event) {
        event.preventDefault();
        var pk = $(this).data('pk');
        data = {
            'csrfmiddlewaretoken': csrftoken,
            'lead_id': pk
        };
        $.ajax({
            type : "POST",
            url : "/fetch/flag-hot-lead/",
            data : data,
            beforeSend: function() {
                $('#loader').show();
            },
            complete: function(){
                $('#loader').hide();
            },
            success: function(response) {
                if(response['success'] == 1){
                    var divClass = '.hot-lead-' + pk + '';
                    var $flagSpan = $(divClass).find('span');
                    $flagSpan.removeClass('gray').addClass('red');
                    var content = "<p>Hot Lead has been successfully flagged.</p>";
                    $('#emailSuccessId').dialog('option', 'title', 'Flag Hot Lead');
                    $('#emailSuccessId').html(content);
                    $("#emailSuccessId").dialog("open");
                    $("#emailSuccessId").bind('dialogclose', function(event) {
                        location.reload();
                    });
                }
                else if(response['success'] == 2){
                    var divClass2 = '.hot-lead-' + pk + '';
                    var $flagSpan2 = $(divClass2).find('span');
                    $flagSpan2.removeClass('red').addClass('gray');
                    var content2 = "<p>Hot Lead has been successfully unflagged.</p>";
                    $('#emailSuccessId').dialog('option', 'title', 'Flag Hot Lead');
                    $('#emailSuccessId').html(content2);
                    $("#emailSuccessId").dialog("open");
                    $("#emailSuccessId").bind('dialogclose', function(event) {
                        location.reload();
                    });
                }
            }
        });
    });
    $(".flag-phone-contact").on('click', function(event) {
        event.preventDefault();
        var pk = $(this).data('pk');
        data = {
            'csrfmiddlewaretoken': csrftoken,
            'lead_id': pk
        };
        $.ajax({
            type : "POST",
            url : "/fetch/flag-phone-contact/",
            data : data,
            beforeSend: function() {
                $('#loader').show();
            },
            complete: function(){
                $('#loader').hide();
                var content = "<p>Phone Contact has been successfully flagged.</p>";
                $('#emailSuccessId').dialog('option', 'title', 'Flag Phone Contact');
                $('#emailSuccessId').html(content);
                $("#emailSuccessId").dialog("open");
            },
            success: function(response) {
                if(response['success'] == 1){
                    var divClass = '.phone-contact-' + pk + '';
                    var $flagSpan = $(divClass).find('span');
                    $flagSpan.removeClass('gray').addClass('white');

                    var divClass2 = '.emails-sent';
                    $(divClass2).html(response['emails_sent']);
                }
                else if(response['success'] == 2){
                    var divClass3 = '.phone-contact-' + pk + '';
                    var $flagSpan2 = $(divClass3).find('span');
                    $flagSpan2.removeClass('white').addClass('gray');

                    var divClass4 = '.emails-sent';
                    $(divClass4).html(response['emails_sent']);
                }
            }
        });
    });
    $(".flag-booked").on('click', function(event) {
        event.preventDefault();
        var pk = $(this).data('pk');
        data = {
            'csrfmiddlewaretoken': csrftoken,
            'lead_id': pk
        };
        $.ajax({
            type : "POST",
            url : "/fetch/flag-booked/",
            data : data,
            beforeSend: function() {
                $('#loader').show();
            },
            complete: function(){
                $('#loader').hide();
            },
            success: function(response) {
                if(response['success'] == 1){
                    var divClass = '.booked-' + pk + '';
                    var $flagSpan = $(divClass).find('span');
                    $flagSpan.removeClass('gray-booked').addClass('booked');

                    var divClass2 = '.bookings-from-leads';
                    $(divClass2).html(response['bookings_from_leads']);
                    var inputClass = '.goal';
                    $(inputClass).val(response['bookings_goal']);
                    var divClass3 = '.calls-received';
                    $(divClass3).html(response['calls_received']);

                    $("#send-concierge-letter").data("pk", pk);
                    $("#send-concierge-letter").dialog("open");

                    var commentClass = '.dash-comment-list-' + pk + '';
                    $(commentClass).html(response['comment_list']);
                }
            }
        });
    });

    $("#fetch-search-for-leads-box-submit").on('click', function(event) {
        var data = {
            'csrfmiddlewaretoken': csrftoken,
            'search_query': $("#search").val()
        };
        $.ajax({
            type : "POST",
            url : "/fetch/search/",
            data : data,
            beforeSend: function() {
                $('#loader').show();
            },
            complete: function(){
                $('#loader').hide();
            },
            success: function(response) {
                var divClass = '#search-results-id';
                $(divClass).html(response);
                item_details();
            }
        });
    });
    $(".lead-status-link").on('click', function(event) {
        event.preventDefault();
        var status = $(this).data('status');
        data = {
            'csrfmiddlewaretoken': csrftoken,
            'status': status
        };
        $.ajax({
            type : "POST",
            url : "/fetch/get-leads-with-status/",
            data : data,
            beforeSend: function() {
                $('#loader').show();
            },
            complete: function(){
                $('#loader').hide();
            },
            success: function(response) {
                var divClass = '#search-results-id';
                $(divClass).html(response);
                /*----------- Retiver comment functionalities ------------*/
                $('.item-details').hide();
                $('.guest-name').click(function(){
                    var $itemDetails = $(this).parent().parent().parent().find('div.item-details');
                    if ($itemDetails.css('display') == 'none') {
                        $(this).css( 'color', '#f9a44a');
                        $('.edit').hide();
                        $itemDetails.show();
                    }
                    else {
                        $(this).css( 'color', '#66cb29');
                        $('.edit').hide();
                        $itemDetails.hide();
                    }

                    var lead_id = $(this).data("pk");
                    var data = {
                        "csrfmiddlewaretoken": csrftoken,
                        "lead_id": lead_id
                    };
                    $.ajax({
                        type : "POST",
                        url : "/fetch/mark-comments-as-read/",
                        data : data,
                        beforeSend: function() {
                            $('#loader').show();
                        },
                        complete: function(){
                            $('#loader').hide();
                        },
                        success: function(response) {
                        }
                    });
                    return false;
                });
                $('.item1 .add-comment').click(function(){
                    $('.item1 .guest-name').css( 'color', '#f9a44a');
                    $('.edit').hide();
                    $('.item1 .item-details:first').show();
                    return false;
                });
            }
        });
    });
    $("#comment-alert-link-id").on('click', function(event) {
        event.preventDefault();
        var data = {
            'csrfmiddlewaretoken': csrftoken
        };
        $.ajax({
            type : "POST",
            url : "/fetch/alerts/",
            data : data,
            beforeSend: function() {
                $('#loader').show();
            },
            complete: function(){
                $('#loader').hide();
            },
            success: function(response) {
                var divClass = '#search-results-id';
                $(divClass).html(response);
                /*----------- Retiver comment functionalities ------------*/
                $('.item-details').hide();
                $('.guest-name').click(function(){
                    var $itemDetails = $(this).parent().parent().parent().find('div.item-details');
                    if ($itemDetails.css('display') == 'none') {
                        $(this).css( 'color', '#f9a44a');
                        $('.edit').hide();
                        $itemDetails.show();
                    }
                    else {
                        $(this).css( 'color', '#66cb29');
                        $('.edit').hide();
                        $itemDetails.hide();
                    }
                    var lead_id = $(this).data("pk");
                    var data = {
                        "csrfmiddlewaretoken": csrftoken,
                        "lead_id": lead_id
                    };
                    $.ajax({
                        type : "POST",
                        url : "/fetch/mark-comments-as-read/",
                        data : data,
                        beforeSend: function() {
                            $('#loader').show();
                        },
                        complete: function(){
                            $('#loader').hide();
                        },
                        success: function(response) {
                        }
                    });
                    return false;
                });
                $('.item1 .add-comment').click(function(){
                    $('.item1 .guest-name').css( 'color', '#f9a44a');
                    $('.edit').hide();
                    $('.item1 .item-details:first').show();
                    return false;
                });
                /*----------- Retiver Edit functionalities ------------*/
                $('.edit').hide();
                $('.edit-info').click(function(event){
                    $('.item1 .guest-name').css( 'color', '#f9a44a');
                    $('.item-details').hide();
                    $('.edit:first').show();
                    return false;
                });
            }
        });
    });
    $(function() {
        $(".fetch-booking-toolbar").button({
            icons: {
                primary: "ui-icon-plusthick"
            }
        }).click(function(event) {
            event.preventDefault();
        });
    });
    $(function() {
        var availableTags = [];
        $('.guest-name').each(function(){
            if(!(jQuery.inArray($(this).text(), availableTags) > 0)) {
                availableTags.push($(this).text());
            }

        });
        $("#search").autocomplete({
            source: availableTags
            });
        });
    });
