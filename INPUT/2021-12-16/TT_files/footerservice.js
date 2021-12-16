(function() {

// Localize jQuery variable
    var jQuery;

    /******** Load jQuery if not present *********/
    /*  Removed Version check  || window.jQuery.fn.jquery !== '1.10.1' */
    if (window.jQuery === undefined) {
        var script_tag = document.createElement('script');
        script_tag.setAttribute("type","text/javascript");
        script_tag.setAttribute("src",
            "https://ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js");
        if (script_tag.readyState) {
            script_tag.onreadystatechange = function () { // For old versions of IE
                if (this.readyState == 'complete' || this.readyState == 'loaded') {
                    scriptLoadHandler();
                }  
            };
        } else {
            script_tag.onload = scriptLoadHandler;
        }
        // Try to find the head, otherwise default to the documentElement
        (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);
    } else {
        // The jQuery version on the window is the one we want to use
        jQuery = window.jQuery;
        main();
    }

    /******** Called once jQuery has loaded ******/
    function scriptLoadHandler() {
        // Restore $ and window.jQuery to their previous values and store the
        // new jQuery in our local jQuery variable
        jQuery = window.jQuery.noConflict(true);
        // Call our main function
        main();
    }

    /******** Our main function ********/
    function main() {
        jQuery(document).ready(function($) {
            var htmldata = '<style type="text/css">.sub-sites{text-align:center; position:relative; padding:10px 15px 0;}.sub-sites li{padding:0 10px; border-left:1px solid #6b6c6f; display:inline-block;  margin-bottom:10px; list-style:none;} .sub-sites li:first-child,.footer-logo li:first-child{border:none;}.sub-sites:after {    background: rgba(0, 0, 0, 0) linear-gradient(to right, rgba(6, 47, 60, 0.01) 0%, rgba(45, 75, 100, 0.98) 50%, #2c4a63 51%, rgba(6, 47, 60, 0.01) 100%) repeat scroll 0 0;    content: "";display: block;    height: 1px;    position: absolute;    right: 0;    top: 0;    width: 100%;}.footer-logo {    background: #000;    padding: 7px 15px 0;    text-align: center;}.footer-logo li {    border-left: 1px solid #28282a;    display: inline-block;    padding: 0 10px;	margin-bottom:7px;    vertical-align: middle;	list-style:none;	 box-sizing:border-box; -moz-box-sizing:border-box; -webkit-box-sizing:border-box;} @media all and (max-width:640px){	.sub-sites li, .sub-sites li:first-child{padding:10px; border:1px solid #2c4a63;}	.sub-sites{padding:15px 10px 5px;} } @media all and (max-width:567px){	.footer-logo{overflow:hidden; padding:10px 5px 0;}	.footer-logo li{width:50%; border-left:none; padding:0px; float:left; margin:10px 0;}	.footer-logo li:nth-child(2n+2){border-left:1px solid #28282a; } }</style><div class="service-footer-wrapper">  <ul class="sub-sites">    <li><a title="Transforming India" href="https://transformingindia.mygov.in" target="_blank"><img title="Transforming India" alt="Transforming India" src="https://www.mygov.in/footer_service/images/Transforming-india-logo.png"></a></li><li><a title="MyGov Innovate India" href="https://innovateindia.mygov.in" target="_blank"><img title="MyGov Innovate India" alt="MyGov Innovate India" src="https://www.mygov.in/footer_service/images/innovation-logo.png"></a></li><li><a title="Swachhbharat" href="https://swachhbharat.mygov.in/" target="_blank"><img title="Swachhbharat" alt="Swachhbharat" src="https://www.mygov.in/footer_service/images/swachh-bharat.png"></a></li><li><a title="MyGov Quiz" href="https://quiz.mygov.in" target="_blank"><img title="MyGov Quiz" alt="MyGov Quiz" src="https://www.mygov.in/footer_service/images/mygov_quiz.png"></a></li><li><a title="MyGov Blog" href="https://blog.mygov.in" target="_blank"><img alt="MyGov Blog" src="https://www.mygov.in/footer_service/images/blog-logo.png"></a></li><li><a title="Self4Society" href="https://self4society.mygov.in" target="_blank"><img alt="Self4Society Logo" src="https://www.mygov.in/footer_service/images/itowe-logo.png"></a></li><li><a title="E-Greetings" href="https://egreetings.gov.in" target="_blank"><img title="E-Greetings" alt="E-Greetings" src="https://www.mygov.in/footer_service/images/e-greating.png"></a></li></ul>  <div class="footer-logo">    <ul>      <li><a target="_blank" href="http://www.digitalindia.gov.in" title="Digital India"><img title="Digital India (External Site that opens in a new window)" alt="Digital India" src="https://www.mygov.in/footer_service/images/digital-india-logo.png"></a></li>      <li><a target="_blank" href="http://data.gov.in" title="Data Portal"><img title="Data Portal (External Site that opens in a new window)" alt="Data Portal" src="https://www.mygov.in/footer_service/images/data-gov-logo.png"></a></li>      <li><a target="_blank" href="https://india.gov.in" title="National Portal of India"><img title="National Portal of India (External Site that opens in a new window)" alt="National Portal of India" src="https://www.mygov.in/footer_service/images/india-gov-logo.png"></a></li>      <li><a target="_blank" href="https://www.mygov.in" title="MyGov"><img title="MyGov (External Site that opens in a new window)" alt="MyGov" src="https://www.mygov.in/footer_service/images/mygov-footer-logo.png"></a></li>      <li><a title="MeitY (External Site that opens in a new window)" target="_blank" href="http://meity.gov.in/"><img title="Meity(External Site that opens in a new window)" alt="Meity" src="https://www.mygov.in/footer_service/images/Meity_logo.png"></a></li>      <li><a target="_blank" href="http://pmindia.gov.in" title="PMINDIA"><img title="PMINDIA(External Site that opens in a new window)" alt="PMINDIA" src="https://www.mygov.in/footer_service/images/pm-india-logo.png"></a></li></ul>  </div></div>';
            /******* Load HTML *******/
            $('.service-footer-wrapper').append(htmldata);
            jQuery('a[href^=http]').click(function(e){
                var curUrl = window.location.href;

                var curUrlArray = curUrl.split("/");

                if(curUrlArray[2] != "www.mygov.in"  && curUrlArray[2] != "secure.mygov.in" && curUrlArray[2] != "mygov.in"){
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
                             if(urlArray[2] == "www.mygov.in"  || urlArray[2] == "mygov.in"  || urlArray[2] == "auth.mygov.in"  || urlArray[2] == "secure.mygov.in" ||  urlArray[2] == curUrlArray[2]){

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
                } 
            
            });
        });
    }

})(); // We call our anonymous function immediately