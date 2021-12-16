(function ($) {
    Drupal.behaviors.firebase_push = {
        attach: function (context, settings) {
            $('body', context).once('web_push_notification', function () {

                var config = Drupal.settings.web_push_config;
                var banner = Drupal.settings.web_push_banner;
                var banner_script = Drupal.settings.banner_script;

                firebase.initializeApp(config);

                if (firebase.messaging.isSupported()) {

                    // messaging is supported
                    const messaging = firebase.messaging();

                    // Show notification
                    if(firebase.Promise && messaging && banner && !banner_script) {
                        $('#web_notification').show();
                    }

                    messaging
                        .requestPermission()
                        .then(function () {

                            // Hide banner notification
                            $('#web_notification').hide();

                            // get the token in the form of promise
                            return messaging.getToken()
                        })
                        .then(function(token) {

                            // Send token to server
                            sendSubscriptionToServer(token);
                        })
                        .catch(function (err) {

                            $('#web_notification').hide();
                            console.log("Unable to get permission to notify.");
                        });
                    messaging.onMessage(function(payload) {
                        ///console.log(payload);

                        // Generate HTML for message.
                        //var data = payload.data.notification;
                        var data = payload.data;
                        //data = $.parseJSON(data);
                        var messageHtml ="<div class='message-wrap'><span class='msg_close'></span><a href='"+data.url+"'><div class='msg_header'><span class='site_logo'><img src='/sites/all/themes/mygov/front_assets/images/logo.png'></span><span class='msg_title'>"+data.title+"</span></div><div class='msg_image'><img src='"+data.image+"'/></div><div class='msg_body'>"+data.body+"</div></a></div>";

                        $('#web_notification_message').append(messageHtml);

                        // Hide on click close.
                        $('.msg_close').click(function () {
                            $(this).parent('.message-wrap').hide();
                        });
                    });
                } else {
                   console.log("Browser doesn't support firebase API");
                }

            });

            /**
             *  Send subscription to server.
             **/
            function sendSubscriptionToServer (token) {
              var uid = Drupal.settings.web_push_user_id;
              if(!uid) {
                  uid = 0;
              }
                $.post('/api/1.0/web_push',
                    JSON.stringify({
                        registration_id: token,
                        domain_name:window.location.hostname,
                        uid:uid
                    }),function (data) {
                        if(data.success) {
                            $('#web_notification').hide();
                        }
                    });
            }
        }
    };
})(jQuery);



jQuery(document).ready(function($) {
	//alert("dsfsdfsdfsdf");
	/*jQuery( "#web-push-notification-form .form-item-domain input").attr("disabled","disabled");
	jQuery( "#web-push-notification-form .form-item-device input" ).click(function() {		
		jQuery( "#web-push-notification-form .form-item-device input").prop("checked", false);		
		jQuery(this).prop("checked", true);
		jQuery( "#web-push-notification-form .form-item-domain input").attr("disabled","disabled");
		jQuery( "#web-push-notification-form .form-item-domain input").prop("checked", false);	
		if(jQuery(this).val() == 'web'){			
			jQuery( "#web-push-notification-form .form-item-domain input").removeAttr("disabled");
		}
	});
	jQuery( "#web-push-notification-form .form-item-domain input" ).click(function() {	
		jQuery( "#web-push-notification-form .form-item-domain input").prop("checked", false);		
		jQuery(this).prop("checked", true);
	});*/

});

jQuery(document).ready(function($) {
	
	
	jQuery("#web-push-notification-batchpost-form").ready(function($) {
		jQuery("#web-push-notification-batchpost-form").submit();
	});
	//alert(jQuery("#web-push-notification-form .form-item-title #edit-title").val());
	jQuery("#web-push-notification-form .form-item-title #edit-title").keyup(function(){
		var len = parseInt(jQuery(this).val().length);
		if(len > 120){
			jQuery(this).val(jQuery(this).val().slice(0,-1));
			jQuery("#web-push-notification-form .form-item-title .description").text("0 Char left");
			alert("Title field is allowed only 160 letter");
		}else{
			jQuery("#web-push-notification-form .form-item-title .description").text((120 - len) +" Char left");
		}
	});
	//jQuery("#web-push-notification-form").ready(function($) {
		//jQuery("#web-push-notification-batchpost-form").submit();
		//alert("sdsd");
		
	//});
	
});

function test_notification(){	
		var body = jQuery("#edit-body").val();
		var title = jQuery("#edit-title").val();
		var icon = encodeURI(jQuery("#im-area img").attr("src"));
		var url = encodeURI(jQuery("#edit-url").val());
		
		if(title == ''){
			alert("Please enter Title.");
		}else if(icon == undefined){
			alert("Please Upload Icon.");
		}else if(url == ''){
			alert("Please enter Url.");
		}else{
			var targetUrl = "/admin/config/services/web_push_notification/postbatch_test?title="+title+"&icon="+icon+"&url="+url+"&body="+body; 
			window.open(targetUrl, '_blank');
		}
	}
function demo_notification(){
	var body = jQuery("#edit-body").val();
	var title = jQuery("#edit-title").val();
	var icon = encodeURI(jQuery("#im-area img").attr("src"));
	var url = encodeURI(jQuery("#edit-url").val());
	
	if(title == ''){
		alert("Please enter Title.");
	}else if(url == ''){
		alert("Please enter Url.");
	}else{
		var str = "<div class='msg_image'><img src='"+icon+"'/></div>";
		if(icon == undefined || icon == "undefined"){
			str = '';
		}
		var messageHtml ="<div class='message-wrap'><span class='msg_close'></span><a href='"+url+"' target='_BLANK'><div class='msg_header'><span class='site_logo'><img src='/sites/all/themes/mygov/front_assets/images/logo.png'></span><span class='msg_title'>"+title+"</span></div>"+str+"<div class='msg_body'>"+body+"</div></a></div>";

		jQuery('.overlayNotify').html(messageHtml);
		jQuery('.overlayNotify').show();
		jQuery(".msg_close").click(function(){
			jQuery('.overlayNotify').hide();
		  })
	}
	
}
