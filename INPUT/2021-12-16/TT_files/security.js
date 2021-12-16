
function burstCache() { 
	if (!navigator.onLine) { 
		document.body.innerHTML = 'Loading...'; 
		window.location = '/'; 
	} 
}

window.onload = burstCache;
(function ($) {
	/**
	 * Handler for the form redirection error.
	 */ 
if(typeof Drupal.ajax != 'undefined' ) {
		Drupal.ajax.prototype.error = function (response, uri) {
		  var html;
		  if(typeof WB_Popup != 'undefined') {
			  html = drupalErrorMessage(response, uri, true);
			  WB_Popup.show();
			  WB_Popup.setContent(html);
			  WB_Popup.setToCenter();
			  WB_Popup.hideNext();
			  WB_Popup.hidePrev();
		  } else {
			  //html = Drupal.ajaxError(response, uri);
			  html = drupalErrorMessage(response, uri);
			  //alert(html);
			  console.log(html);
		  }
		  
		  // Remove the progress element.
		  if (this.progress.element) {
		    $(this.progress.element).remove();
		  }
		  
		  if (this.progress.object) {
		    this.progress.object.stopMonitoring();
		  }
		  
		  // Undo hide.
		  $(this.wrapper).show();
		  
		  // Re-enable the element.
		  $(this.element).removeClass('progress-disabled').removeAttr('disabled');
		  
		  // Reattach behaviors, if they were detached in beforeSerialize().
		  if (this.form) {
		    var settings = response.settings || this.settings || Drupal.settings;
		    Drupal.attachBehaviors(this.form, settings);
		  }
		};
	}
	
})(jQuery);
(function ($) {
	  Drupal.behaviors.ogpl_security_suit = {
	    attach: function(context) {
	      // JavaScript Alert bei AJAX-Autocomplete deaktivieren. Siehe:
	      // Drupal alerts "An AJAX HTTP request terminated abnormally" during
	      // normal site operation, confusing site visitors/editors:
	      // http://drupal.org/node/1232416#comment-6165578 (#98)
	      $.ajaxSetup({
	        beforeSend: function(jqXHR, settings) {
	          settings.error = function(jqXHR, textStatus, errorThrown) {
	            if (jqXHR.status) {
	              // An AJAX HTTP error occurred.
	              // Show error Message.
	            	 if(typeof WB_Popup != 'undefined') {
	       			  html = drupalErrorMessage(jqXHR, settings.url, true);
	       			  WB_Popup.show();
	       			  WB_Popup.setContent(html);
	       			  WB_Popup.setToCenter();
	       			  WB_Popup.hideNext();
	       			  WB_Popup.hidePrev();
		       		  } else {
		       			  //html = Drupal.ajaxError(response, uri);
		       			  html = drupalErrorMessage(jqXHR, settings.url);
		       			  alert(html);
		       		  }
	            }
	            // do nothing if AJAX HTTP request terminated abnormally.
	          };
	        }
	      });
	    }
	  };
	})(jQuery);

function drupalErrorMessage(response, uri, is_html) {
	if(typeof is_html == 'undefined') {
		is_html = false;
	}
	var title;
	var message;
	switch(response.status) {
		case 200:
		case 404:
			title = 'Request Not Found';
			message = 'Error! Requested page could not be found.';
			break;
		case 403:
			title = 'Access Denied';
			message = 'You are not authorized. Please contact site Administrator.';
			break;
	}
	if(is_html) {
	var html = '<div id="web_catalog_content"><div id="web_catalog_title">'+
	'<h2>'+title+'</h2></div><div id="web_catalog_error" style=" padding: 50px 0; '+
	'text-align:center;">'+message+'</div></div>';
	} else {
		var html = "Error! Try later";
	}
	return html;
} 