/*
Created the module to consume it on the index.html page
Which is calling the myApp.Service
*/
//var apiURL = "apidata.json";
var apiURL = "/api/leads/?format=json";

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
    // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
   });
   $.ajaxSetup({ cache: false });
var myapp = angular.module('myApp', ['myApp.service', 'myApp.service1']).directive('onFinishRender', function ($timeout) {
    return {
        restrict: 'A',
        link: function (scope, element, attr) {
            if (scope.$last === true) {
                scope.$evalAsync(attr.onFinishRender);
            }
        }
    }
});

//Added the django-rest-resource module as a dependency to call the API
angular.module('myApp.service', ['djangoRESTResources']).
    factory('States', function (djResource) {
        //Here djResource calling the API using Get method and return the data
        return djResource(apiURL, {}, {
            get: { method: 'GET', isArray: true }
        });


    });
angular.module('myApp.service1', ['djangoRESTResources']).
    factory('Messages', function (djResource) {
        //Here djResource calling the API using Get method and return the data
        return djResource('msgdata.json', { lead_id: '@lead_id' }, {
            get: { method: 'GET', isArray: true }
        });
    });

//here is the controller
    var StatesController = function ($scope, States, Messages) {
        //storing the data in the scope to display it on the html page
        //Get data from 'States' factory into statedata json array 
       $scope.proplst=[];
        $scope.stateData = States.get();
       
        $scope.testdiv = function () {

            $("#loader").hide();
        }
        //Function to call the message API on click of lead rows
        $scope.abcd = function (id) {
            $.ajax({
                url: '/api/messages/?format=json',
                dataType: 'json',
                method: 'GET',
                data: { lead_id: id },
                contentType: 'application/json',
                success: function (innerdata) {
                    //On successful calling the data will be bind dynamically to the main grid
                    //this will generate nested grid and append the grid after the row which has been clicked
                    var htmltagcontent = "";
                    $.each(innerdata.results, function (idcnt, rowdata) {
                        htmltagcontent += "<tr><td class='tenth'>" + rowdata.subject + "</td><td class='first'>" + rowdata.processed + "</td><td class='second'>" + rowdata.mailbox + "</td></tr>"
                    });
                    $("#tbody" + id).html(htmltagcontent);
                    $scope.showhidetr('tr' + id);
                },
                error: function (err, sts, msg) {
                    alert(sts);
                }
            });
        }
        $scope.showhidetr = function (trid) {
            if ($("#" + trid).is(":visible")) {
                $("#" + trid).hide();
            }
            else {
                $("#" + trid).show();
            }
        }
        //To show Message
        $scope.showmsg = function (id,adults,children) {
            $.ajax({
                    url: '/leads/customers/'+ id +'/?format=json',
                    dataType: 'json',
                    method: 'GET',
                    contentType: 'application/json',
                    success: function (innerdata) {
                        //On successful calling the data will be bind dynamically to the main grid
                        //this will generate nested grid and append the grid after the row which has been clicked
                        $('#trmsg'+id).find('#hrefemail').html(innerdata.email);
                        $('#trmsg'+id).find('#spnphone').html('Phone : '+ innerdata.phone);
                        $scope.showhidetr('trmsg' + id);
                    },
                    error: function (err, sts, msg) {
                        //alert(sts);
                    }
                });
           
        }

        //To show add guest form
        $scope.showaddguest=function(){
         $( "#dialog-addguest" ).dialog({
            title:"Add Guest",
            height: 550,
            width:500,
            modal: true,
            buttons: {
            "Save":function(){
                            

                }
            }
            });
            $("#dialog-addguest").dialog("open");
        }
        var count=0;
        $scope.showalert=function(){
        
            $.ajax({
                    url: '/api/notifications/?format=json',
                    dataType: 'json',
                    method: 'GET',
                    contentType: 'application/json',
                    success: function (innerdata) {
                        //On successful calling the data will be bind dynamically to the main grid
                        //this will generate nested grid and append the grid after the row which has been clicked
                        var htmltagcontent = "";
                        if(innerdata.count>count){
                            count=innerdata.count;
                        }
                        $.each(innerdata.results, function (idcnt, rowdata) {
                            //htmltagcontent += "<tr><td class='tenth'>" + rowdata.subject + "</td><td class='first'>" + rowdata.processed + "</td><td class='second'>" + rowdata.mailbox + "</td></tr>"
                            count=count+1;
                        });
//                        if($("#comment-alert-id").html()<count){
//                            alert("New Alert");
//                            $("#comment-alert-id").html(count);
//                        }else
//                        {
                        //alert("Timer is working");
                        //}
                        
                        //alert(count);
                    },
                    error: function (err, sts, msg) {
                        //alert(sts);
                    }
                });
        }
        $scope.justpost = function (id) {

            if (window.event) { window.event.returnValue = false; }
            else if (event.preventDefault) { event.preventDefault(); }
            else { event.returnValue = false; alert(id); }

            return false;
        }

        $scope.GetStatusClass = function (istruedata, trueclass, falseclass) {
            if (istruedata) {
                return trueclass;
            }
            else {
                return falseclass;
            }
        }
       
       //function to call the first response trigger on click of "set prop info"       
       $scope.actionPopup=function(id,arr,dep,cust,src,replyid){
        var templateUrl='/api/first_response/'+id+'/';
        if($("#lblsts").hasClass("alert-error")){
            $("#lblsts").removeClass("alert-error");
        }
        if($("#lblsts").hasClass("alert-success")){
            $("#lblsts").removeClass("alert-success");
        }
        $.ajax({
                url: '/api/properties/?format=json',
                dataType: 'json',
                method: 'GET',
                cache:false,
                contentType: 'application/json',
                success: function (data) {
                    $scope.proplst = data.results;
                    var htmltagcontent = "";
                    $.each(data.results,function(idcnt, rowdata){

                    htmltagcontent += "<option value="+rowdata.id+">"+rowdata.title+"</option>";
                    });
                    $("#id_property_name").html(htmltagcontent);
                    //to open dialog box
                    $("#dialog-form").dialog({
			        autoOpen: false,
			        height: 400,
			        width: 450,
			        modal: true,
			        buttons: {
                    "See Template Preview": function() {
                            var rate;
                            var property;
                            var status;
                            var available_from;
                            var available_to;

                            if($("#txtPropRate").val()!=0.00){
                            rate=$("#txtPropRate").val();
                            }
                            property="http://djangoangularui.demos.classicinformatics.com:8000/leads/properties/"+$("#id_property_name").val()+"/";
                            available_from=$("#datepickerArr").val();
                            available_to= $("#datepickerDep").val();
                            if ($('#propsts').is(':checked')) {
                            status="RQ";
                            } else {
                            status="NA";
                            } 

                            datatopass = { 'status': status, 'property': property, 'rate': rate, 'available_from':available_from,'available_to':available_to };
                            //Code to add/update the property under lead
                            // Ajax function to call the API's post method
                                $.ajax({
                                    url: '/api/leads/' + id + '/properties/',
                                    method: 'POST',
                                    data: JSON.stringify(datatopass),
                                    dataType: 'json',
                                    contentType: 'application/json',
                                    success: function (msg) {
                                        
                                        datatopass = { 'first_response': true, 'customer': cust, 'source': src };
                                        $scope.fetchTemplateResponse(templateUrl,replyid,id,datatopass,'first_response','green','gray');
                                       
                                    },
                                    error: function (err, sts, msg) {
                                        
                                        $("#lblsts").text(err.responseText);
                                        if($("#lblsts").hasClass("alert-success")){
                                            $("#lblsts").removeClass("alert-success");
                                        }
                                        $("#lblsts").addClass("alert-error");
                                        $( "#dialog-editor" ).dialog( "close" );
                                    }
                     });

            },
                    
            Cancel: function() {
	            $( this ).dialog( "close" );
            }
            },
            close: function() {
                $( this ).dialog( "close" );
            //allFields.val( "" ).removeClass( "ui-state-error" );
            }
		    });
            $("#dialog-form").dialog("open");
            $("#datepickerArr").val(arr);
            $("#datepickerDep").val(dep);
        },
        error: function (err, sts, msg) {
        alert(sts);
        }
    });
 }

       
       
       //function to fetch template
        $scope.fetchTemplateResponse=function(tempurl,replyid,id,datatopass,objid,classadd, classremove){
        $.ajax({
                url: tempurl,
                dataType: 'json',
                method: 'GET',
                data: { },
                contentType: 'application/json',
                success: function (msg) {
                    
                    if (objid == 'first_response') {
                     $("#textarea1").val(msg.first_response);
                      tinymce.init({
                        selector: "textarea",
                        plugins: [
                        "advlist autolink lists link image charmap print preview anchor",
                        "searchreplace visualblocks code fullscreen",
                        "insertdatetime media table contextmenu paste "
                        ],
                        toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image"
                        });
                        //to open dialog box
                        $( "#dialog-editor" ).dialog({
                        title:"Email Preview",
                        height: 450,
                        width:750,
                        modal: true,
                        buttons: {
                        "Send Email":function(){
                            
                                var message =$('#textarea1').val();
                                var dataToPass={'message':message};
                                $scope.postEmailMessage(message,replyid, id, datatopass,'first_response','green', 'gray');
                                //After successfully submitted the status has been reflect back to grid by change its style Class
                                    $("#lblsts").text("Successfully Saved");
                                    if($("#lblsts").hasClass("alert-error")){
                                    $("#lblsts").removeClass("alert-error");
                                }
                                $("#lblsts").addClass("alert-success");
                                $( "#dialog-editor" ).dialog( "close" );
                                }
                            }
                        });
                        $("#dialog-editor").dialog("open");
                    }
                    
                    if (objid == 'second_response') {
                    $scope.postEmailMessage(msg.second_response,replyid,id,datatopass,objid,classadd, classremove);
                    }
                    if (objid == 'booked') {
                    $scope.postEmailMessage(msg.concierge_response,replyid,id,datatopass,objid,classadd, classremove);
                    }
                    if (objid == 'offer') {
                    $scope.postEmailMessage(msg.offer_response,replyid,id,datatopass,objid,classadd, classremove);
                    }

                },
                error: function (err, sts, msg) {
                
                    alert(sts);
                }
            });
        }
        //To post email message
       $scope.postEmailMessage=function(message,replyid,id,datatopass,objid,classadd, classremove){
        var dataToPass={'message':message };
        $.ajax({
                url: '/api/reply/' + replyid + '/',
                dataType: 'json',
                method: 'POST',
                data: JSON.stringify(dataToPass),
                contentType: 'application/json',
                success: function (msg) {
                
                   // return msg;
                     if(msg){
                        $scope.stsdialogPopup(id,datatopass,objid,classadd, classremove);
                    }
                },
                error: function (err, sts, msg) {
                
                    alert(sts);
                }
            });
        }

        //Function used to trigger the POST method to change the staus of the Offer and booking status
        $scope.bookSts = function (id, booked, classadd, classremove, objid, customer, source,replyid) {
            var datatopass = {};
            var templateUrl="/api/"+objid+"/"+ id;
            var sts;
            var submsg = "";
            //code for booking status
            if (objid == 'booked') {
                templateUrl= "/api/concierge_response/"+ id + "/";
                sts = "Confirm Booking";
                submsg="Sending off concierge letter";
                 $("#dialog-message").dialog({
                    title: sts,
                    modal: true,
                    open: function () {
                        if (sts != "") {
                            $(this).find('p:eq(0)').html(submsg);
                        }
                        $(this).find('p:eq(1)').html('Click ok to proceed.');
                    },
                    buttons: {
                        Ok: function () {
                            $(this).dialog("close");
                            
                            datatopass = { 'booked': !booked, 'customer': customer, 'source': source };
                            $scope.fetchTemplateResponse(templateUrl,replyid,id,datatopass,objid,classadd, classremove);
                        },
                         Cancel: function() {
	                        $( this ).dialog( "close" );
                        }

                    }

                });
            }
            //code for offers 
            else if (objid == 'offer') {
            templateUrl= "/api/offer_response/"+ id + "/";
                sts = "Send special offer";
                submsg="Do you have manager approval?";
                 $("#dialog-message").dialog({
                    title: sts,
                    modal: true,
                    open: function () {
                        if (sts != "") {
                            $(this).find('p:eq(0)').html(submsg);
                        }
                        $(this).find('p:eq(1)').html('Click ok to proceed.');
                    },
                    buttons: {
                        Ok: function () {
                            $(this).dialog("close");
                            
                            datatopass = { 'offer': !booked, 'customer': customer, 'source': source };
                            $scope.fetchTemplateResponse(templateUrl,replyid,id,datatopass,objid,classadd, classremove);
                        },
                         Cancel: function() {
	                        $( this ).dialog( "close" );
                        }

                    }

                });
            }
            else if (objid == 'first_response') {
                sts = "";
            }
            else if (objid == 'second_response') {
                var  respObj="";
                sts = "Send follow up marketing letter";
                //submsg="It will send an follow up email to the customer";
                $("#dialog-message").dialog({
                    title: sts,
                    modal: true,
                    open: function () {
                        if (sts != "") {
                            $(this).find('p:eq(0)').html(submsg);
                        }
                        $(this).find('p:eq(1)').html('Click ok to proceed.');
                    },
                    buttons: {
                        Ok: function () {
                            $(this).dialog("close");
                            datatopass = { 'second_response': !booked, 'customer': customer, 'source': source };
                            $scope.fetchTemplateResponse(templateUrl,replyid,id,datatopass,objid,classadd, classremove);
                        },
                         Cancel: function() {
	                        $( this ).dialog( "close" );
                        }

                    }

                });
            }
            else if (objid == 'hot') {
                sts = "Guest is now a 'Hot Lead'";
                //submsg="It will generate a hot lead against the property";
                $("#dialog-message").dialog({
                    title: sts,
                    modal: true,
                    open: function () {
                        if (sts != "") {
                            $(this).find('p:eq(0)').html(submsg);
                        }
                        $(this).find('p:eq(1)').html('Click ok to proceed.');
                    },
                    buttons: {
                        Ok: function () {
                            $(this).dialog("close");
                            
                            datatopass = { 'hot': !booked, 'customer': customer, 'source': source };
                            $scope.stsdialogPopup(id,datatopass,objid,classadd, classremove);
                        },
                         Cancel: function() {
	                        $( this ).dialog( "close" );
                        }

                    }

                });

            }
            else if (objid == 'phone_call') {
                sts = "Guest Contacted";
                //submsg="It will  set phone_call against the property for customer";
                $("#dialog-message").dialog({
                    title: sts,
                    modal: true,
                    open: function () {
                        if (sts != "") {
                            $(this).find('p:eq(0)').html(submsg);
                        }
                        $(this).find('p:eq(1)').html('Click ok to proceed.');
                    },
                    buttons: {
                        Ok: function () {
                            $(this).dialog("close");
                            
                            datatopass = { 'phone_call': !booked, 'customer': customer, 'source': source };
                            $scope.stsdialogPopup(id,datatopass,objid,classadd, classremove);
                        },
                         Cancel: function() {
	                        $( this ).dialog( "close" );
                        }

                    }

                });
            }
        }
        
        $scope.stsdialogPopup=function(id,datatopass,objid,classadd, classremove){
              $.ajax({
                    url: '/api/leads/' + id + '/',
                    method: 'PUT',
                    data: JSON.stringify(datatopass),
                    dataType: 'json',
                    contentType: 'application/json',
                    success: function (msg) {
                        //After successfully submitted the status has been reflect back to grid by change its style Class
                        $("#" + objid + id).find("span").each(function () {
                        
                            if ($(this).hasClass(classremove)) {
                                $(this).removeClass(classremove);
                                $(this).addClass(classadd);
                            }
                            else {
                                $(this).removeClass(classadd);
                                $(this).addClass(classremove);
                            }
                        });

                    },
                    error: function (err, sts, msg) {
                        alert(err.responseText);
                    }
                });
         }
    };       