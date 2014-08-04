/*
* Author: SIMON GOMES <busy.s.simon@gmail.com>
* Description : jQuery functions including menu functions.
* Date: August 6, 2012 
*/

$(document).ready(function(){

	/*------------------- Menu Functions -----------------*/
	$('.sub-menu').hide();
	$('.sub-menu ul').hide();

	$('.dropdown.report').hover(function(){
		$('.report .sub-menu').show(100);
	},
	function(){
		$('.report .sub-menu').hide(100);
	}
	);

	$('.dropdown.agent').hover(function(){
		$('.agent .sub-menu').show(100);
	},
	function(){
		$('.agent .sub-menu').hide(100);
	}
	);

	$('.dropdown.alert').hover(function(){
		$('.alert .sub-menu').show(100);
	},
	function(){
		$('.alert .sub-menu').hide(100);
	}
	);


	$('.leads').hover(function(){
		$('.leads-sub').show(100);
	},
	function(){
		$('.leads-sub').hide(100);
	}
	);

	$('.bookings').hover(function(){
		$('.bookings-sub').show(100);
	},
	function(){
		$('.bookings-sub').hide(100);
	}
	);

	$('.settings').hover(function(){
		$('.settings-sub').show(100);
	});
	// function(){
	// 	$('.settings-sub').hide(100);
	// 	$('.account .sub-menu').show(100);
	// }
	// );
	//------------- Log out menu button-----------------
	$('.dropdown.account').hover(function(){
		$('.account .sub-menu').show(100);
	},
	function(){
		$('.account .sub-menu').hide(100);
	}
	);

	//Disabling the Reports link
	$('.reports').click(function(){
		return false;
	});
	/*------------------- END Menu Functions -----------------*/  

	/*------ Manager dashboard button function --------*/

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
	    // Do something on mouseout
	    $('#bingoboard-tooltip').hide();
	});

});

// Email Validation Function
function valid_email(email){
	var pattern= new RegExp(/^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]+$/);
	return pattern.test(email);
}
