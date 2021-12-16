Drupal.behaviors.commonUtilityAnchor = {
	attach: function (context) {
		/* Find img tag in the site and add the alt tag by title name - starts */
		
		jQuery("a").each(function() {
			var images = jQuery(this).find('img');
			/* 
			 * * Code for the <img alt> where <img alt> is not available
			 * if <img> is the child element of <a> , then <a title> will be <img alt> if <img alt=""> */
			
			if (images.length) {
				jQuery(images).each(function() {
					var $parent = jQuery(this).parent();
					  
				  if((jQuery(this).attr('alt') == null || jQuery(this).attr('alt') == '') && $parent.attr('title') != '') {
					  jQuery(this).attr('alt', $parent.attr('title'));
					  
					  if(jQuery(this).attr('title') == $parent.attr('title')) {
						jQuery(this).attr('title', "") ;
					  }
				  }
				});	
			}
			
			/* 
			 * Code for the <a title> where <a title> is not available
			 * <a>value</a>  - code for anchor title */
			
			else {
				
				  if((jQuery(this).attr('title') == null || jQuery(this).attr('title') == '')){
					  
					  /* var anchorvalue = jQuery(this).text().replace(/\s+/g, ' '); */
					  
					  var anchorvalue = jQuery(this).text().replace(/\s+/g, ' ');
	
					 
	
					  if(jQuery(this).hasClass('ext')) {
						  anchorvalue += Drupal.t(' (External Site that opens in a new window)');
						  jQuery(this).attr('title' , anchorvalue);
						  jQuery(this).attr('target', "_blank");
					  }
					  else {
						  jQuery(this).attr('title', anchorvalue);
					  }
				  }
			}
		 });
		
		/* 
		 * Code for the <input> where <input title> is not available
		 * <input value=""> will be <input title="">  - code for input title attribute */
		
		jQuery("input").each(function() { 
			
			if((jQuery(this).attr('title') == null)  || (jQuery(this).attr('title') == '' )) {
				
				 var anchorvalue = jQuery(this).val();
				  jQuery(this).attr('title', anchorvalue);
			}
		});
		
		/* Find img tag in the site and add the alt tag by title name - Ends */

		/*
		* Test for campaign dashboard json data
		*/
		
		jQuery(document).ready(function () {
			jQuery("select#state option").each(function(){
			  if (jQuery(this).val() == profileState)
			    jQuery(this).attr("selected","selected");
			});
			jQuery("select#district option").each(function(){
			  if (jQuery(this).val() == profileDistrict)
			    jQuery(this).attr("selected","selected");
			});
			var pathposhan_en = window.location.pathname.substr(1, 24);
			var pathposhan_hi = window.location.pathname.substr(1, 27);
			if((pathposhan_en == 'campaigns/poshanabhiyaan') || (pathposhan_hi == 'hi/campaigns/poshanabhiyaan')){
				jQuery.getJSON('/sites/default/files/campaign/poshan.json')
				.done(function(poshan_data) {
					//console.log(poshan_data);
					var totalActivityCount = numberWithComma(poshan_data.data.total.totalActivityCount);
					var adultFemaleCount = numberWithComma(poshan_data.data.total.adultFemaleCount);
					var adultMaleCount = numberWithComma(poshan_data.data.total.adultMaleCount);
					var childrenFemaleCount = numberWithComma(poshan_data.data.total.childrenFemaleCount);
					var childrenMaleCount = numberWithComma(poshan_data.data.total.childrenMaleCount);
					
					jQuery(".total-count").html(totalActivityCount);
					jQuery(".adult-female-count").html(adultFemaleCount);
					jQuery(".adult-male-count").html(adultMaleCount);
					jQuery(".child-female-count").html(childrenFemaleCount);
					jQuery(".child-male-count").html(childrenMaleCount);
					
					
				})
				.fail(function() {
					console.log("ERROR: Poshan url not responding.");
				});
			}

			var pathname_en = window.location.pathname.substr(1, 20);
			var pathname_hi = window.location.pathname.substr(1, 23);
			if((pathname_en == 'campaigns/pmay-urban') || (pathname_hi == 'hi/campaigns/pmay-urban')){
			//jQuery.getJSON('https://pmaymis.gov.in/api/PMAY_Services/MYGOV_Dashboard_Data')
			jQuery.getJSON('/sites/default/files/campaign/pmay.json')
				.done(function(pmay_data) {
				var houseCompleted = pmay_data[0].Value[0].House_Completed;
				var houseGrounded = pmay_data[0].Value[0].House_Grounded;
				var sanctioned = pmay_data[0].Value[0].Houses_Sanctioned;
				jQuery(".sanctioned-number").html(sanctioned);
				jQuery(".grounded-number").html(houseGrounded);
				jQuery(".completed-number").html(houseCompleted);
			})
				.fail(function() {
					console.log("ERROR: PMAY url not responding.");
				});
			}
		});
		
		//End campaign dashboard json data

		//Start popup-profile-form code
		jQuery("select#state").change(function(){
			//alert("select state");
		 	jQuery("#profile-popup-form #edit-submit").attr("disabled","disabled");
			//var st_val = jQuery('#state option:selected').val();
			var selectedState = jQuery(this).children("option:selected").val();
		  	if(!selectedState){
			 jQuery("#district").html('<select id="district" placeholder="district" name="district" class="form-select required"><option value="" selected="selected">- Select district -</option></select>');
			}
			formValidation();
			//console.log(selectedState);
			if(selectedState){
			  jQuery.ajax({
				url: "/get-districts",
				type: "POST",
				data: {
				  state_id : selectedState,
				},
				dataType: "json",
				success: function(data) {
				  var html = [];
				  var selectDist = Drupal.t('- Select district -');
				  html.push('<select id="district" placeholder="district" name="district" class="form-select required">');
				  html.push('<option value="" selected="selected">'+selectDist+'</option>');
				  jQuery.each(data, function(index, district) {
					html.push('<option value="'+district.tid+'">'+district.name+'</option>');
				  })
				  html.push('</select>'); 
				  if(selectedState != ''){
					jQuery("#district").html(html.join(''));
				  } else {
				    console.log('something went wrong with district select.');	
				  }	
				  formValidation();			  
				}
			  });
			}
			
	 	});

	 	jQuery("#pincode").change(function(){
			//alert("select state");
		 	formValidation();
			var pincode = jQuery("#pincode").val();
		  	if(!pincode){
			 jQuery("#city").html('<input id="city" placeholder="City" type="text" name="city" value="" size="60" maxlength="128" class="form-text required" title="">');
			}
			//console.log(pincode);
			if(pincode){
			  jQuery.ajax({
				url: "/get-city-by-pin/"+pincode,
				type: "GET",
				dataType: "json",
				success: function(data) {
				  console.log(data.data);
				  var city_name = data.data.City;
				  var stateName = data.data.statename;
				  var Districtname = data.data.Districtname;
				  //search = "Malaysia";
				  jQuery('#state option:contains('+stateName+')').prop('selected',true);
				  var selectedState = jQuery('#state').val();
				  	if(!selectedState){
					 jQuery("#district").html('<select id="district" placeholder="district" name="district" class="form-select required"><option value="" selected="selected">- Select district -</option></select>');
					}
					//console.log(selectedState);
					if(selectedState){
					  jQuery.ajax({
						url: "/get-districts",
						type: "POST",
						data: {
						  state_id : selectedState,
						},
						dataType: "json",
						success: function(data) {
						  
						  var html = [];
						  var selectDist = Drupal.t('- Select district -');
						  html.push('<select id="district" placeholder="district" name="district" class="form-select required">');
						  html.push('<option value="" selected="selected">'+selectDist+'</option>');
						  jQuery.each(data, function(index, district) {
							html.push('<option value="'+district.tid+'">'+district.name+'</option>');
						  })
						  html.push('</select>'); 
						  if(selectedState != ''){
							jQuery("#district").html(html.join(''));
							jQuery('#district option:contains('+Districtname+')').prop('selected',true);
						  } else {
						    console.log('something went wrong with district select.');	
						  }	
						   formValidation();		
						}
					  });
					}
				  var districtName = data.data.Districtname;
				  if(city_name) {
					jQuery("#city").val(city_name);

				  } else {
				  	jQuery("#city").val('');
				  	console.log('City not found for selected pincode.');
				  }
				   formValidation();		
				  //console.log(data);
				}
			  });
			}
			
	 	});
		
	 	function formValidation(){
	 		if(jQuery("form#profile-popup-form").length){
		 		var isFine = true;

				jQuery(".form-item-state .alert").remove();	
				jQuery(".form-item-district .alert").remove();
				jQuery(".form-item-pincode .alert").remove();
				jQuery(".form-item-city .alert").remove();	
				jQuery(".form-item-address .alert").remove();	
		 		if(jQuery("#state").val() == ''){
					isFine = false;
					jQuery("#state").addClass("error-message");
					var selectState = Drupal.t('Please select state');
					jQuery(".form-item-state").append("<div class='alert' >"+selectState+"</div>");
				}else{
					jQuery("#state").removeClass("error-message");			
				}
				if(jQuery("#district").val() == ''){
					isFine = false;
					jQuery("#district").addClass("error-message");
					var selectDistrict = Drupal.t('Please select district');
					jQuery(".form-item-district").append("<div class='alert' >"+selectDistrict+"</div>");
				}else{
					jQuery("#district").removeClass("error-message");	
				}
				var pattern = /^[0-9]+$/;
				var selectPincode = Drupal.t('Please enter valid Pincode. Allowed only 6 digit numbers(1-9)');
				if(jQuery("#pincode").val() != ''){				
					if(pattern.test(jQuery("#pincode").val()) == false){
						isFine = false;
						jQuery("#pincode").addClass("error-message");
						jQuery(".form-item-pincode").append("<div class='alert' >"+selectPincode+"</div>");
					}else{
						//alert(parseInt(jQuery("#pincode").val()));
						if(parseInt(jQuery("#pincode").val()) > 1000000 || parseInt(jQuery("#pincode").val()) < 99999){
							isFine = false;
							jQuery("#pincode").addClass("error-message");
							jQuery(".form-item-pincode").append("<div class='alert' >"+selectPincode+"</div>");	
						}else{
							jQuery("#pincode").removeClass("error-message");
							
						}						
					}
				}else{
					jQuery(".form-item-pincode").append("<div class='alert' >"+selectPincode+"</div>");
					isFine = false;
					jQuery("#pincode").addClass("error-message");				
				}
				var pattern = /^[a-zA-Z -]+$/;
				var selectCity = Drupal.t('Please enter valid City/Village name in alphabet characters only.');
				if(jQuery("#city").length){
					if(jQuery("#city").val() != ''){
						if(pattern.test(jQuery("#city").val()) == false ||  jQuery("#city").val().length < 3 || jQuery("#city").val().length > 20){
							isFine = false;
							jQuery("#city").addClass("error-message");
							jQuery(".form-item-city").append("<div class='alert' >"+selectCity+"</div>");
						}else{
							jQuery("#city").removeClass("error-message");
										
						}
					}else{
						jQuery(".form-item-city").append("<div class='alert' >"+selectCity+"</div>");
						jQuery("#city").addClass("error-message");	
						isFine = false;			
					}
				}
				var pattern = /^[a-zA-Z0-9\/ -,\-_.:#]+$/;
				var selectAddress = Drupal.t('Address field only contains Alpha numeric and -,.:# /');
				if(jQuery("#address").length){
					if(jQuery("#address").val() != ''){
						if(pattern.test(jQuery("#address").val()) == false){
							isFine = false;					
							jQuery("#address").addClass("error-message");
							jQuery(".form-item-address").append("<div class='alert' >"+selectAddress+"</div>");
						}else{
							jQuery("#address").removeClass("error-message");	
						}
						var selectAddress = Drupal.t('Address field must contains maximum 200 characters. ');
						if((jQuery("#address").val() != '') && (jQuery("#address").val().length > 200)){
							isFine = false;					
							jQuery("#address").addClass("error-message");
							jQuery(".form-item-address").append("<div class='alert' >"+selectAddress+"</div>");
						}else{
							jQuery("#address").removeClass("error-message");	
						}
					}
				}
				if(isFine == false){
					jQuery("#profile-popup-form #edit-submit").attr("disabled","disabled");
					//jQuery("#box").show();
				}else{
					//jQuery("#box").hide();
					jQuery("#profile-popup-form #edit-submit").removeAttr("disabled");
					//jQery(".alert").remove();
				}
				return isFine;
			}
	 	}
		
		jQuery("#profile-popup-form").ready(function () {
			//alert(jQuery("#state").val());
			formValidation();
			
		});
		jQuery("select#district").change(function(){
			formValidation();
		});
		jQuery("#pincode").keyup(function(){
			formValidation();
		});
		jQuery("#city").keyup(function(){
			formValidation();
		});
		jQuery("#address").keyup(function(){
			formValidation();
		});
		jQuery("textarea#address").change(function(){
			formValidation();
		});
		//End popup-profile-form code
	}
};


function numberWithComma(x) {
  var parts = new Intl.NumberFormat('en-IN', { maximumSignificantDigits: 15 }).format(x);
  return parts;
}