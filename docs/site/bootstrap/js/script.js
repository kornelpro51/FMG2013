
     $(function($) {
$('ul.nav li a').click(function (e) {
    e.preventDefault();
	
    if($(this).attr('href') !== '#'){
	
		$(this).parent("li").addClass("active");
        var location = $($(this).attr('href')).offset().top - 95; /* For your header height, subtract 150 or whatever it ends up being */
        $('html, body').animate({scrollTop: location}, 300);
    } else {
        $('html, body').animate({scrollTop: 0}, 300);
    }
});

	 var content1 = $("#content").height() +28; /*header height*/
	 var content2 = $("#content2").height() + content1 +26; /* 50 is padding for container */
	 var content3 = $("#content3").height() + content2 +26;
	 var content4 = $("#content4").height() + content3 +26;
	 var content5 = $("#content5").height() + content4 ;
	

 $(window).scroll(function () {
	
	
        if ($(this).scrollTop() <= content1  ) {
			 $("ul.nav li").removeClass();
		$('ul.nav li a[href=#content]').parent("li").addClass("active");
		}
		else if($(this).scrollTop() <= content2 ) {
			 $("ul.nav li").removeClass();
		$('ul.nav li a[href=#content2]').parent("li").addClass("active");
			}
			else if($(this).scrollTop() <= content3) {
			 $("ul.nav li").removeClass();
		$('ul.nav li a[href=#content3]').parent("li").addClass("active");
			}
			else if($(this).scrollTop() <= content4) {
			 $("ul.nav li").removeClass();
		$('ul.nav li a[href=#content4]').parent("li").addClass("active");
			}
			else  {
			 $("ul.nav li").removeClass();
		$('ul.nav li a[href=#content5]').parent("li").addClass("active");
			}
		
		});
	 });
	 