/*window.twttr = (function (d,s,id) {
    var t, js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return; js=d.createElement(s); js.id=id;
    js.src="https://platform.twitter.com/widgets.js";
    fjs.parentNode.insertBefore(js, fjs);
    return window.twttr || (t = { _e: [], ready: function(f){ t._e.push(f) } });
}(document, "script", "twitter-wjs"));
*/
/*twttr.ready(function (twttr) {
    twttr.events.bind('tweet', function ( e ) {
        if(e && e.type == "tweet") {
            var entity_type = jQuery(e.target).attr('data-entity-type');
            var entity_id = jQuery(e.target).attr('data-entity-id');
            jQuery.ajax({
                url: "/share-n-track/record",
                type: "POST",
                data: {
                    service     : 'twitter' ,
                    entity_type : entity_type,
                    entity_id   : entity_id
                },
                success: function() {
                    var sharingMsg = Drupal.t('Thank you for sharing!');
                    alert(sharingMsg);
                }
            });
        }
    });
});*/

if(typeof window.fbAsyncInit == 'undefined') {
    window.fbAsyncInit = function() {
        FB.init({
          appId      : '1463671287222985',
          xfbml      : true,
          version    : 'v2.1'
        });
    };

    (function(d, s, id){
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/en_US/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
}

window.shar_n_track = {};

(function($) {
	Drupal.behaviors.share_n_track = {
    attach : function(context, settings) {
        /*jQuery('a.share-n-track-facebook',context).click(function(e) {
            window.shar_n_track.link        = jQuery(this).attr('href');
            window.shar_n_track.title       = jQuery(this).attr('title');
            window.shar_n_track.share_text  = jQuery(this).attr('data-text');
            window.shar_n_track.entity_type = jQuery(e.target).attr('data-entity-type');
            window.shar_n_track.entity_id   = jQuery(e.target).attr('data-entity-id');

            FB.login(function() {
                
                // calling the API ...
                var obj = {
                  method: 'feed',
                  redirect_uri: window.location.origin,
                  link: window.shar_n_track.link,
                  name: window.shar_n_track.title,
                  caption: window.shar_n_track.title,
                  description: window.shar_n_track.share_text
                };

                function callback(response) {
                  //if (response && !response.error) {
                        jQuery.ajax({
                            url: "/share-n-track/record",
                            type: "POST",
                            data: {
                                service     : 'facebook',
                                entity_type : window.shar_n_track.entity_type, 
                                entity_id   : window.shar_n_track.entity_id
                            },
                            success: function() {
                                var sharingMsg = Drupal.t('Thank you for sharing!');
                                alert(sharingMsg);
                            }
                        });
                        
                        window.shar_n_track = {}
                    //}
                }

                FB.ui(obj, callback);
              });
            
            return false;
        });*/
	}
	}
}(jQuery));
