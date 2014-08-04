// JavaScript Document

$(document).ready(function ()
                  {

$("#sidebar").height($("#content").height());




$(".navigation li.dropdown > a").click(function(){

$(".navigation li.dropdown a").parent("li").find("ul").slideUp(650);
	$(".navigation li.dropdown a").removeClass("expand");	
	
$(this).parent("li").find("ul").slideDown(650);
$(this).addClass("expand");



});



var $overlay = $('<div class="overlay"/>');
$('body').append($overlay);
$('.navigation li.po span.popin').click(function(){
	
	var data = $(this).parent("li").find('.popup').wrap('<p/>').parent().html();

	$(".overlay").html(data);

	$(".overlay").fadeIn(800).addClass('visible');
	$(".overlay .popup").show();

	});
	



  $(".popup_wrap").on("click", function(e){
  e.stopPropagation();
});
	$('.popup').click(function() {
	$(".overlay .popup").hide();
	$(".overlay").removeClass('visible');
	console.log(this);
		
});


	
	
				  });


function close_popup(){
		
	$(".overlay .popup").hide();
	$(".overlay").removeClass('visible');
	$(".overlay").empty();
	};

		
	