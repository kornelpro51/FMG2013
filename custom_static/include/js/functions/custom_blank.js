$(document).ready(function() {

	

	//===== Append right sidebar to the left. REMOVE THIS CODE if you're using 2 columns layout. =====//

	$(window).resize(function () {
	  var width = $(this).width();
		if (width < 1367) {
			$('.three-columns .appendable').appendTo('#left-sidebar');
			$('.three-columns .content').css('marginRight', '0');
		}
		else { 
			$('.three-columns .appendable').appendTo('#right-sidebar');
			$('.three-columns .content').css('marginRight', '250px')
		 }
	}).resize();



	//===== Top nav and responsive functions =====//

	$('.topnav > li.search > a').click(function () {
		$('.top-search').fadeToggle(50);
	});

	$('.sidebar-button > a').toggle(function () {
		$('.sidebar').addClass('show-sidebar').removeClass('hide-sidebar');
	},
	function () {
		$('.sidebar').removeClass('show-sidebar').addClass('hide-sidebar');
	}
	);



	//===== Collapsible plugin for main nav =====//
	
	$('.expand').collapsible({
		defaultOpen: 'current',
		cookieName: 'navAct',
		cssOpen: 'subOpened',
		cssClose: 'subClosed',
		speed: 200
	});

	$('.opened').collapsible({
		defaultOpen: 'opened,toggleOpened',
		cssOpen: 'inactive',
		cssClose: 'normal',
		speed: 200
	});

	
			
});