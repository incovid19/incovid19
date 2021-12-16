/** Comment Auto Load Script **/
(function($) {
	  Drupal.behaviors.comment_auto_load = {
	    attach : function(context, settings) {
	    	jQuery(".node-type-talk .view-filters").css('display','none');
	    }
	  }
}(jQuery));

jQuery(function() {
	if(typeof jQuery("#new_comment").attr('id') != 'undefined') {

    		var intTimeout = setInterval(refresh_talk_page,60000);
		var intTimeout1 = setInterval(refresh_comment_list, 900000);
		//var nid = jQuery('#task_nid').val();
		//var cid = jQuery("#last_comment_details").attr("data-cid");
		//var count = jQuery("#last_comment_details").attr("data-count");
		//jQuery("#new_arrival").load("/js/refresh_comment_list/"+nid+"/"+count+"/"+cid);
		//jQuery("#comment_count_stats").load("/js/stats_count_update/"+nid);
		//jQuery.ajax({
	        //type:"get",    
	        //url: "/js/refresh_comment_list/"+nid+"/"+count+"/"+cid+"/"+1,
	        //success: function(data){
	        //	jQuery("#edit-submit-view-comments").click();
	    	  //  var cid_last = data.last_cid;
	    	//	var count_last = data.$new_count;
	    	//	jQuery("#last_comment_details").attr("data-cid", cid_last);
	    	//	jQuery("#last_comment_details").attr("data-count", count_last);
	        //}
	    //});
		
	}
	if( jQuery('.node-type-mygov-survey').length > 0 ){
		var nid = jQuery('#task_nid').val();
//		jQuery("#total_tasks").load("/js/survey_count_update/"+nid);
	}
});

function refresh_comment_list () {
	
	var nid = jQuery('#task_nid').val();
	var cid = jQuery("#last_comment_details").attr("data-cid");
	var count = jQuery("#last_comment_details").attr("data-count");
	jQuery("#comment_count_stats").load("/js/stats_count_update/"+nid);
	jQuery.ajax({
		type:"get",
		url: "/js/refresh_comment_list/"+nid+"/"+count+"/"+cid+"/"+1,
		success: function(data){
		        jQuery("#edit-submit-view-comments").click();
		    var cid_last = data.last_cid;
		        var count_last = data.$new_count;
		        jQuery("#last_comment_details").attr("data-cid", cid_last);
		        jQuery("#last_comment_details").attr("data-count", count_last);
		}
	});

}

function refresh_talk_page() {
	jQuery(".node-type-talk .views-submit-button input").click();
}
function refresh_count() {
	jQuery('#new_comment').click();
	if (jQuery("#new_arrival").html() == ""){
		jQuery('#new_arrival').removeAttr('onclick');
		jQuery('#new_arrival').removeAttr('title');
	}
	else {
		jQuery('#new_arrival').attr('onclick', 'get_new_comments();');
	}
}
/** Comment Auto Load Script **/
function get_latest_count(autoload) {
	
	var nid = jQuery('#task_nid').val();
	var cid = jQuery("#last_comment_details").attr("data-cid");
	var time = jQuery("#last_comment_details").attr("data-time");
	var count = jQuery("#last_comment_details").attr("data-count");
	jQuery("#new_arrival").load("/js/refresh_comment_list/"+nid+"/"+count+"/"+cid);
	if(!autoload){
		jQuery("#new_arrival").slideDown('slow');
	}
}
/** New Comments List Show **/
function get_new_comments() {
	
	var nid = jQuery('#task_nid').val();
	var cid = jQuery("#last_comment_details").attr("data-cid");
	var time = jQuery("#last_comment_details").attr("data-time");
	var count = jQuery("#last_comment_details").attr("data-count");
	var content;	
	jQuery.ajax({
        type:"get",    
        url: "/js/new_comment_show/"+cid+"/"+nid,
        beforeSend: function() {
            var loadText = Drupal.t('Loading...');
            jQuery( "#new_arrival" ).after( "<div class='ajax-processed-throbber'>"+loadText+"</div>" );
        	jQuery('#new_comment').removeAttr('onclick');
        },
        success: function(data){
        	content = data;
    	    jQuery("#latest_comment").prepend(content);
    	    Drupal.attachBehaviors(jQuery("#latest_comment"));
    	    jQuery("#post_list_content div.ajax-processed-throbber").hide();
    	    jQuery("#new_arrival").slideUp('slow');
    	    var cid_last = jQuery("#last_cid").val();
    		var count_last = jQuery("#last_count").val();
    		jQuery("#last_comment_details").attr("data-cid", cid_last);
    		jQuery("#last_comment_details").attr("data-count", count_last);
    		jQuery('.comment_count a').html(count_last);
    		jQuery('#new_comment').attr('onclick', 'get_latest_count();');
        }
    });
}
