(function (jQuery) {
	Drupal.behaviors.validate = {
	attach: function (context, settings) {
		
  }
  };
});

jQuery('#cowin-certificate-form #edit-mobile').on('keypress', function(e) {
	  keys = ['0','1','2','3','4','5','6','7','8','9']
	  return keys.indexOf(event.key) > -1
});

jQuery('#cowin-certificate-form #edit-otp').on('keypress', function(e) {
	  keys = ['0','1','2','3','4','5','6','7','8','9']
	  return keys.indexOf(event.key) > -1
});

jQuery('#cowin-certificate-form #edit-beneficiary_id').on('keypress', function(e) {
	  keys = ['0','1','2','3','4','5','6','7','8','9']
	  return keys.indexOf(event.key) > -1
});