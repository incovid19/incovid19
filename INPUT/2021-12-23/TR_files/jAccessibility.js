jQuery(document).ready(function( $ ){
	function createCookie(name, value, days){
		var expires = "";
		if(days){
			var time = new Date();
			time.setTime(time.getTime()+(days*24*60*60*1000));
		}
		document.cookie = name+"="+value+expires+"; path=/";
	}

	function getCookie(name){
		var nameEQ = name + "=";
		var ca = document.cookie.split(';');
		for(var i=0;i < ca.length;i++) {
			var c = ca[i];
			while (c.charAt(0)==' ') c = c.substring(1,c.length);
			if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
		}
		return "";
	}

	function deleteCookie(name) {
		createCookie(name,"",-1);
	}

	function checkCookie(name){
		var check = getCookie(name);
		if(check != "")
			return true;
		return false;
	}

	/*======================================
	*		functions
	*======================================*/
	function addConstrast(){
  	console.log('addConstrast');
    $('*').addClass('pagina-acessivel');
    $('.acess-container').addClass('f-transparent');
    $('#botao').addClass('f-transparent');
    $('#acess-icons').addClass('f-transparent');
    $('.acess-icon').addClass('f-transparent');
    $('img').addClass('f-transparent');
    $('#jbbutton').addClass('f-transparent');
  }

  function removeConstrast(){
    console.log('removeConstrast');
    $('*').removeClass('pagina-acessivel');
    $('.acess-container').removeClass('f-transparent');
    $('#botao').removeClass('f-transparent');
    $('#acess-icons').removeClass('f-transparent');
    $('.acess-icon').removeClass('f-transparent');
    $('img').removeClass('f-transparent');
    $('#jbbutton').removeClass('f-transparent');
  }

  if(checkCookie('ccontrast')){
  	addConstrast();
  }

  $('#contrast').click(function(){
  	var ck = checkCookie('ccontrast');
	  if(ck){
	  	deleteCookie('ccontrast');
	    removeConstrast();
	  }else{
	    createCookie('ccontrast', 'cookieContrast');
	    addConstrast();
	  }
  });

	var $cElements = $("body").find("*");
	var fonts = [];
	var fontsOriginal = [];

	function getFontSize() {
		for (var i = 0; i < $cElements.length; i++) {
		    fonts.push(parseFloat($cElements.eq(i).css('font-size')));
		    fontsOriginal.push(parseFloat($cElements.eq(i).css('font-size')));
	  }
	}

	getFontSize();
	$("#increaseFont").on('click', function() {
		for (var i = 0; i < $cElements.length; i++) {
	   	++fonts[i];
	   	$cElements.eq(i).css('font-size', fonts[i]);
	  }
	});

	$("#decreaseFont").on('click', function() {
		for (var i = 0; i < $cElements.length; i++) {
			--fonts[i];
			$cElements.eq(i).css('font-size', fonts[i]);
		}
	});

	$("#restore").on('click', function () {
        //Reset Contrast
	    deleteCookie('ccontrast');
	    removeConstrast();
        //Reset Font
	    for (var i = 0; i < $cElements.length; i++) {
	        $cElements.eq(i).css('font-size', fontsOriginal[i]);
	    }
	    //Reset Font Array
	    fonts = [];
	    fonts = fontsOriginal.slice();
	});

	$('#jbbutton').click(function(){
    $('#acess-icons').toggle(150);
  });

});
