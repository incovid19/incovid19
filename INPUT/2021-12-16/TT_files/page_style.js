/* ********* Page Style Toggele Code Starts ********* */

			var themecookie = jQuery.cookie('mycookie');

			switch (themecookie) {
			case 'color-white-to-black':
				jQuery("body").removeClass('color-standard').addClass(
						"color-white-to-black");
				break;
			default:
				jQuery("body").removeClass('color-white-to-black').addClass(
						"color-standard");
				break;
			}

			jQuery(".cp_white_to_black a").click(
					function() {
						jQuery("body").removeClass('color-standard').addClass(
								"color-white-to-black");
						jQuery.cookie('mycookie', 'color-white-to-black');
						return false;
					});

			jQuery(".cp_standard a").click(
					function() {
						jQuery("body").removeClass('color-white-to-black')
								.addClass("color-standard");
						jQuery.cookie('mycookie', 'color-standard');
						return false;
					});

			if (typeof themecookie != 'undefined' && themecookie != null) {
				switch (themecookie) {
				case 'color-white-to-black':
					jQuery('#pagestyle').css("marginLeft", '0px');
					break;
				default:
					jQuery('#pagestyle').css("marginLeft", '25px');
				}
			}

			jQuery('#pagestyle a').click(function() {
				if (jQuery("#pagestyle").css("marginLeft") == '25px') {
					jQuery('#pagestyle').stop().animate({
						marginLeft : '0px'
					}, 100);
				} else {
					jQuery('#pagestyle').stop().animate({
						marginLeft : '25px'
					}, 100);
				}
			});

			/* ********* Page Style Toggele Code Ends ********* */