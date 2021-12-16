
/*
 1. Tabs
 2. flexslider
 */
// Verhoeff algorithm validator
String.prototype.verhoeffCheck = (function () {
	var d = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
	[1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
	[3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
	[5, 9, 8, 7, 6, 0, 4, 3, 2, 1], [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
	[7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
	[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]];
	var p = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
	[1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
	[8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
	[4, 2, 8, 6, 5, 7, 3, 9, 0, 1], [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
	[7, 0, 4, 6, 9, 1, 3, 2, 5, 8]];
	var j = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9];

	return function () {
		var c = 0;
		this.replace(/\D+/g, "").split("").reverse().join("").replace(/[\d]/g,
			function (u, i, o) {
				c = d[c][p[i & 7][parseInt(u, 10)]];
			});
		return (c === 0);
	};
})();


jQuery(document).ready(function () {
	
	// gigw keyboard show detail
	jQuery(".comment_toggle_wrapper a").on('keyup', function(e) { 
		var keyCode = e.keyCode || e.which; 

		if (keyCode == 9) { 
		  jQuery(this).trigger('click');
		} 
	  });


  // gigw keyboard show detail
	jQuery("#see_details .expand").on('keyup', function(e) { 
		var keyCode = e.keyCode || e.which; 

		if (keyCode == 9) { 
		  jQuery(this).trigger('click');
		} 
	  });
	//keyboard group change						
	  jQuery("#group_switch_btn").on('keyup', function(e) { 
		var keyCode = e.keyCode || e.which; 

		if (keyCode == 9) { 
		  jQuery(this).trigger('click');
		} 
	  });

	  //gigw keyboard Close group list//
	  jQuery('#groups_list li:last-child').keydown(function(e) {
		var code = e.keyCode || e.which;
	
		if (code === 9) {  
			jQuery("#group_switch_btn").trigger('click');
		}
	   });

	 // gigw keyboard show meghamnu and accessibility btn//
	 jQuery(".res_menu").on('keyup', function(e) { 
		var keyCode = e.keyCode || e.which; 

		if (keyCode == 9) { 
		  jQuery( ".flyout-menu-wrapper" ).show().focus();
		} 
	  });
  //gigw keyboard Close Megamenu//
   jQuery('.mygov-apps-inner li:last-child').keydown(function(e) {
	var code = e.keyCode || e.which;

	if (code === 9) {  
		jQuery('.flyout-menu-wrapper').hide();
	}
   });
   jQuery('.c-accordian h3').on('keydown', function(e) { 
	var keyCode = e.keyCode || e.which; 

	if (keyCode == 9) { 
		jQuery(this).trigger('click');
		
	} 
  });
//   jQuery('.ac_title2 a.plus_icon,.ac_title1 a.plus_icon').on('keydown', function(e) { 
// 	var keyCode = e.keyCode || e.which; 

// 	if (keyCode == 9) { 
// 		jQuery(this).trigger('click');
		
// 	} 
//   }); 
   
	  jQuery(".user_accessibility").on('keydown', '.access_icon', function(e) { 
		var keyCode1 = e.keyCode || e.which; 

		if (keyCode1 == 9) { 
		  jQuery( ".access-type" ).show().focus();
		} 
	  });
	  
	  //hide accessibility btn on keyboard focusout//
   jQuery('.cp_standard a').keydown(function(e) {
	var code1 = e.keyCode || e.which;

	if (code1 === 9) {  
		jQuery('.access-type').hide();
	}
   });

	 
//Show  Notificationlist on keyboard focus//
   jQuery(".header-push-notification").on('keydown', '> a', function(e) { 
		var keyCode1 = e.keyCode || e.which; 

		if (keyCode1 == 9) { 
		  jQuery('.header-push-notification').addClass('show');
		  jQuery(".notification-container").show().focus();
		} 
	  });
	  
 //hide  Notificationlist on keyboard focusout//
   jQuery('.push_notification_list li:last-child a').keydown(function(e) {
	var code2 = e.keyCode || e.which;

	if (code2 === 9) {  
		 jQuery('.header-push-notification').removeClass('show');
		  jQuery(".notification-container").hide();
	}
   });


   //hide  Search on keyboard focusout//
   jQuery('#search_link_btn').keydown(function(e) {
	var code2 = e.keyCode || e.which;

	if (code2 === 9) {  
		jQuery( ".search_mygov_box" ).removeClass('active_search')
	}
   });
   
    jQuery(".search_mygov_box").on('keyup', '.search_toggle', function(e) { 
		var keyCode = e.keyCode || e.which; 

		if (keyCode == 9) { 
		  jQuery( ".search_mygov_box" ).addClass('active_search').focus();
		} 
	  });
	  
	//show latest Notification at covid page by keyboard
	  jQuery(".notification-btn").on('keydown', function(e) { 
		var keyCode = e.keyCode || e.which; 

		if (keyCode == 9) { 
		  jQuery('.ln-block').show().focus();
		} 
	  });
	  
	  //Hide latest Notification at covid page by keyboard
   jQuery('.ln-block > a').keydown(function(e) {
	var code = e.keyCode || e.which;

	if (code === 9) {  
		 jQuery('.ln-block').hide();
	}
   });
   
   //show social share at covid page by keyboard
	  jQuery(".share_corona_page .share-icon").on('keydown', function(e) { 
		var keyCode = e.keyCode || e.which; 

		if (keyCode == 9) { 
		  jQuery('.share_corona_page .mshare-list').show().focus();
		} 
	  });
	  
 //Hide social share at covid page by keyboard
   jQuery('.mshare-list .fb-icon').keydown(function(e) {
	var code = e.keyCode || e.which;

	if (code === 9) {  
		 jQuery('.share_corona_page .mshare-list').hide();
	}
   });
   //show Sticky Menu at covid page by keyboard
	  jQuery(".sticky-menu-btn").on('keydown', function(e) { 
		var keyCode = e.keyCode || e.which; 

		if (keyCode == 9) { 
		  jQuery('.covid-menus').addClass('extend').focus();
		} 
	  });
	  
  //Hide Sticky Menu at covid page by keyboard
   jQuery('.covid-menus li:last-child a').keydown(function(e) {
	var code = e.keyCode || e.which;

	if (code === 9) {  
		 jQuery('.covid-menus').removeClass('extend');
	}
   });
//show Activities in this group by keyboard
jQuery(".group_stats > a").on('keydown', function(e) { 
	var keyCode = e.keyCode || e.which; 

	if (keyCode == 9) { 
		jQuery(this).parents('.group_stats').find('.group_info_wrap').show().focus();
		jQuery(this).parents('.group_stats').addClass('show');
	} 
  });
  //Hide Activities in this group by keyboard
  jQuery('.group_info_wrap .view-status:last-child a').keydown(function(e) {
	var code = e.keyCode || e.which;

	if (code === 9) {  
		jQuery(this).parents('.group_stats').find('.group_info_wrap').hide();
		jQuery(this).parents('.group_stats').removeClass('show');
	}
   });
//    jQuery('.group_stats > a').off("click").on('click', function (event) {
// 	event.preventDefault();
// 	jQuery(this).parents('.group_stats').find('.group_info_wrap').slideToggle();
// 	jQuery(this).parents('.group_stats').toggleClass('show');
// })
   

   // close Accessibility btns outside click
	jQuery(document).mouseup(function (e) {
		var access_box = jQuery('.user_accessibility');
		if (!access_box.is(e.target) && access_box.has(e.target).length === 0) {
			jQuery('.access-type').fadeOut();
		}
	});

	
	jQuery(".share_btn").on('keyup', function(e) { 
		var keyCode = e.keyCode || e.which; 

		if (keyCode == 9) { 
			jQuery(this).next(".share_links").show();
		} 
	  }); 


 // Toogle Accessibility Btns
	jQuery('.access_icon').click(function(){
		jQuery('.access-type').slideToggle();
	})
		
	if (jQuery('.update_block').length > 0) {
		jQuery('#content').removeClass('container').addClass('covid');
		jQuery('#page-title').wrap('<div class="container" />')
	}
	
	if (jQuery('.comment-top .comment_toggle_wrapper').length < 1) {
		jQuery('.comment-top').hide();
	}
	jQuery('#sector_select').selectric({
		inheritOriginalWidth: true
	});
	jQuery('.sort_by_link_wrapper').selectric();
//campaign page main tab  and inner common tabbing

jQuery('.info-tab a').not(".outerlink").click(function(e){
	e.preventDefault();
	jQuery('.ctab').hide();
	jQuery('.info-tab a').removeClass('active');
	jQuery(this).addClass('active');
	var targetBtn = jQuery(this).attr('href');
	jQuery('.info_block').hide()
	jQuery(targetBtn).show();
})
jQuery( ".info-tab li:nth-child(2) a" ).click(function(e){

	if(!jQuery("#info-2 div").hasClass("state-covid-advisory")){
		
		state_advisory();
		/*
		var curUrl = window.location.href;
		var curUrlArray = curUrl.split("/");
		if(curUrlArray[3] == 'hi'){
			var gatData = "/hi/vaccine-state-advisory";
		}else{
			var gatData = "/vaccine-state-advisory";
		}
    jQuery("#info-2 img.loader").show();
		jQuery.ajax({
        type: 'GET',
        url: gatData,
        dataType: 'text',
        success: function(response) { 
           jQuery(".stade_advisory").html(response);
           jQuery("#info-2 img.loader").hide();           
        },
        error: function() {
        	jQuery("#info-2 img.loader").hide();
        },
        complete: function() {
        	jQuery("#info-2 img.loader").hide();
        }
    });*/
	}
	
	
});
jQuery("#edit-submit-covid-states-advisory2" ).click(function(e){
		//var gatData = "/vaccine-state-advisory?title="+jQuery("#edit-title").val()+"&states="+jQuery("#edit-field-advisory-states-value").val()+"&category="+jQuery("#edit-field-advisory-category-tid").val();
		/*var gatData = "https://api.mygov.in/covid-advisory/?api_key=57076294a5e2ab7fe000000112c9e964291444e07dc276e0bca2e54b";
		alert("ok");
		jQuery(".stade_advisory").html('');
    jQuery("img.loader").show();
		jQuery.ajax({
        type: 'GET',
        url: gatData,
        dataType: 'text',
        success: function(response) { 
           jQuery(".stade_advisory").html(response);
           jQuery("img.loader").hide();
        },
        error: function() {
        	jQuery("img.loader").hide();
        },
        complete: function() {
        	jQuery("img.loader").hide();
        }
    });
	*/
	state_advisory();
	
	
});


//Language switcher popup
jQuery('.language-link').click(function(e) {
	if(jQuery(this).attr("lang")== "hi"){
 	 return confirm("You Are Redirecting to MyGov Hindi Language Portal.");
	}
	if(jQuery(this).attr("lang")== "en"){
 	return confirm("आप MyGov अंग्रेजी भाषा पोर्टल पर रीडायरेक्ट कर रहे हैं।");
	}
})

//Advisary page
if(jQuery('.advisory-tab').length > 0){
	jQuery('.advisory-tab .tabs li:first a').addClass('active');
jQuery('.advisory-tab .tabs li:first a').click(function(e){
	e.preventDefault();
	jQuery(this).addClass('active');
	jQuery('.advisory-tab .tabs li:last a').removeClass('active');
	jQuery('.advisory-list .tab2').hide();
	jQuery('.advisory-list .tab1').show();
})
jQuery('.advisory-tab .tabs li:last a').click(function(e){
	e.preventDefault();
	jQuery(this).addClass('active');
	jQuery('.advisory-tab .tabs li:first a').removeClass('active');
	jQuery('.advisory-list .tab1').hide();
	jQuery('.advisory-list .tab2').show();
})
}

// Footer activity list for mobile
if(jQuery(window).width() < 768){
	jQuery('.ft-label').click(function(){
		jQuery(this).next('.block-menu').slideToggle();
		jQuery(this).toggleClass('open');
	})
	jQuery('.mygov-app').click(function(){
		jQuery(this).next('.footer-mygov-app-wrapper').slideToggle();
		jQuery(this).toggleClass('open');
    })
}
// Tab at covid page notification section
jQuery(function() {	

	jQuery('.ctab a').click(function () {
		
	$this = jQuery(this);
     
	  var $target = jQuery(this).attr('href');
	    $this.parent().siblings().removeClass('active');
	    $this.parent().addClass('active')
		dropdownText = $this.text();
		$this.parents('.info_header').find('.dropdown-text').text(dropdownText);
		$this.parents('.info_block').find('.tab-content').hide();
		jQuery($target).show();
		
		$this.parents('.ctab').hide();
	
		return false;
	});
	jQuery('.ctab li:first-child a').trigger('click');
	
	jQuery('.dropdown-text').click(function(){
	  	jQuery(this).parents('.info_header').find('.ctab').slideToggle();
	})
	
	jQuery('.mobile_language').text(jQuery('li span.actv').text());
	jQuery('.mobile_language').click(function(){
	  	jQuery('#lang').slideToggle();
	})
})

//covid-19 Compaign page infographics slider for each tab

	jQuery('.islider').each(function(){
	  //jQuery(this).addClass('owl-carousel');
	 var owl = jQuery(this).owlCarousel({
		  loop:false,
		  dots:false,
		  nav:true,
		  margin:15,
		  responsiveClass:true,
		   navText : ["Previous","Next"],
		 responsive:{
          0:{
              items: 1
          },
		  569:{
		     items:2
	      },
		  768:{
		     items:3
	      }
		 }
		  
	  });
	  owl.on('changed.owl.carousel', function(event) { 
		jQuery('.view-all-items').parents('.owl-item').addClass('btn_wrap');
	})

	})
	
	/*Covid menu click page scroll*/
	
	 if(jQuery('.covid-menus').length > 0 ){
	jQuery('.covid_menu_list a').not('.out').click(function(e){
		e.preventDefault();
		var trigger = jQuery(this);
		//jQuery('.covid_menu_list a').removeClass('active');
		//trigger.addClass('active');
		
		var target = this.hash;
		var pos = jQuery(target).offset().top;
		jQuery('html, body').animate({
			scrollTop: pos - jQuery('.top_wrapper').height() +5
		});	
		//jQuery('.covid_menu_list').hide();
		
	})
	// covid dashboard block link click page scroll at target block
	jQuery('.state_btn,.state_link').click(function(e){
		e.preventDefault();
		var trigger = jQuery(this);
		var target = this.hash;
		var pos = jQuery(target).offset().top;
		jQuery('html, body').animate({
			scrollTop: pos - jQuery('.top_wrapper').height() +5
		});	
		
	})
	
		

 /* jQuery(document).on("scroll", function(event){
	  jQuery('.covid_menu_list a').each(function() {
		// console.log('555')
	  event.preventDefault();
      var currLink = jQuery(this);
	 
      var scrollPos = jQuery(document).scrollTop();
      var refElement = jQuery(currLink.attr("href"));
	 // console.log(refElement);
        if (refElement.offset().top - jQuery('.top_wrapper').height() <= scrollPos) {
            jQuery('.covid_menu_list a').removeClass("active");
            currLink.addClass("active");
         } else {
            currLink.removeClass("active");
          }
      });
	  
	  });*/
}

 if(jQuery('.ncc_wrapper').length > 0 ){
	jQuery('.readmore-btn a').click(function(e){
		e.preventDefault();
		var trigger = jQuery(this);
		var target = this.hash;
		var pos = jQuery(target).offset().top;
		jQuery('html, body').animate({
			scrollTop: pos - jQuery('.top_wrapper').height() +5
		});	
		
		
	})
 }
	
	
	
	
	
	jQuery('.showon').show()
jQuery('.infographics_links a').not(".t_video").click(function(e){
	e.preventDefault();
	
	jQuery('.infographics_links a').removeClass('active');
	jQuery(this).addClass('active');
	var targetBtn = jQuery(this).attr('href');
	jQuery('.infog_area').hide()
	jQuery(targetBtn).show();
})

  //covid-19 Compaign page contact slider for mobile
	 jQuery('.social_list').owlCarousel({
      loop:true,
	  dots:true,
	  nav:true,
      margin:15,
      responsiveClass:true,
	  dotsData: true,
	  navText : ["Previous","Next"],
      responsive:{
          0:{
              items: 1
          },
		  569:{
              items: 2
          },
		  768:{
		     items:3
	      },
		   1023:{
		     items:4
	      },
		  1200:{
		     items:5
	      }
		 }
	  });
	
	if(jQuery('.camp-slider').length > 0){
		jQuery('.camp-slider').owlCarousel({
		  loop:false,
		  dots:false,
		  nav:true,
		  margin:0,
		  responsiveClass:true,
		  responsive:{
			  0:{
				  items: 1
			  }
			 }
		  });
	  }  
	  
	  //Arch Compaign page slider
	if (jQuery('.arc-slider').length > 0) {  
	 jQuery('.arc-slider').owlCarousel({
		  loop:false,
		  dots:false,
		  nav:true,
		  margin:100,
		  responsiveClass:true,
		 responsive:{
          0:{
              items: 1,
			   margin:0
          },
		  569:{
		     items:2,
			  margin:15
			 
	      },
		  768:{
		     items:3,
			 margin:30
	      },
		  1024:{
		     margin:100
	      }
		 }
		  
	  });
	  
	}
	 // Podcast section slider for covid page
     if(jQuery('.podcast-slider').length > 0){
		  jQuery('.podcast-slider').owlCarousel({
		  loop:true,
		   dots:true,
		  margin:10,
		  dotsData: true,
		  responsiveClass:true,
		  responsive:{
			  0:{
				  items: 1
			  }
		  }
	  });
	 }
	  
	 
	
	//covid page slider for mobile
	 if(jQuery(window).width() < 768){
	 jQuery('.help_slider,.card-columns').owlCarousel({
      loop:true,
	  dots:true,
      margin:10,
      responsiveClass:true,
      responsive:{
          0:{
              items: 1
          },
	  500:{
		     items:2
	      }
		  }
	  });
	  
	 jQuery('.arogya_bhav').owlCarousel({
      loop:true,
	  dots:true,
      margin:10,
      responsiveClass:true,
      responsive:{
          0:{
              items: 1
          },
	  500:{
		     items:2
	      }
		 }
	  });
	  
	  jQuery('.event-block').each(function(){
		  jQuery(this).owlCarousel({
		  loop:true,
		   dots:true,
		  margin:10,
		  responsiveClass:true,
		  responsive:{
			  0:{
				  items: 1
			  },
			  567:{
				  items: 2
			  }
		  }
	  });
	  
	  })
	  
	 	  
	}
	
	

 // slider for state-wise corona data
 if (jQuery('.statewise_title').length > 0) {
	jQuery('.ac_title1').click(function(){
	   jQuery(this).toggleClass('on');
	   jQuery('.ac-block1').slideToggle('fast');	
		
	 })
		 
	jQuery('.latest_notify > a').click(function(){
	   jQuery('.ln-block').toggle();	
	 })
	// close covid lATEST NOTIFICATION on click outside
	jQuery(document).mouseup(function (e) {
		var ntl = jQuery('.latest_notify')
		if (!ntl.is(e.target) && ntl.has(e.target).length === 0) {
			jQuery(".ln-block").fadeOut();
			
		}
	});
	
	if(jQuery(window).width()< 600	){
		if(jQuery('.covid-data_hi').length){
			jQuery('.covid-data_hi th').not(':first').each(function () {
			 jQuery(this).text(jQuery(this).text().substring(0, 3))
		  })
		  jQuery('.covid-data_hi th:first').each(function () {
			 jQuery(this).text(jQuery(this).text().substring(0, 5))
		  })	
		}
		else{
		  jQuery('#state-covid-data th').not(':first').each(function () {
			 jQuery(this).text(jQuery(this).text().substring(0, 1))
		  })
	   }
	  
   }
	  
	  
 	 }

 	 // slide Toogle for state-wise vaccine data
 	if (jQuery('.statewise_vaccine').length > 0) {
		jQuery('.statewise_vaccine').click(function(){
		   jQuery(this).toggleClass('on');
		   jQuery('.state_vaccine_record').slideToggle('fast');	
			
		 })

 	}
	 // slide Toogle for vaccine centers 
 	if (jQuery('.center-api-list').length > 0) {
		jQuery('.center-api-list > a').click(function(){
		   jQuery('.center-api-list').toggleClass('on');
		   jQuery('.vaccination_centers_list').slideToggle('fast');	
			
		 })

 	}
	//Explore FAQs PDF in language
	if (jQuery('.faq-pdf').length > 0) {
		jQuery('.faq-pdf').click(function(){
		   jQuery('.vac-faq-list').slideToggle('fast');	
			
		 })

 	}
	 // get cowin certificate 
 	if (jQuery('.get_cert-btn').length > 0) {
		jQuery('.get_cert-btn').click(function(e){
			e.preventDefault();
		   jQuery('.cowin-cerificate-wrapper').slideToggle('fast');	
			
		 })

 	}
	// close covid lATEST NOTIFICATION on click outside
	jQuery(document).mouseup(function (e) {
		var getCert = jQuery('.get-cerificate')
		if (!getCert.is(e.target) && getCert.has(e.target).length === 0) {
			jQuery('.cowin-cerificate-wrapper').fadeOut();
			
		}
	});
	
// Notificaion and advisary block slider wrap items 10 for desktop and 2 for mobile	
	
	jQuery('.tslider').each(function(){
	var $pArr = jQuery(this).find('.stg_item');
	var pArrLen = $pArr.length;
  if(jQuery(window).width() > 767){
    var pPerDiv = 10;
	for (var i = 0;i < pArrLen;i+=pPerDiv){
		$pArr.filter(':eq('+i+'),:lt('+(i+pPerDiv)+'):gt('+i+')').wrapAll('<div class="state_book" />');
	}
	jQuery(this).addClass('owl-carousel');
	  jQuery(this).owlCarousel({
		  loop:false,
		  nav:true,
		  margin:10,
		  responsiveClass:true,
		  responsive:{
			  0:{
				  items: 1
			  }
		  }
		  
	  });
  }
  else{
    var pPerDiv = 2;
	for (var i = 0;i < pArrLen;i+=pPerDiv){
		$pArr.filter(':eq('+i+'),:lt('+(i+pPerDiv)+'):gt('+i+')').wrapAll('<div class="state_book" />');
	}
	jQuery(this).addClass('owl-carousel');
	  jQuery(this).owlCarousel({
		  loop:false,
		  nav:true,
		  margin:10,
		  responsiveClass:true,
		  responsive:{
			  0:{
				  items: 1
			  }
		  }
		  
	  });	  
	  }
	})

	

	// Tabs ====
	jQuery('#tabs div.tab-content').hide();
	jQuery('#tabs div.tab-content:first').show();
	jQuery('#tabs ul li:first').addClass('active');

	jQuery('#tabs ul li a').click(function () {
		jQuery('#tabs ul li').removeClass('active');
		jQuery(this).parent().addClass('active');
		var currentTab = jQuery(this).attr('href');
		jQuery('#tabs div.tab-content').hide();
		jQuery(currentTab).show();
		return false;
	});
// covid page myths model
	jQuery('.fact_btn').click(function(e){
		e.stopPropagation();
		jQuery('.overlay').show();
		 jQuery('#myth_model').fadeIn();
		
	})
	jQuery('.closePop').click(function(){
		jQuery('.overlay').hide();
		 jQuery('#myth_model').fadeOut();
	})
	//hide it when clicking anywhere else except the popup
	jQuery(document).click(function(event) {
	  //if you click on anything except the modal itself or the "open modal" link, close the modal
	  if (!jQuery(event.target).closest("#myth_model,.fact_btn,.popup-form-wrapper").length) {
		jQuery('.overlay,#myth_model,.popup-form-wrapper').hide();
	  }
	});
	 jQuery(document).keydown(function(event) { 
	  if (event.keyCode == 27) { 
		jQuery('.overlay,#myth_model,.popup-form-wrapper').hide();
	  }
	})
	
	//Home page user profile popup
	jQuery(document).click(function(event) {
	  //if you click on anything except the modal itself or the "open modal" link, close the modal
	  if (!jQuery(event.target).closest(".popup-form-wrapper").length) {
		jQuery('.popup-form-wrapper').hide();
	  }
	});
	jQuery('.close-popup,.close-btn').click(function(e){
		e.preventDefault();
		 jQuery('.popup-form-wrapper').fadeOut();
	})

	//covid resource pop-up display
	/*jQuery('.covid-res-btn-en').click(function(){
		alert('This link will take you to an external web site.');
	})
	jQuery('.covid-res-btn-hi').click(function(){
		alert('à¤¯à¤¹ à¤²à¤¿à¤‚à¤• à¤†à¤ªà¤•à¥‹ à¤à¤• à¤¬à¤¾à¤¹à¤°à¥€ à¤µà¥‡à¤¬à¤¸à¤¾à¤‡à¤Ÿ à¤ªà¤° à¤²à¥‡ à¤œà¤¾à¤à¤—à¤¾');
	})*/



    

// scroll on click text

	jQuery('.h-prev').click(function(event) {
			  event.preventDefault();
			  jQuery('.info-tab').animate({
				scrollLeft: "-=200px"
			  }, function(){
                // createCookie('scrollPos', $('#slide-wrap').scrollLeft());
                scrollArrowShow();
         });
	});
	
	 jQuery('.h-next').click(function(event) {
		  event.preventDefault();
		  jQuery('.info-tab').animate({
		   scrollLeft: "+=200px"
		  }, function(){
                // createCookie('scrollPos', $('#slide-wrap').scrollLeft());
                scrollArrowShow();
         });
	});
	 function scrollArrowShow() {
      	var $elem = jQuery('.info-tab');
		  var newScrollLeft = $elem.scrollLeft(),
			  width = $elem.width(),
			  scrollWidth = $elem.get(0).scrollWidth;
		  var offset = 0;
		  if (scrollWidth - newScrollLeft - width === offset) {
			  jQuery('.h-next').css({visibility: 'hidden'});
		  }else{
            jQuery('.h-next').css({visibility: 'visible'});
          }
		  if (newScrollLeft === 0) {
			jQuery('.h-prev').css({visibility: 'hidden'});
        }else{
            jQuery('.h-prev').css({visibility: 'visible'});
        
		  }
    }

	// Toggle Megha Menu **********

	jQuery(".res_menu").click(function (e) {
		e.preventDefault();
		jQuery(this).toggleClass('open_meghamenu');
		jQuery('.flyout-menu-wrapper').slideToggle();
	})

	// close Megha Menu  outside click
	jQuery(document).mouseup(function (e) {
		var menuwrap = jQuery('.header-main-flyout-menu');
		if (!menuwrap.is(e.target) && menuwrap.has(e.target).length === 0) {
			jQuery('.flyout-menu-wrapper').fadeOut();
			jQuery('.res_menu').removeClass('open_meghamenu');
		}
	});

	jQuery(".nav-menu-close").click(function (e) {
		jQuery('.flyout-menu-wrapper').slideUp();
		jQuery(".res_menu").removeClass('open_meghamenu');
	})
	
	// Toggle covid 19 Menu **********

	jQuery(".covid-menus .sticky-menu-btn").click(function (e) {
		e.preventDefault();
		jQuery('.covid-menus').toggleClass('extend');
		//jQuery('.covid_menu_list').slideToggle();
	})
	
	
	jQuery(".close_menus").click(function (e) {
		e.preventDefault();
		jQuery('.covid-menus').removeClass('extend');
	})

	// close Megha Menu  outside click
	jQuery(document).mouseup(function (e) {
		var menuwrap1 = jQuery('.covid-menus');
		if (!menuwrap1.is(e.target) && menuwrap1.has(e.target).length === 0) {
			jQuery('.covid-menus').removeClass('extend');
		}
	});

	
	
	// Toggle  Socialhub Megha Menu **********

	jQuery(".header-social-block > a").click(function (e) {
		e.preventDefault();
		jQuery(this).toggleClass('open_socialmenu');
		jQuery('.shub-menu-wrapper').slideToggle();
	})

	// close Socialhub Megha Menu  outside click
	jQuery(document).mouseup(function (e) {
		var menuwrapn = jQuery('.header-social-block');
		if (!menuwrapn.is(e.target) && menuwrapn.has(e.target).length === 0) {
			jQuery('.shub-menu-wrapper').fadeOut();
			jQuery('.header-social-block a').removeClass('open_socialmenu');
		}
	});

	jQuery(".nav-smenu-close").click(function (e) {
		jQuery('.shub-menu-wrapper').slideUp();
		jQuery(".header-social-block a").removeClass('open_socialmenu');
	})




	// Toggle mygov states
	jQuery(".region-header .mygov-states").click(function () {
		jQuery(this).toggleClass('show-state');
		jQuery(this).siblings('.mygov-states-inner').slideToggle();
		jQuery(this).parents('.lang-box').find('.mygov-apps').removeClass('show-applist');
	})


	// close mygov states on click outside
	jQuery(document).mouseup(function (e) {
		var states = jQuery('#block-common-utils-mygov-sites')
		if (!states.is(e.target) && states.has(e.target).length === 0) {
			jQuery(".region-header .mygov-states-inner").fadeOut();
			jQuery('.region-header .mygov-states').removeClass('show-state');

		}
	});

	// Toggle mygov App list
	jQuery(".mygov-apps").click(function () {
		jQuery(this).toggleClass('show-applist');
		jQuery(this).siblings('.mygov-apps-inner').slideToggle();
		jQuery(this).parents('.lang-box').find('.mygov-states').removeClass('show-state');
	})

	// close mygov App list on click outside
	jQuery(document).mouseup(function (e) {
		var states = jQuery('#block-common-utils-mygov-apps')
		if (!states.is(e.target) && states.has(e.target).length === 0) {
			jQuery(".region-header .mygov-apps-inner").fadeOut();
			jQuery('.region-header .mygov-apps').removeClass('show-applist');
		}
	});


	//Search Toggle
	jQuery('.search_toggle').click(function () {
		//jQuery('.the_box').slideToggle();
		jQuery('.search_mygov_box').toggleClass('active_search');
		jQuery('.region-header .mygov-states').removeClass('show-state');
		jQuery('.region-header .mygov-apps').removeClass('show-applist');
	})

	//Home Popup
	var date = new Date();
	var minutes = 1440;
	date.setTime(date.getTime() + (minutes * 60 * 1000));

	if (jQuery('#profile-popup-form').length > 0) {
		jQuery('.badge-wrap').hide();
		jQuery.cookie('msg', 'str', { expires: date });
	}

	jQuery('.badge-popup-close').click(function () {
		jQuery('.badge-wrap').hide();
		jQuery.cookie('msg', 'str', { expires: date });
	})

	var getPop = jQuery('.badge-wrap');
	if (getPop.length > 0) { //console.log('gotit');
		if (jQuery.cookie('msg') == null) {
			jQuery('.badge-wrap').show();
			jQuery.cookie('msg', 'str', { expires: date });
		}
		else {
			jQuery('.badge-wrap').hide();
		}
	}

// 	if (jQuery('.dark_bg').length > 0) { 
// 	if (jQuery.cookie('msg1') == null) {
// 		jQuery('.dark_bg').show();
// 		jQuery.cookie('msg1', 'str', { expires: date });
// 	}
// 	else {
// 		jQuery('.dark_bg').hide();
// 	}
//   }

// 	jQuery('.dark_bg').click(function () {
// 		jQuery('.dark_bg').hide();
// 		jQuery.cookie('msg1', 'str', { expires: date });
// 	})

	jQuery(document).click(function (e) {
		if (!jQuery(e.target).hasClass("search_toggle") && jQuery(e.target).parents(".header-search-block").length === 0) {
			//jQuery(".the_box").hide();
			jQuery('.search_mygov_box').removeClass('active_search');
		}
	});

	// Notification toggle

	jQuery('.header-push-notification a').click(function () {
		jQuery('.notification-container').slideToggle();
		jQuery('.header-push-notification').toggleClass('show');
	})

	jQuery(document).mouseup(function (e) {
		var notifyBlock = jQuery(".header-push-notification");
		if (!notifyBlock.is(e.target) && notifyBlock.has(e.target).length === 0) {
			jQuery(".notification-container").fadeOut();
			jQuery('.header-push-notification').removeClass('show');
		}
	});


	// close Notification in logged status

	jQuery(document).mouseup(function (e) {
		var container = jQuery(".header-push-notification");
		if (!container.is(e.target) && container.has(e.target).length === 0) {
			jQuery("#ogpl-alert-notify-list").fadeOut();
		}
	});

	//Close login menu
	jQuery(document).mouseup(function (e) {
		var menubox = jQuery('#block-views-my-details-block');
		var logout_box = jQuery('.logged-in .notification_user');
		if (!menubox.is(e.target) && menubox.has(e.target).length === 0 && !logout_box.is(e.target) && logout_box.has(e.target).length === 0) {
			jQuery(".notification_user").fadeOut();
		}
	});

	//Fixed header on scroll

	jQuery(window).scroll(function () {
		var headerH = jQuery('.top_wrapper').height();
		if (jQuery('.top_wrapper').css('display') != 'none') {
			if (jQuery(this).scrollTop() > jQuery('.top_wrapper').height() - 20) {
				jQuery('.top_wrapper').addClass("sticky");
				jQuery('body').css('paddingTop', headerH);

			} else {
				jQuery('.top_wrapper').removeClass("sticky");
				jQuery('body').css('paddingTop', '0');

			}
		}
	});

	// Mobile menu 
	if (jQuery(window).width() < 768) {
		jQuery('.menu-container > div > span').click(function () {
			jQuery(this).parent('.menu-row').siblings().find('.menu-res').slideUp();
			jQuery(this).next('.menu-res').slideToggle();
			jQuery(this).parent('.menu-row').toggleClass('extend_box');
			jQuery(this).parent('.menu-row').siblings().removeClass('extend_box');

		})
	}

	//Pariksha pe charcha

	jQuery('.acc_survey_header').click(function () {
		jQuery(this).toggleClass('expend');
		jQuery(this).next('.acc_survey_block').slideToggle('fast');
	})

	// Ticker js
	if (jQuery('.view-ticker-block').length) {
		jQuery('.view-ticker-block').jConveyorTicker({ reverse_elm: true });
	}
	
	// Ticker js for covid-19 page
	if (jQuery('.marquee').length) {
		jQuery('.marquee').jConveyorTicker({ reverse_elm: true });
	}
	// stricky menu display after scroll
 if(jQuery('.main-activities-status').length > 0){
	var str_offset = jQuery('.main-activities-status').offset().top;
	jQuery(window).scroll(function () {
		if (jQuery(window).scrollTop() > str_offset) {

			jQuery('body').addClass('stricky_menu');
		}
		else {
			jQuery('body').removeClass('stricky_menu');

		}
	})
}


	// tricker jquery

	//var mqr =jQuery('.view-id-ticker_block').hover(function(){
	//    jQuery('.view-id-ticker_block').addClass('pause_ticker');	
	//},
	//function(){
	//	jQuery('.view-id-ticker_block').removeClass('pause_ticker');
	//});



	// skip content

	jQuery('.skip_content').click(function (evn) {
		evn.preventDefault();
		var target = this.hash;
		var pos = jQuery(target).offset().top;
		jQuery('html, body').animate({
			scrollTop: pos - jQuery('.top_wrapper').height()
		});
	});



	jQuery("#group_switch_btn").click(function () {
		jQuery("#groups_list").slideToggle();
		jQuery(".group_name_selected").toggleClass('active');
		jQuery("#group_switch_btn").toggleClass('up');
	});

	jQuery('.block-do-discuss-filter .views-exposed-form #edit-title-wrapper label, .block-do-discuss-filter .views-exposed-form #edit-field-hashtags-tid-wrapper label').click(function () {
		jQuery('.block-do-discuss-filter .views-exposed-form #edit-title-wrapper .views-widget input[type="text"], .block-do-discuss-filter .views-exposed-form #edit-field-hashtags-tid-wrapper .views-widget input[type="text"]').toggle();
	});
	jQuery('.search_area .search_toggle').click(function () {
		jQuery('.search_box').toggle();
	});





	var collectOnMe = document.querySelectorAll('.collectonme'),
		buttons = document.getElementsByTagName("input");

	for (var i = 0; i < collectOnMe.length; i++) {
		collectOnMe[i].style.display = "none";
	}

	
	
	//default options
	//var testContainer = document.querySelector('.site-wrapper'),
	//				testContainerIsSnowing = true;
	//
	//		snowFall.snow(testContainer,{round : true, minSize: 3, maxSize:5});
	//
	//		testContainer.addEventListener('click', function(e){
	//				testContainerIsSnowing = !testContainerIsSnowing;
	//
	//				if(!testContainerIsSnowing){
	//						snowFall.snow(testContainer, "clear");
	//				}else{
	//						snowFall.snow(testContainer);
	//				}
	//		})


	jQuery(document).keydown(function (event) {
		if (event.keyCode == 27) {
			jQuery('#web_notification').hide();
			jQuery('.badge-wrap').hide();
			jQuery.cookie('msg', 'str', { expires: date });

		}
	})

	jQuery('.notification-close,#web_notification').click(function () {
		jQuery('#web_notification').fadeOut();
	})

	if (jQuery('#block-mygov-gratification-top-user').length) {
		jQuery('#block-mygov-gratification-top-user .content').flexslider();
	}

	// view result btn
	if (jQuery('.result-url').length) {
		jQuery('.closed_task').addClass('new_btn');
	}
	
	// covid -19 state wise status change in link
	if(jQuery('.field-name-field-district-reporting').length ){
	 var linkText = jQuery('.field-name-field-district-reporting .field-item').text();
     jQuery('.field-name-field-district-reporting .field-item').html('<a target="_blank" href="'+linkText+'">'+linkText+'</a>');
	}
	
	if(jQuery('.node-corona-data .field-name-field-whatsapp-chatbot-url').length ){
	jQuery('.field-name-field-whatsapp-chatbot-url,.field-name-field-fb-chatbot-url,.field-name-field-e-pass-url,.field-name-field-fb-url,.field-name-field-whatsapp-chatbot').each(function () {
	 var linkText = jQuery(this).find('.field-item').text();
     jQuery(this).find('.field-item').html('<a target="_blank" href="'+linkText+'">'+linkText+'</a>');
	})
	}
	
   
   
   // Animating number on covid page
   /*
    if (jQuery('.icount').length) { 
		jQuery('.icount').counterUp({
			delay: 10,
			time: 1000
		});
	}
   */
 
if(jQuery('#state-covid-data').length){
var oTable;
var oSettings;
 oTable=jQuery('#state-covid-data').DataTable( {
	  pageLength: 6,
	  "order": [[ $('td.now').index(), "desc" ]],
	  //"order": [[ 1, "desc" ]],
        "info":false,
        "pagingType": "full_numbers",
         responsive: true,
	
	});
	
    oSettings = oTable.settings();
	
	jQuery("#btn-load-more").on('click',function(){
	   oSettings[0]._iDisplayLength = oSettings[0].fnRecordsTotal();
	   oTable.draw(); 
	    jQuery(this).hide();
	});
	
}
	//var visible = false;
//    var tableContainer = jQuery(oTable.table().container());
//      jQuery('.statewise_title').click(function(){
//		   jQuery(this).toggleClass('on');
//		   jQuery('.state_record').toggle('fast',function(){
//			     tableContainer.css( 'display', visible ? 'none' : 'block' );
//           oTable.fixedHeader.adjust();
// 
//             visible = ! visible;
//			});
//		 
//			
//		 })


// weblink for trevelling list
 jQuery('.getpass').click(function(e){
	 e.preventDefault();
	jQuery('.helpno_list').hide();
    jQuery('.weblink_list').toggle(); 
 })
 
 jQuery('.helplines-block').click(function(e){
	 e.preventDefault();
	jQuery('.weblink_list').hide();
    jQuery('.helpno_list').toggle(); 
 })
 
  jQuery('.close_list').click(function(){
    jQuery(this).parents('.card_list').hide(); 
 })

 // weblink for helpline list
 jQuery('.helplines-block,.close_helplines').click(function(e){
	 e.preventDefault();
    jQuery('.weblink_helplines').slideToggle(); 
 })
 
 
 //Accordian jquery
 if(jQuery('.c-accordian').length){
	jQuery('.c-accordian h3').click(function() {
		//REMOVE THE ON CLASS FROM ALL BUTTONS
		jQuery('.c-accordian h3').removeClass('on');
		  
		//NO MATTER WHAT WE CLOSE ALL OPEN SLIDES
	 	jQuery('.c-accordian > .content-body').slideUp('normal');
   
		//IF THE NEXT SLIDE WASN'T OPEN THEN OPEN IT
		if(jQuery(this).next().is(':hidden') == true) {
			
			//ADD THE ON CLASS TO THE BUTTON
			jQuery(this).addClass('on');
			  
			//OPEN THE SLIDE
			jQuery(this).next().slideDown('normal');
		 }
		  
	 });
	 jQuery('.content-body').hide();
	//jQuery('.content-body:first-of-type').show();
	//jQuery('.show').show();
	//jQuery('.c-accordian h3:first-child').addClass('on');
   }
});






(function (jQuery) {
	jQuery(window).on("load", function () {
		jQuery(".scroll-wrap").mCustomScrollbar();
		if (jQuery(".update_block").length > 0) {
			var target = window.location.hash;
			if(target.length){
				var pos = jQuery(target).offset().top;
				var siteHeadH =jQuery('.top_wrapper').height();
				jQuery('html, body').animate({
					scrollTop: pos - 140
				});
				//jQuery(target).trigger('click'); 
			}		
		}
		if(jQuery('.play-podcast').length > 0){
				// podcast load on click 
		jQuery('.play-podcast ').each(function () {
			jQuery("#podcast .audio").html('<audio controls autoplay style="display:none;"><source  src="" type="audio/mpeg"></audio>');
			 jQuery(this).click(function(){
			  jQuery(this).hide();
			  var audUrl =jQuery(this).attr('rel');
			 // console.log(audUrl);
			  jQuery(this).parents('.event-items').find('source').attr('src', audUrl);
			  jQuery(this).parents('.event-items').find('audio').load().show();
			})
			
			
			
		})
		
		var vidDefer = document.getElementsByTagName('iframe');
			for (var i=0; i<vidDefer.length; i++) {
			if(vidDefer[i].getAttribute('data-src')) {
			vidDefer[i].setAttribute('src',vidDefer[i].getAttribute('data-src'));
		 } 
		} 
	
		//jQuery('.pause-podcast ').each(function () {
//			 jQuery(this).click(function(){
//			   jQuery(this).sibling().find('audio').pause()
//			})
//		})
		}
	});
})(jQuery);

jQuery(".mygov_survey iframe").on('load', function () {
	//var cm = jQuery('.mygov_survey iframe').contents().find("body").height();
	jQuery('.mygov_survey iframe').height(800);

	if (jQuery(this).contents().find('.group-name').text() == 'Awareness And Usage of MyGov') {
		jQuery(this).height(jQuery(this).contents().find("body").outerHeight() + 1600);
		//window.scrollTo(500, 500);

	}
	else {
		//alert(jQuery(this).height( jQuery(this).contents().find("body").outerHeight()));

		jQuery(this).height(jQuery(this).contents().find("body").outerHeight() + 500);
	}
	if (jQuery(this).contents().find('#bootstrap-alert-box-modal').length > 0) {
		window.scrollTo(500, 500);
	}
	if (jQuery(this).contents().find(".reloadlink").length > 0) {
		this.contentWindow.location.reload(true);
		//location.reload();
	}
	if (jQuery(this).contents().find('#tokenmessage>span:has(a)').length == 0 && jQuery(this).contents().find("#tokenmessage>span").length > 0) {
		location.reload();
	}
});


/*******************************************************************************
 * 2. Tabs for login page==================================================
 ******************************************************************************/

jQuery(document).ready(function () {

	if (jQuery(window).width() < 300) {
		jQuery("body.page-user-login #block-pwdless-login-pwdless-login-block").hide();
		jQuery("body.page-user-login #block-system-main").hide();
		jQuery("body.page-user-login #block-system-main").before('<div id="tabs"><ul class="tabs"><li class="tab-link1"><a href="#block-system-main">Log In With Password</a></li><li class="tab-link2"><a href="#block-pwdless-login-pwdless-login-block">Log In With OTP</a></li></ul></div>');
		jQuery('body.page-user-login ul.tabs li.tab-link1 a').click(function () {
			jQuery("body.page-user-login #block-system-main").show();
			jQuery("body.page-user-login #block-pwdless-login-pwdless-login-block").hide();
		})
		jQuery('body.page-user-login ul.tabs li.tab-link2 a').click(function () {
			jQuery("body.page-user-login #block-pwdless-login-pwdless-login-block").show();
			jQuery("body.page-user-login #block-system-main").hide();
		})

	}
});




/*******************************************************************************
 * Comment Load More ==================================================
 ******************************************************************************/
(function ($) {
	Drupal.behaviors.commentLoadMore = {
		attach: function (context, settings) {
			// Stem star and card page
			jQuery('.awardi-info .card-btn').on('click',function () {
				jQuery(this).parents('.views-row').addClass('showCard');
		
			})
			jQuery('.card-close').on('click',function () {
				jQuery(this).parents('.views-row').removeClass('showCard');
		
			})

			jQuery('.podcast_img').on('click', function () {
				var audio = jQuery(this).parent('.do_box').find('.audio audio')[0];
				if (audio.paused) {
				audio.play();
				}
				else{audio.pause();}
			 
			})

			$('#comment-load-more', context).click(
				function () {
					var base = $(this).attr('id');
					var url = $(this).attr('href');

					var element_settings = {
						url: url,
						event: 'loadMore',
					};

					Drupal.ajax[base] = new Drupal.ajax(base, this,
						element_settings);

					$(this).trigger('loadMore');
					return false;
				});



			jQuery('.group_stats > a').off("click").on('click', function (event) {
				event.preventDefault();
				jQuery(this).parents('.group_stats').find('.group_info_wrap').slideToggle();
				jQuery(this).parents('.group_stats').toggleClass('show');
			})

		}
	};
}(jQuery));


/*******************************************************************************
 * User Profile Page Task Toggle
 * ==================================================
 ******************************************************************************/

/**
 * Behaviors for collapsible menu.
 */
//(function($) {
//    /**
//     * Adds toggle link.
//     * Toggles menu on small resolutions.
//     * Restores menu on window width increasing.
//     */
//    Drupal.behaviors.pageTaskToggle = {
//        attach: function (context, settings) {
jQuery(document).ready(function () {
	jQuery('#block-views-my-details-block').click(function () {
		jQuery('#notification_user_menu').toggle('fast');
	});
	jQuery('#block-views-my-details-block-1').css("cursor",
		"pointer");

	jQuery('#block-views-groupissue-block-2').css('display',
		'none');

	jQuery('#task_tab').css('cursor', 'pointer');
	jQuery('#groupissue_tab').css('cursor', 'pointer');

	jQuery('#edit-timezone').addClass('collapsed');
	jQuery('#edit-heartbeat').addClass('collapsed');


	jQuery('.home-slider-text a').attr('target', '_blank');

	jQuery('#edit-field-gi-comment-file legend').css('display',
		'none');
	jQuery('#edit-field-comment-file label').css('display',
		'none');

	jQuery('.page-groups #block-system-main').addClass('grid');
	var youtubePlaceholde = Drupal.t('Put youtube Video ID. e.g flWwMxGilAY');
	var hashtagPlaceholde = Drupal.t('Search by Hashtag');
	var searchPlaceholde = Drupal.t('Search by Title');
	var sharePlaceholde = Drupal.t('Share Your Views...');
	var submitPlaceholde = Drupal.t('Submit Your Task...');

	jQuery('#edit-field-video input').attr('placeholder', youtubePlaceholde);
	jQuery('.page-node #edit_search').attr('placeholder', hashtagPlaceholde);
	jQuery('.page-home #edit_search').attr('placeholder', searchPlaceholde);
	jQuery('.page-groups #edit_search').attr('placeholder', searchPlaceholde);
	jQuery('.node-type-group-issue #edit-comment-body textarea').attr('placeholder', sharePlaceholde);
	jQuery('.node-type-task #edit-comment-body textarea').attr('placeholder', submitPlaceholde);

	//Image map of front page slider...
	jQuery('.view-homepage-slider .view-content .flexslider .slides ').find('li').each(function () {
		var map_name = jQuery(this).find('.views-field.views-field-field-banner-image .field-content map').attr("name");
		if (map_name != undefined) {
			jQuery(this).find('.views-field.views-field-field-banner-image .field-content img').attr("usemap", "#" + map_name);
		}

	});
	
	

	jQuery('#sms-user-settings-reset-form #edit-number label')
		.html('Your Mobile Number');

	jQuery("#edit-field-user-picture-und-0-ajax-wrapper .description")
		.text(jQuery("#edit-field-user-picture-und-0-ajax-wrapper .description").text().substring(29));
	var moreText = Drupal.t('more');

	jQuery("#block-views-view-comments-block-8 .view-content").append("<a id='more-link'>" + moreText + "</a>");
	jQuery("#more-link").click(function () {
		jQuery("#featured_tab").click();
		jQuery('html, body').animate({
			scrollTop: jQuery("#block-system-main").offset().top
		}, 2000);
	});

	// Podcast page slider
	jQuery('.podcast-top-view .view-content').addClass('owl-carousel');
	jQuery('.podcast-top-view .view-content').owlCarousel({
		loop:false,
		nav:true,
		margin:15,
		responsiveClass:true,
		dots:true,
		responsive:{
			0:{
				items: 1
			},
			480:{
				items: 2
			},
			768:{
				items: 3
			}
		}
		
	});	

	jQuery('.podcast-top-view .views-field-field-podcast-image').click(function () {
		var audio = jQuery(this).parent('.views-row').find('.views-field-field-mp3-file audio')[0];
		if (audio.paused) {
		audio.play();
		}
		else{
			audio.pause();	
		}
	 
	})
	jQuery('.img-podcast').click(function () {
		var audio = jQuery(this).parent('.podcast-item').find('.mp3-podcast audio')[0];
		if (audio.paused) {
		audio.play();
		}
		else{
			audio.pause();	
		}
	 
	})
	
});
//  }
//    }
//})(jQuery);


/*******************************************************************************
 * My Submissions Ajax View ==================================================
 ******************************************************************************/
(function ($) {

	$("#my_submissions").hide();
	$(".all_comments").show();

	Drupal.behaviors.mygov_submission_show = {
		attach: function (context, settings) {
			jQuery(document).ajaxComplete(function () {
				jQuery('.comment-unpublished').parents('.ajax-comment-wrapper').addClass('unpublish_wrapper');
			})
			$('#reset_tab:not(.mygov-ajax-processed)', context).addClass('mygov-ajax-processed').click(function () {
				var nid = $("#task_nid").val();
				jQuery(".all_comments").prependTo("#post_list-wrapper-nid-" + nid);
				$(".all_comments").show();
				$("#my_submissions").hide();
				$("#talk_discussions").hide();
				$("#under_moderation").hide();
				$("#talk_ivrs").hide();
				$("#talk_featured").hide();
				if ($('.bottom_nav_wrapper').find('.links_wrapper').length > 0) {
					$(".links_wrapper").show();
					$(".comment_body_wrapper").hide();
				}
				else {
					$(".comment_body_wrapper").show();
				}
				if ($('.bottom_nav_wrapper').find('.talk_end').length > 0) {
					$(".comment_body_wrapper").hide();
				}
				if ($('.bottom_nav_wrapper').find('.not_started').length > 0) {
					$(".comment_body_wrapper").hide();
				}
				$("#reset_tab").addClass("active");
				$("#my_submissions_tab").removeClass("active");
				$("#moderate_tab").removeClass("active");
				$("#discussions_tab").removeClass("active");
				$("#ivrs_tab").removeClass("active");
				$("#featured_tab").removeClass("active");
			});
			$('#my_submissions_tab').click(function () {
				var nid = $("#task_nid").val();
				if (!$(this).hasClass('mygov-ajax-processed-once')) {
					var base = $(this).attr('id');
					var element_settings = {
						url: '/show-my-submissions/' + nid,
						event: 'submissions',
					};

					Drupal.ajax[base] = new Drupal.ajax(base,
						this, element_settings);
					$(this).trigger('submissions');
					$(this).addClass('mygov-ajax-processed-once');

				}

				$(".links_wrapper").hide();
				$(".comment_body_wrapper").hide();
				$(".all_comments").hide();
				$("#talk_discussions").hide();
				$("#under_moderation").hide();
				$("#talk_ivrs").hide();
				$("#talk_featured").hide();
				jQuery("#my_submissions").prependTo("#post_list-wrapper-nid-" + nid);
				$("#my_submissions").show();

				$("#reset_tab").removeClass("active");
				$("#moderate_tab").removeClass("active");
				$("#discussions_tab,#featured_tab").removeClass("active");
				$("#my_submissions_tab").addClass("active");

				return false;
			});



			$('#moderate_tab').click(function () {
				var nid = $("#task_nid").val();
				if (!$(this).hasClass('mygov-ajax-processed-once')) {
					var base = $(this).attr('id');
					var element_settings = {
						url: '/show-under-moderation/' + nid,
						event: 'under_moderation',
					};

					Drupal.ajax[base] = new Drupal.ajax(base,
						this, element_settings);
					$(this).trigger('under_moderation');
					$(this).addClass('mygov-ajax-processed-once');

				}

				$(".all_comments").hide();
				$(".links_wrapper").hide();
				$(".comment_body_wrapper").hide();
				$(".all_comments").hide();
				$("#my_submissions").hide();
				$("#talk_ivrs").hide();
				$("#talk_featured").hide();
				$("#talk_discussions").hide();
				jQuery("#under_moderation").prependTo("#post_list-wrapper-nid-" + nid);
				$("#under_moderation").show();

				$("#reset_tab").removeClass("active");
				$("#my_submissions_tab").removeClass("active");
				$("#discussions_tab").removeClass("active");
				$("#moderate_tab").addClass("active");
				return false;
			});

			$('#discussions_tab').not('.mygov-ajax-processed').addClass(
				'mygov-ajax-processed').click(function () {
					var nid_val = $("#task_nid").val();
					if (!$(this).hasClass('mygov-ajax-processed-once')) {
						var base = $(this).attr('id');
						if ($("#discussion_nid").val()) {
							var nid = $("#discussion_nid").val();
						}
						else {
							var nid = null;
						}

						var element_settings = {
							url: '/show-talk-discussions/' + nid,
							event: 'talk_discussion',
						};

						Drupal.ajax[base] = new Drupal.ajax(base,
							this, element_settings);
						$(this).not(".active").trigger('talk_discussion');
						$(this).addClass('mygov-ajax-processed-once');
					}
					$(".links_wrapper").hide();
					$(".comment_body_wrapper").hide();
					$("#discussions_tab").addClass("active");
					$("#ivrs_tab").removeClass("active");
					$("#featured_tab").removeClass("active");
					$("#reset_tab").removeClass("active");
					$("#my_submissions_tab").removeClass("active");

					$("#talk_ivrs").hide();
					$("#talk_featured").hide();
					$("#my_submissions").hide();
					$(".all_comments").hide();
					jQuery("#talk_discussions").prependTo("#post_list-wrapper-nid-" + nid_val);
					$("#talk_discussions").show();
					$("#under_moderation").hide();
					return false;
				});

			//featured comment tab for talk
			$('#featured_tab').not('.mygov-ajax-processed').addClass(
				'mygov-ajax-processed').click(function () {
					var nid_val = $("#task_nid").val();
					if (!$(this).hasClass('mygov-ajax-processed-once')) {
						var base = $(this).attr('id');
						if ($("#discussion_nid").val()) {
							var nid = $("#discussion_nid").val();
						}
						else {
							var nid = null;
						}
						var element_settings = {
							url: '/show-featured-comments/' + nid,
							event: 'talk_featured',
						};

						Drupal.ajax[base] = new Drupal.ajax(base,
							this, element_settings);
						$(this).not(".active").trigger('talk_featured');
						$(this).addClass(
							'mygov-ajax-processed-once');

					}
					$(".links_wrapper").hide();
					$(".comment_body_wrapper").hide();
					$("#discussions_tab,#my_submissions_tab,#reset_tab").removeClass("active");
					$("#ivrs_tab").removeClass("active");
					$("#featured_tab").addClass("active");

					$("#talk_discussions").hide();
					$("#under_moderation").hide();
					$("#talk_ivrs").hide();
					$("#my_submissions").hide();
					$(".all_comments").hide();
					jQuery("#talk_featured").prependTo("#post_list-wrapper-nid-" + nid_val);
					$("#talk_featured").show();
					return false;
				});

			//ivrs comment tab for talk
			$('#ivrs_tab').not('.mygov-ajax-processed').addClass(
				'mygov-ajax-processed').click(function () {
					var nid_val = $("#task_nid").val();
					if (!$(this).hasClass('mygov-ajax-processed-once')) {
						var base = $(this).attr('id');
						if ($("#discussion_nid").val()) {
							var nid = $("#discussion_nid").val();
						}
						else {
							var nid = null;
						}
						var element_settings = {
							url: '/show-ivrs-comments/' + nid,
							event: 'ivrs_comments',
						};

						Drupal.ajax[base] = new Drupal.ajax(base,
							this, element_settings);
						$(this).not(".active").trigger('ivrs_comments');
						$(this).addClass('mygov-ajax-processed-once');

					}
					$(".links_wrapper").hide();
					$(".comment_body_wrapper").hide();
					$("#discussions_tab").removeClass("active");
					$("#featured_tab").removeClass("active");
					$("#ivrs_tab").addClass("active");

					$("#talk_discussions").hide();
					$("#under_moderation").hide();
					$("#talk_featured").hide();
					$("#my_submissions").hide();
					$(".all_comments").hide();
					jQuery("#talk_ivrs").prependTo("#post_list-wrapper-nid-" + nid_val);
					$("#talk_ivrs").show();
					return false;
				});
		}
	};

}(jQuery));

/** Activity Page Icons Span Append **/
(function ($) {
	Drupal.behaviors.activity_page_icons = {
		attach: function (context, settings) {

			// jQuery('.post').parents('div.views-row').prepend('<span class="activities_icon post_icon"></span>');
			// jQuery('.like').parents('div.views-row').prepend('<span class="activities_icon like_icon"></span>');
			// jQuery('.hour').parents('div.views-row').prepend('<span class="activities_icon hour_icon"></span>');
			// jQuery('.task').parents('div.views-row').prepend('<span class="activities_icon task_icon"></span>');
			// jQuery('.grp').parents('div.views-row').prepend('<span class="activities_icon grp_icon"></span>');

		}
	}

}(jQuery));

/** Coment Box Show/Hide on Content Details Page **/
/*(function($) {
	Drupal.behaviors.comment_form_show = {
		attach : function(context, settings) {

			jQuery('.submit_comment_button').click(function(){
			  jQuery('#comments form').toggle('slow');
			});

		}
	}

}(jQuery));*/



/** Switch Group Text Change in Group select List on every page
(function($) {
	Drupal.behaviors.switch_group_select = {
		attach : function(context, settings) {

		  jQuery('#edit-group option:selected').html('Select a Group');
                  jQuery('#edit-group-select option:selected').html('Select a Group');

		}
	}

}(jQuery));
**/


/** Poll Submission on selecting atleast one option from the form. **/
(function ($) {
	Drupal.behaviors.mygov_poll_form = {
		attach: function (context, settings) {
			jQuery('.vote-form input.form-submit').attr('disabled', true);
			jQuery('.poll_questions .field-items .field-item').each(function () {
				jQuery(this).find('.form-item-choice label:first').hide();
			});
			jQuery('.container').find('.vote-form').each(
				function () {
					var vote_submit = jQuery(this)
						.find('input.form-submit');
					jQuery(this).find('.choices input.form-radio')
						.click(
							function () {
								jQuery(vote_submit).attr(
									'disabled', false);
							});
				});
			jQuery(".node-poll h2 a").removeAttr("href");
			jQuery(".node-poll h2 a").css("cursor", "pointer");
		}
	};

}(jQuery));

/*
(function($, Drupal) {
	// put function into drupal commands:
	Drupal.ajax.prototype.commands.changeBrowserURL = function(ajax,
			response, status) {
		// response object as passed in our Ajax callback
		// do what you want in here
		window.history.pushState('', '', response.url);
	};
}(jQuery, Drupal));
*/


/** All Groups Page Sort order switch **/
(function ($) {
	Drupal.behaviors.groups_sort_by = {
		attach: function (context, settings) {
			$('#group_sort select').change(function () {
				var url = $(this).val(); // get selected value
				if (url) { // require a URL
					window.location = url; // redirect
				}
				return false;
			});
		}
	}

}(jQuery));

/** Comment Page Sort order switch **/
(function ($) {
	Drupal.behaviors.comment_sort_by = {
		attach: function (context, settings) {
			$('#comment_sort select').change(function () {
				if (jQuery('#comment_sort select option:selected').val() == 'recent') {
					jQuery("#edit-sort-order").change().val("DESC");
					jQuery("#latest_comment").hide();
					jQuery("#edit-submit-view-comments").click();
				}
				if (jQuery('#comment_sort select option:selected').val() == 'oldest') {
					jQuery("#edit-sort-order").change().val("ASC");
					jQuery("#latest_comment").hide();
					jQuery("#edit-submit-view-comments").click();
				}
				if (jQuery('#comment_sort select option:selected').val() == 'popular') {
					jQuery("#edit-sort-order").change().val("DESC");
					jQuery("#latest_comment").hide();
					jQuery("#edit-submit-view-comments").click();
				}
				if (jQuery('#comment_sort select option:selected').val() == 'shared') {
					jQuery("#edit-sort-order").change().val("ASC");
					jQuery("#latest_comment").hide();
					jQuery("#edit-submit-view-comments").click();
				}
			});
		}
	}

}(jQuery));

/** Set Filter Option to all page load of home page ( Do Discuss Filter Page ). **/
//jQuery(document).ready(function(){
//$("#edit-field-deadline-value-op").change().val("empty");
//$(".views-submit-button input").click();
//});

/** Filter Operation of home page ( Do Discuss Filter Page ). **/
(function ($) {
	Drupal.behaviors.filters = {
		attach: function (context, settings) {

			$(window).load(function () {
				if ($('.block-do-discuss-filter .view-empty').length > 0) {
					// $("#edit-field-deadline-value-op").change().val("<");
					// $("#views-exposed-form-discussion-block-1 .views-operator #edit-field-group-issue-status-value-op").change().val("or");
					// $("#views-exposed-form-discussion-block-1 .views-widget #edit-field-group-issue-status-value").change().val("close");
					// $("#views-exposed-form-poll_list-block .views-widget #edit-active").change().val("0");
					// $(".views-submit-button input").click();
					// $("#close_filter").prop("checked", true);
					$("#close_filter").click();
				}
				else {

					$("#open_filter").prop("checked", true);
					var sector = Drupal.t('All Sectors');
					var newest = Drupal.t('Newest First');
					$(".sector_filter .selectric-wrapper .selectric .label").change().val(sector);
					$("#sort_by .selectric-wrapper .selectric .label").change().val(newest);
					if ($('body.page-home-do').length > 0) {
						var openTask = Drupal.t('Open Tasks Under MyGov');
						if ($("#open_filter").prop("checked")) {
							$("#display_type_changer_wrapper h2").text(openTask);
						}

					}
					if ($('body.page-home-discuss').length > 0) {
						var openDiscussion = Drupal.t('Open Discussions Under MyGov');
						if ($("#open_filter").prop("checked")) {
							$("#display_type_changer_wrapper h2").text(openDiscussion);
						}

					}
					if ($('body.page-home-poll').length > 0) {
						var openPoll = Drupal.t('Open Polls/Survey Under MyGov');
						if ($("#open_filter").prop("checked")) {
							$("#display_type_changer_wrapper h2").text(openPoll);
						}

					}
					if ($('body.page-home-talk').length > 0) {
						var openTalk = Drupal.t('Open Talks Under MyGov');
						if ($("#open_filter").prop("checked")) {
							$("#display_type_changer_wrapper h2").text(openTalk);
						}

					}
				}


			});

			$('.filter_value input').click(function () {
				//if ($(this).attr('checked') !== undefined) {
				if ($(this).val() == 'all') {
					$("#edit-field-deadline-value-op").change().val("empty");
					$("#views-exposed-form-discussion-block-1 .views-operator #edit-field-group-issue-status-value-op").change().val("or");
					$("#views-exposed-form-discussion-block-1 .views-widget #edit-field-group-issue-status-value").change().val("All");
					$("#views-exposed-form-poll_list-block .views-widget #edit-active").change().val("All");
					$(".views-submit-button input").click();
				}
				if ($(this).val() == 'open') {
					$("#edit-field-deadline-value-op").change().val(">");
					$("#views-exposed-form-discussion-block-1 .views-operator #edit-field-group-issue-status-value-op").change().val("or");
					$("#views-exposed-form-discussion-block-1 .views-widget #edit-field-group-issue-status-value").change().val("open");
					$("#views-exposed-form-poll_list-block .views-widget #edit-active").change().val("1");
					$(".views-submit-button input").click();
				}
				if ($(this).val() == 'close') {
					$("#edit-field-deadline-value-op").change().val("<");
					$("#views-exposed-form-discussion-block-1 .views-operator #edit-field-group-issue-status-value-op").change().val("or");
					$("#views-exposed-form-discussion-block-1 .views-widget #edit-field-group-issue-status-value").change().val("close");
					$("#views-exposed-form-poll_list-block .views-widget #edit-active").change().val("0");
					$(".views-submit-button input").click();
				}
				//	}
				if ($('body.page-home-do').length > 0) {
					var allTasks = Drupal.t('All Tasks Under MyGov');
					var openTasks = Drupal.t('Open Tasks Under MyGov');
					var closedTasks = Drupal.t('Closed Tasks Under MyGov');
					if ($(this).val() == 'all') {
						$("#display_type_changer_wrapper h2").text(allTasks);
					}
					if ($(this).val() == 'open') {
						$("#display_type_changer_wrapper h2").text(openTasks);
					}
					if ($(this).val() == 'close') {
						$("#display_type_changer_wrapper h2").text(closedTasks);
					}

				}

				if ($('body.page-home-discuss').length > 0) {
					var allDiscussions = Drupal.t('All Discussions Under MyGov');
					var openDiscussions = Drupal.t('Open Discussions Under MyGov');
					var closedDiscussions = Drupal.t('Closed Discussions Under MyGov');
					if ($(this).val() == 'all') {
						$("#display_type_changer_wrapper h2").text(allDiscussions);
					}
					if ($(this).val() == 'open') {
						$("#display_type_changer_wrapper h2").text(openDiscussions);
					}
					if ($(this).val() == 'close') {
						$("#display_type_changer_wrapper h2").text(closedDiscussions);
					}

				}
				if ($('body.page-home-poll').length > 0) {
					var allPolls = Drupal.t('All Polls/Survey Under MyGov');
					var openPolls = Drupal.t('Open Polls/Survey Under MyGov');
					var closedPolls = Drupal.t('Closed Polls/Survey Under MyGov');
					if ($(this).val() == 'all') {
						$("#display_type_changer_wrapper h2").text(allPolls);
					}
					if ($(this).val() == 'open') {
						$("#display_type_changer_wrapper h2").text(openPolls);
					}
					if ($(this).val() == 'close') {
						$("#display_type_changer_wrapper h2").text(closedPolls);
					}

				}
				if ($('body.page-home-talk').length > 0) {
					var allTalks = Drupal.t('All Talks  Under MyGov');
					var openTalks = Drupal.t('Open Talks Under MyGov');
					var closedTalks = Drupal.t('Closed Talks Under MyGov');
					if ($(this).val() == 'all') {
						$("#display_type_changer_wrapper h2").text(allTalks);
					}
					if ($(this).val() == 'open') {
						$("#display_type_changer_wrapper h2").text(openTalks);
					}
					if ($(this).val() == 'close') {
						$("#display_type_changer_wrapper h2").text(closedTalks);
					}

				}

			});


		}
	}

}(jQuery));

/** Search Trigger after a word in home page ( Do Discuss Filter Page ). **/
(function ($) {
	Drupal.behaviors.search_trigger = {
		attach: function (context, settings) {
			if ($('#edit-field-hashtags-tid').val()) {
				var resetLabel = Drupal.t('Reset');
				$('.reset_view').replaceWith("<span class='reset_view'>" + resetLabel + "</span>");
			}
			else {
				$('.reset_view').hide();
			}

			$('.reset_view').click(function (e) {
				$('.form-item-field-hashtags-tid input').val("");
				$(".views-submit-button input").click();
			});

			$('#edit_search_btn').click(function (e) {
				var text_search = jQuery('#edit_search').val();
				if (jQuery(this).hasClass("search_mygov")) {
					var type = jQuery("#search_type").val();
					if (type == "") {
						type = "All";
					}
					var url = jQuery("#search_url").val();
					window.location = url + "?title=" + text_search + "&type=" + type;
					return false;
				}
				var n = text_search.indexOf("#");
				var hash_text = text_search;
				if (n != 0 && $.trim(text_search) != "") {
					hash_text = '#' + text_search;
				}
				$('.form-item-field-hashtags-tid input').val(hash_text);
				$('#edit-title').val(text_search);
				$('#t_keyword').html(text_search);
				$(".views-submit-button input").click();
			});
			$('.the_box #search_title').keyup(function (e) {
				var key = e.which;
				if (key == 13) {
					$('a#search_link_btn')[0].click();
				}
			});

			$('#search_link_btn').click(function (e) {
				var searchValue = jQuery(".search_title_box").val();
				window.location = '/search?title='+searchValue+'&type=All';				
			});

			$('#edit_reset_btn').click(function (e) {
				if (jQuery(this).hasClass("reset_search_mygov")) {
					var url = jQuery("#search_url").val();
					window.location = url + "?title=&type=All";
					return false;
				}
				$('#edit-title').val("");
				$('#edit-type').val("All");
				$("#edit-sort-by").change().val("created");
				$("#edit-sort-order").change().val("DESC");
				$(".views-submit-button input").click();
			});

			$('#edit_search').keyup(function (e) {
				if (e.keyCode == 13) {
					var text_search = jQuery('#edit_search').val();
					if (jQuery(this).hasClass("search_mygov")) {
						var type = jQuery("#search_type").val();
						if (type == "") {
							type = "All";
						}
						var url = jQuery("#search_url").val();
						window.location = url + "?title=" + text_search + "&type=" + type;
						return false;
					}
					var n = text_search.indexOf("#");
					var hash_text = text_search;
					if (n != 0 && $.trim(text_search) != "") {
						hash_text = '#' + text_search;
					}
					$('.form-item-field-hashtags-tid input').val(hash_text);
					$('#edit-title').val(text_search);
					$(".views-submit-button input").click();
				}
			});
			$('a.hashtag_comments').click(function (e) {
				var text_search = jQuery(this).attr('data');
				var n = text_search.indexOf("#");
				var hash_text = text_search;
				if (n != 0 && $.trim(text_search) != "") {
					hash_text = '#' + text_search;
				}
				$('.form-item-field-hashtags-tid input').val(hash_text);
				$('#edit-title').val(text_search);
				$(".views-submit-button input").click();
				return false;
			});
		}
	}

}(jQuery));

/** Sort order switch of home page ( Do Discuss Filter Page ). **/
(function ($) {
	Drupal.behaviors.do_discuss_filter_sort_by = {
		attach: function (context, settings) {
			$('#sort_by select').change(function () {
				if (jQuery('#sort_by select option:selected').val() == 'recent') {
					jQuery("#edit-sort-by").change().val("created");
					jQuery("#edit-sort-order").change().val("DESC");
					jQuery(".views-submit-button input").click();
				}
				if (jQuery('#sort_by select option:selected').val() == 'oldest') {
					jQuery("#edit-sort-by").change().val("created");
					jQuery("#edit-sort-order").change().val("ASC");
					jQuery(".views-submit-button input").click();
				}
				if (jQuery('#sort_by select option:selected').val() == 'deadline') {
					jQuery("#edit-sort-by").change().val("field_deadline_value");
					jQuery("#edit-sort-order").change().val("DESC");
					jQuery(".views-submit-button input").click();
				}
				if (jQuery('#sort_by select option:selected').val() == 'popular') {
					jQuery("#edit-sort-by").change().val("comment_count");
					jQuery("#edit-sort-order").change().val("DESC");
					jQuery(".views-submit-button input").click();
				}
				if (jQuery('#sort_by select option:selected').val() == 'shared') {
					jQuery("#edit-sort-order").change().val("ASC");
					jQuery(".views-submit-button input").click();
				}
			});
		}
	}

}(jQuery));

/** Sector Filter switch of home page ( Do Discuss Filter Page ). **/
(function ($) {
	Drupal.behaviors.do_discuss_filter_sector = {
		attach: function (context, settings) {
			$('#sector_select').change(function () {
				var sec_val = jQuery('#sector_select option:selected').val();
				jQuery("#edit-field-sectors-tid-op").change().val("or");
				jQuery("#edit-field-sectors-tid").change().val(sec_val);
				jQuery(".views-submit-button input").click();
			});
		}
	}
}(jQuery));

/** Link to us Page Image Positioning Script **/
(function ($) {
	Drupal.behaviors.link_to_us_page_script = {
		attach: function (context, settings) {
			var $container = $('#bannerHolder');

			$container.imagesLoaded(function () {
				$container.masonry({
					itemSelector: '.linkto-us-box'
				});
			});

		}
	}

}(jQuery));

/** Refresh Page after clicking DO button on a Task. **/
(function ($) {
	Drupal.behaviors.flag_link_update = {
		attach: function (context, settings) {
			/*if ($("#submission_type").find("a.unflag-action").length > 0) {
				jQuery("#team_area").show();
			}
			if ($("#submission_type").find(".unflag-disabled").length > 0) {
				jQuery("#team_area").show();
			}*/
			/*if ($(".invitation_wrapper .flag-reject-invitation").find(".flag.unflag-disabled").length > 0) {
				jQuery(".flag-accept-invitation").hide();
			}*/
			$(document).bind('flagGlobalAfterLinkUpdate', function (event, data) {
				if (data.flagName == 'do') {
					window.location.reload(true);
				}

				if (data.flagName == 'reject_invitation' && data.flagStatus == 'flagged') {
					var id = "#invitee_" + data.contentId;
					jQuery(id + " .flag-accept-invitation").hide();
				}
				if (data.flagName == 'reject_invitation' && data.flagStatus == 'unflagged') {
					var id = "#invitee_" + data.contentId;
					jQuery(id + " .flag-accept-invitation").show();
				}

				if (data.flagName == 'accept_invitation' && data.flagStatus == 'flagged') {
					var id = "#invitee_" + data.contentId;
					jQuery(id + " .flag-reject-invitation").remove();
					jQuery(".flag-reject-invitation a").click();
				}

				/*if(data.flagName == 'submission_type' && data.flagStatus == 'flagged') {
					jQuery("#team_area").show();
				}
				if(data.flagName == 'submission_type' && data.flagStatus == 'unflagged') {
					jQuery("#team_area").hide();
				}*/

			});
		}
	}

}(jQuery));


/** Check availability of Team Name **/
(function ($) {
	Drupal.behaviors.team_name_check = {
		attach: function (context, settings) {
			jQuery('#ief-entity-table-edit-field-invitees-und-entities tbody .form-item.form-type-select').parent().hide();
			jQuery("#team-node-form #edit-title-field input").blur(function () {
				var team_name = encodeURIComponent(jQuery(this).val());
				if (team_name == "") {
					team_name = "null";
				}
				jQuery("#name_warning").load("/check_team_name/" + team_name);
				jQuery("#name_warning").show();
				setInterval(function () {
					jQuery("#name_warning").hide();
				}, 6000);
			});
		}
	}
}(jQuery));

/** Adds Class to input submit button after invitee added in team node form. **/
(function ($) {
	Drupal.behaviors.add_class_input = {
		attach: function (context, settings) {
			if (jQuery(".field-name-field-invitees .fieldset-wrapper").find(".ief-entity-table").length > 0) {
				jQuery('body.page-node-add-team #team-node-form #edit-field-invitees-und-actions input[type="submit"]').addClass("once_add_invitee");
			}
		}
	}
}(jQuery));

/** Adds active link to group page sorting filters. **/
(function ($) {
	Drupal.behaviors.change_groups_sort_select = {
		attach: function (context, settings) {
			if (typeof $('#group_sort').attr('id') != 'undefined') {
				if (($('#edit-sort-by option:selected').val()) == 'title') {
					$('#group_sort select option')[0].selected = true;
				}

				if (($('#edit-sort-by option:selected').val()) == 'created' && ($('#edit-sort-order option:selected').val()) == 'DESC') {
					$('#group_sort select option')[1].selected = true;
				}
				if (($('#edit-sort-by option:selected').val()) == 'created' && ($('#edit-sort-order option:selected').val()) == 'ASC') {
					$('#group_sort select option')[2].selected = true;
				}
			}

		}
	}
}(jQuery));

/** Remove anchor from inactive links from content detail nav bar. **/
(function ($) {
	Drupal.behaviors.remove_inactive_href = {
		attach: function (context, settings) {
			jQuery('#activities a.inactive').removeAttr('href');
		}
	}
}(jQuery));

/** Add image and video in comments by clicking icons. **/
(function ($) {
	Drupal.behaviors.add_image_btn = {
		attach: function (context, settings) {
			//var md = new MobileDetect(window.navigator.userAgent);
			//if (md.mobile() == null && md.phone() == null && md.tablet() == null) {
			jQuery('.field-name-field-gi-comment-file .form-managed-file .form-file').addClass('element-invisible');
			jQuery('.field-name-field-gi-comment-file fieldset').css('border', 'none');
			jQuery('.field-name-field-gi-comment-file legend').css('display', 'none');
			jQuery('.field-name-field-comment-file .form-managed-file .form-file').addClass('element-invisible');
			jQuery('.field-name-field-comment-file fieldset').css('border', 'none');
			//jQuery('.field-name-field-comment-file legend').css('display', 'none');
			//} else {
			//if (md.mobile()) {
			//    			jQuery('.field-name-field-add-image-gi').addClass('element-invisible');
			//    			jQuery('.field-name-field-add-image-gi').hide();
			//    		}
			//    		if (md.phone()) {
			//    			jQuery('.field-name-field-add-image-gi').hide();
			//    			jQuery('.field-name-field-add-image-gi').addClass('element-invisible');
			//    		}
			//    		if (md.tablet()) {
			//    			jQuery('.field-name-field-add-image-gi').hide();
			//    			jQuery('.field-name-field-add-image-gi').addClass('element-invisible');
			//    		}
			//    	}
			jQuery('.comment_body_wrapper div.field-name-field-hashtags').hide();
			// jQuery('.comment_body_wrapper div.field-name-field-video').hide();

			jQuery('#add_image').once("add_image_btn", function () {
				jQuery(this).click(function () {
					jQuery('.field-name-field-gi-comment-file input.form-file').click();
				});
			});

			jQuery('#add_image_task', context).off('click').click(function () {
				jQuery('.field-name-field-comment-file .form-type-managed-file input.form-file').click();
			});
		}
	}
}(jQuery));


/** Add youtube video in comments by clicking icons. **/
(function ($) {
	Drupal.behaviors.youtube_vid = {
		attach: function (context, settings) {
			jQuery('#add_youtube').once("youtube_vid", function () {
				jQuery(this).click(function () {
					jQuery('.comment_body_wrapper div.field-name-field-video').toggle();
				});
			});


		}
	}
}(jQuery));

/** Check for IE version **/
function msieversion() {
	var ua = window.navigator.userAgent
	var msie = ua.indexOf("MSIE ")

	if (msie > 0)      // If Internet Explorer, return version number
		return parseInt(ua.substring(msie + 5, ua.indexOf(".", msie)))
	else                 // If another browser, return 0
		return 0

}

/** Show content of details page after clicking See Deatils. **/
(function ($) {
	Drupal.behaviors.hide_submit_post_button = {
		attach: function (context, settings) {
             
			// jQuery('.node.group-issue .detail_top').hide();
			// jQuery('.node.task .detail_top').hide();
			jQuery('#see_details .collapse').hide();
			jQuery('#see_details .expand').show();
			jQuery('#see_details .expand').click(function () {
				jQuery('.node-details').slideDown('slow');
				jQuery('#see_details .collapse').show();
				jQuery('#see_details .expand').hide();
				jQuery('.short_description').hide();
			});
			jQuery('#see_details .collapse').click(function () {
				jQuery('.node-details').hide();
				jQuery('#see_details .expand').show();
				jQuery('.short_description').slideDown('slow');
				jQuery('#see_details .collapse').hide();
			});

		}
	}
}(jQuery));

/** Show Share Links in comment on button click. **/
(function ($) {
	Drupal.behaviors.show_share_links = {
		attach: function (context, settings) {
			var sharelink = Drupal.t('Share');

			jQuery(".share_links").css('width', '30px');
			//jQuery(".share_links").hide();
			jQuery(".share_btn").html(sharelink);
			jQuery(".share_btn", context).click(function () {
				// jQuery(this).next('div.share_links').toggle();
			});
   
		}
	}
}(jQuery));

/** Slide Down comment box like twitter. **/
(function ($) {
	Drupal.behaviors.slide_down_comment_box = {
		attach: function (context, settings) {
			if (!jQuery('.comment_body_wrapper').hasClass('once_processed')) {
				jQuery('.comment_body_wrapper').hide();
			}
			jQuery('#comments form label').hide();
			jQuery('.logged-in .submit_comment_button').click(function () {
				jQuery('.bottom_nav_wrapper .links_wrapper').remove();
				jQuery('.comment_body_wrapper').animate({ height: 'show' });
				jQuery('.comment_body_wrapper').addClass('once_processed');
			});
		}
	}
}(jQuery));

/** Display type changer. GRID and LIST view of home page blocks. **/
(function ($) {
	Drupal.behaviors.display_type_changer = {
		attach: function (context, settings) {
			jQuery('#display_type_changer a.grid').click(function () {
				jQuery('#-do-discuss-filter-output-wrapper').addClass('grid');
				jQuery('.page-groups #block-system-main').addClass('grid');
				jQuery('#-do-discuss-filter-output-wrapper').removeClass('list');
				jQuery('.page-groups #block-system-main').removeClass('list');
				jQuery('#display_type_changer a.grid').addClass('active');
				jQuery('#display_type_changer a.list').removeClass('active');
			});
			jQuery('#display_type_changer a.list').click(function () {
				jQuery('#-do-discuss-filter-output-wrapper').addClass('list');
				jQuery('.page-groups #block-system-main').addClass('list');
				jQuery('#-do-discuss-filter-output-wrapper').removeClass('grid');
				jQuery('.page-groups #block-system-main').removeClass('grid');
				jQuery('#display_type_changer a.grid').removeClass('active');
				jQuery('#display_type_changer a.list').addClass('active');
			});

			// gigw keyboard show detail
	jQuery(".description_wrapper .title a").on('keyup', function(e) { 
		var keyCode = e.keyCode || e.which; 

		if (keyCode == 9) { 
			jQuery(this).parents('.views-row').find('.caption_btn').show();
			jQuery(this).parents('.views-row').find('.blog_url').show();
			
		} 
	  });

	 

	//   jQuery(".caption_btn a").on('keydown', function(e) { 
	// 	var keyCode = e.keyCode || e.which; 

	// 	if (keyCode == 9) { 
	// 		jQuery(this).parent('.caption_btn').hide();
	// 	} 
	//   });

		}
	}
}(jQuery));

/*Referal Code SMS and mail form toggle*/
(function ($) {
	Drupal.behaviors.ref_forms = {
		attach: function (context, settings) {
			$('.sms_ref', context).click(
				function () {
					jQuery('.sms_form ').removeClass('element-invisible');
					jQuery('.email_form ').addClass('element-invisible');
				});
			$('.email_ref', context).click(
				function () {
					jQuery('.sms_form ').addClass('element-invisible');
					jQuery('.email_form ').removeClass('element-invisible');
				});
			$('#sms_send').click(function () {
				if (!$(this).hasClass('mygov-referal-processed-once')) {
					var nums = $('#sms_num').val();
					var base = $(this).attr('id');
					var code = $(this).attr('data-code');

					var element_settings = {
						url: '/referal_share/' + nums + '/' + code + '/sms',
						event: 'ref_sms_send',
					};

					Drupal.ajax[base] = new Drupal.ajax(base,
						this, element_settings);
					$(this).trigger('ref_sms_send');
					$(this).addClass('mygov-referal-processed-once');
				}
				return false;
			});

			$('#email_send').click(function () {
				if (!$(this).hasClass('mygov-referal-processed-once')) {
					var emails = $('#email_id').val();
					var base = $(this).attr('id');
					var code = $(this).attr('data-code');

					var element_settings = {
						url: '/referal_share/' + emails + '/' + code + '/email',
						event: 'ref_email_send',
					};

					Drupal.ajax[base] = new Drupal.ajax(base,
						this, element_settings);
					$(this).trigger('ref_email_send');
					$(this).addClass('mygov-referal-processed-once');
				}
				return false;
			});

		}
	};
}(jQuery));

/** chandra  **/
(function ($) {
	Drupal.behaviors.covidadvisary = {
		attach: function (context, settings) {
	jQuery(document).ajaxComplete(function () {
	
	jQuery('.covid .view-covid-states-advisory .view-content').each(function(){
	var $pArr = jQuery(this).find('.views-row ');
	var pArrLen = $pArr.length;
	if ( $pArr.parent().hasClass( 'state_book' ) ) {
		    $pArr.unwrap();
		}
  if(jQuery(window).width() > 767){
    var pPerDiv = 10;
	for (var i = 0;i < pArrLen;i+=pPerDiv){
		$pArr.filter(':eq('+i+'),:lt('+(i+pPerDiv)+'):gt('+i+')').wrapAll('<div class="state_book" />');
	}
	
	jQuery('.covid .view-covid-states-advisory .view-content').addClass('owl-carousel');
	  jQuery(this).owlCarousel({
		  loop:false,
		  nav:true,
		  margin:10,
		  responsiveClass:true,
		  dots:false,
		  navText : ["Previous","Next"],
		  responsive:{
			  0:{
				  items: 1
			  }
		  }
		  
	  });
  }
  else{
    var pPerDiv = 2;
	 for (var i = 0;i < pArrLen;i+=pPerDiv){
		$pArr.filter(':eq('+i+'),:lt('+(i+pPerDiv)+'):gt('+i+')').wrapAll('<div class="state_book" />');
	}
		jQuery(this).addClass('owl-carousel');
	  jQuery(this).owlCarousel({
		  loop:false,
		  nav:true,
		  margin:10,
		  responsiveClass:true,
		  navText : ["Previous","Next"],
		  responsive:{
			  0:{
				  items: 1
			  }
		  }
		  
	  });	  
	  }
	})
	})
		}}
		

}(jQuery));

document.addEventListener('play', function(e){
    var audios = document.getElementsByTagName('audio');
    for(var i = 0, len = audios.length; i < len;i++){
        if(audios[i] != e.target){
            audios[i].pause();
        }
    }
}, true);

jQuery(document).ready(function($) {
	  // Handler for .ready() called.
		jQuery( ".covid-lang #lang" ).change(function() {
			var targetUrl = '/covid-19-language/?lang='+jQuery(this).val();
			if(jQuery(this).val() == 'hi' || jQuery(this).val() == '' || jQuery(this).val() == 'en'){
				var targetUrl = '/'+jQuery(this).val()+'/covid-19/';
			}
		  window.open(targetUrl, "_SELF" );
		});
		
		/*jQuery( ".covid-lang-anuvadak #lang" ).change(function() {
			if(jQuery( ".covid-lang-anuvadak #lang" ).val() == 'en'){
				var targetUrl = '/covid-19/';
				window.open(targetUrl, "_BLANK" );
			}else if(jQuery( ".covid-lang-anuvadak #lang" ).val() == 'hi'){
				var targetUrl = '/hi/covid-19/';
				window.open(targetUrl, "_BLANK" );
			}else{
				var targetUrl = '/covid-19/'+jQuery(this).val();
				//if(jQuery(this).val() == 'hi' || jQuery(this).val() == '' || jQuery(this).val() == 'en'){
					//var targetUrl = '/'+jQuery(this).val()+'/covid-19/';
				//}/
			  window.open(targetUrl, "_BLANK" );
			}
		});*/
		jQuery(".page-node-291871 #page-title").text(jQuery("#titleCovid").text()); // Production Covid Language
		jQuery(".page-node-86545 #page-title").text(jQuery("#titleCovid").text());// Staging Covid Language

	});
//Added for accordian in simple pages
(function ($) {
	Drupal.behaviors.accordian_pmay = {
		attach: function (context, settings) {
			if (jQuery('.accordian-block').length > 0) {
				var acc = document.getElementsByClassName("accordion");
				var i;
				for (i = 0; i < acc.length; i++) {
				  acc[i].addEventListener("click", function() {
				  	this.classList.toggle("active");
				    var parent = this.parentElement;
				    var panel = parent.nextElementSibling;
				    if (panel.style.maxHeight){
				      panel.style.maxHeight = null;
				    } else {
				      panel.style.maxHeight = panel.scrollHeight + "px";
				    }
				  });
				}
			}
		}
	}
}(jQuery));


/*
window.onbeforeunload = function (e) {
    e = e || window.event;

    // For IE and Firefox prior to version 4
    if (e) {
        e.returnValue = 'Sure?';
    }

    // For Safari
    return 'Sure?';
};*/




function state_advisory(){
	var stateid = '';
	
	if(jQuery("#advisory-states").val() == 'All' || jQuery("#advisory-states").val() === undefined ){
			var state = '35';
		}else{			
			var state = jQuery("#advisory-states").val();
		}
		stateid = '&state_id='+state;
		var catStr = '';
		var category = jQuery("#advisory-category").val();
		if(jQuery("#advisory-category").val() == 'All' || jQuery("#advisory-category").val() === undefined ){
			category = 'All';
		}else{
			category = jQuery("#advisory-category").val();
			var catStr = '&category_id='+jQuery("#advisory-category").val();
		}
		var curUrl = window.location.href;
		var curUrlArray = curUrl.split("/");
		var srchKey = '';
		var stateStr = '';
		var advCat = '';
		var title = '';
		/*if(!jQuery("#advisory-title").val() === undefined){
			title = jQuery("#advisory-title").val();
		}*/
		if(curUrlArray[3] == 'hi'){
			var gatData = "/hi/vaccine-state-advisory?title="+jQuery("#advisory-title").val()+"&states="+jQuery("#advisory-states").val()+"&category="+jQuery("#advisory-category").val();
				var srchKey = 'कीवर्ड से खोजें';
        var stateStr = 'राज्य';
        var advCat = 'सलाहकार श्रेणी';
        var apply = "खोजें";
        var noRecord = "कोई सूचना मौजूद नहीं है।";
		}else{
			var gatData = "/vaccine-state-advisory?title="+jQuery("#advisory-title").val()+"&states="+jQuery("#advisory-states").val()+"&category="+jQuery("#advisory-category").val();
				var srchKey = 'Search by keyword';
        var stateStr = 'States';
        var advCat = 'Advisory Category';
        var apply = "Apply";
        var noRecord = "No advisory found!";
		}
		var gatData = "https://api.mygov.in/covid-advisory/?api_key=57076294a5e2ab7fe000000112c9e964291444e07dc276e0bca2e54b"+stateid+catStr;
		var str = '<div class="state-covid-advisory"><divi class="view-covid-states-advisory view-id-covid_states_advisory"><div class="view-filters"> <div><div class="views-exposed-form"> <div class="views-exposed-widgets clearfix"><!--div id="edit-title-wrapper" class="views-exposed-widget views-widget-filter-title"> <label for="edit-title"> '+srchKey+'          </label><div class="views-widget"> <div class="form-item form-type-textfield form-item-title"> <input autocomplete="off" type="text" id="advisory-title" name="title" value="'+title+'" size="30" maxlength="128" class="form-text" title=""></div> </div> </div--> <div id="edit-field-advisory-states-value-wrapper" class="views-exposed-widget views-widget-filter-field_advisory_states_value"><label for="edit-field-advisory-states-value">'+stateStr+' </label> <div class="views-widget"> <div class="form-item form-type-select form-item-field-advisory-states-value"> <select id="advisory-states" name="field_advisory_states_value" class="form-select"><option value="35">Andaman and Nicobar Islands</option><option value="28">Andhra Pradesh</option><option value="12">Arunachal Pradesh</option><option value="18">Assam</option><option value="10">Bihar</option><option value="4">Chandigarh</option><option value="22">Chhattisgarh</option><option value="26">Dadra and Nagar Haveli and Daman and Diu</option><option value="7">Delhi</option><option value="30">Goa</option><option value="24">Gujarat</option><option value="6">Haryana</option><option value="2">Himachal Pradesh</option><option value="1">Jammu and Kashmir</option><option value="20">Jharkhand</option><option value="29">Karnataka</option><option value="32">Kerala</option><option value="37">Ladakh</option><option value="31">Lakshadweep</option><option value="23">Madhya Pradesh</option><option value="27">Maharashtra</option><option value="14">Manipur</option><option value="17">Meghalaya</option><option value="15">Mizoram</option><option value="13">Nagaland</option><option value="21">Odisha</option><option value="34">Puducherry</option><option value="3">Punjab</option><option value="8">Rajasthan</option><option value="11">Sikkim</option><option value="33">Tamil Nadu</option><option value="36">Telangana</option><option value="16">Tripura</option><option value="9">Uttar Pradesh</option><option value="5">Uttarakhand</option><option value="19">West Bengal</option></select></div> </div></div><div id="edit-field-advisory-category-tid-wrapper" class="views-exposed-widget views-widget-filter-field_advisory_category_tid"> <label for="advisory-category-tid"> '+advCat+' </label><div class="views-widget"> <div class="form-item form-type-select form-item-field-advisory-category-tid"> <select id="advisory-category" name="field_advisory_category_tid" class="form-select"><option value="All" selected="selected">- Any -</option><option value="352101">For Citizens</option><option value="352121">Travel Advisories</option><option value="356171">Training Material</option><option value="352541">Lockdown</option><option value="365121">Civil Aviation Advisories</option><option value="356161">Behavioural Health</option><option value="352151">For Employees</option><option value="352131">For Hospitals</option><option value="361011">Inspirational series on Healthcare</option><option value="352161">For States/Departments/Ministries</option><option value="352141">Awareness Material</option></select></div> </div> </div><div class="views-exposed-widget views-submit-button"> <input type="submit" id="edit-submit-covid-states-advisory" value="'+apply+'" class="form-submit" title="'+apply+'" onclick="state_advisory()">    </div> </div></div></div>    </div><div class="view-content owl-carousel owl-loaded owl-drag">';
   // alert("state_advisory");
    jQuery("#info-2 img.loader").show();
    jQuery("#info-2 .owl-stage-outer").html('');
		jQuery.ajax({
        type: 'GET',
        url: gatData,
        dataType: 'json',
        success: function(response) { 
        	var res = response['notification_data'];
        	//alert(res.length); 
        	
        	for(var i = 0;  i < res.length; i++){
        		 str += '<div class="views-row views-row-1 views-row-odd views-row-first"><div class="views-field views-field-field-advisory-date"> <div class="field-content">  <span class="date-display-single">'+res[i]['notification_date']+'</span> </div>  </div> <div class="views-field views-field-nothing"> <span class="field-content"><a href="'+res[i]['link']+'" target="_blank">'+res[i]['notification_title']+'</a></span>   </div> </div>';
        	}
        	str += '</div></div>';
           jQuery(".stade_advisory").html(str);
           jQuery("#info-2 img.loader").hide();  
           jQuery("#advisory-states").val(state);
           jQuery("#advisory-category").val(category);
        },
        error: function() {
        	jQuery("#info-2 img.loader").hide();
        },
        complete: function() {
        	jQuery("#info-2 img.loader").hide();
        }
    });
}
(function ($) {
	Drupal.behaviors.ajax = { 
    attach: function(context) {
	    jQuery('a[href^=http]').once().click(function(e){
	      var curUrl = window.location.href;
	      var curUrlArray = curUrl.split("/");
	      if(curUrlArray[2] == "blog.mygov.in" || curUrlArray[2] == "quiz.mygov.in"){ 
	      }else{                       
	          var url=jQuery(this).attr('href');                    
	          var target=jQuery(this).attr('target'); 
	          var urlArray = url.split("/");
	          var urlSpArr = urlArray[2].split(".");
	          if(urlArray[2] == curUrlArray[2]){ 
	          }else{
              e.preventDefault(); 
              var baseDomn = urlSpArr[urlSpArr.length-2]+'.'+urlSpArr[urlSpArr.length-1];                
	            if( urlArray[2] == "wwww.mygov.in"  || urlArray[2] == "mygov.in"  || urlArray[2] == "auth.mygov.in"  || urlArray[2] == "secure.mygov.in" ||  urlArray[2] == curUrlArray[2]){
	                window.location.href=url;
	            }else if(baseDomn == "mygov.in"){
                if(urlArray[4] == "login" ||  urlArray[4] == "register" ){
                   window.location.href=url;
                }else{
                     window.open(url, '_blank');
                }
              }else{
                if(jQuery("body").hasClass("i18n-hi")){
                    var str = "आपको एक बाहरी वेबसाइट पर रीडायरेक्ट किया जा रहा है। कृपया ध्यान दें कि माईगव बाहरी वेबसाइट के कंटेंट और गोपनीयता नीतियों के लिए ज़िम्मेदार नहीं है.";
                }else{
                    var str = "You are being redirected to an external website. Please note that MyGov Website cannot be held responsible for external websites content & privacy policies.";
                }                   
                if (confirm(str)) {
                  if(target=='_blank')
                    window.open(url, '_blank');
                  else
                     window.location.href=url;
                }
	          	}
	              
	          }
	      }
	  	});  
    }
	}
}(jQuery));

//Get vaccine live counts
/*function numberWithCommas(x) {
  var parts = new Intl.NumberFormat('en-IN', { maximumSignificantDigits: 15 }).format(x);
  return parts;
}

setInterval(vaccineTimer, 10000);
function vaccineTimer() {
jQuery.getJSON('https://cdn-api.co-vin.in/api/v1/reports/getLiveVaccination', function(data) {	
	var vaccineCount = numberWithCommas(data.count);
	//var text = `Count: ${data.count}`
	//console.log(vaccineCount);
	jQuery(".vaccine-live-count").html(vaccineCount);
});
}*/

//Remove like/dislike/reply for closed activity
(function ($) {
  Drupal.behaviors.closed_link_remove = {
	attach: function (context, settings) {
	  if (jQuery('.closed_task').length > 0) {
	    $('.comment_extra_links .voting_wrap').remove();
	    $('.comment_extra_links .links_wrapper').remove();
	    $('.comment_extra_links .spam_wrapper').remove();
	    //$('.comment_extra_links .feature_wrapper').remove();
	  }
	}
  }
}(jQuery));