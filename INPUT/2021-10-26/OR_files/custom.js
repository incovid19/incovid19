$(document).ready(function() {

    $('.chart-lnk-hide').hide();
    $('.chart-lnk').click(function() {
        $('.show-chartlnk-box').addClass('active-chartbox');
        $(this).hide();
        $('.chart-lnk-hide').show();
    });
    $('.chart-lnk-hide').click(function() {
        $('.show-chartlnk-box').removeClass('active-chartbox');
        $(this).hide();
        $('.chart-lnk').show();
    });




    // Tool Tip
    $('[data-toggle="tooltip"]').tooltip();
    // Tool Tip

    // add top padding in tab and mobile view
    if ($(window).width() < 800) {
        var mainHdrHght = $('header').height();
        $('.page-controls-section').css('margin-top', mainHdrHght);
    }
    $('.share-section-icons').hide();

    $('.share-widget-handle').click(function(e) {
        e.preventDefault();
        e.stopPropagation();
        $('.share-section-icons').toggle();
    });
    $('.share-section-icons').click(function(e) {
        e.stopPropagation();
    });
    $('body,.share-section-icon').click(function() {
        $('.share-section-icons').hide();
    });

    // end

    var windHght = $(window).height();
    // alert(windHght)
    if ($('.sidemenu .navbar-nav').height() > windHght) {
        $('.sidemenu .navbar-nav').css('height', windHght - 85);
    }
    //$('.sidemenu .navbar')

    // Date picker
    if ($('.datepicker').length > 0) {
        $('.datepicker').datepicker({
            format: "dd-M-yyyy",
            todayBtn: "linked",
            autoclose: true,
            todayHighlight: true
        });
    }
    // Date picker

    // Navigation button click
    $('.nav-toggle-btn').on('click', function(event) {
            event.stopPropagation();
            $(this).toggleClass('on');
            $('.page-container').toggleClass('display-full');
            $('.sidemenu').toggleClass('active');
        })
        // Navigation button click


    // language


    $('.sl-nav li ul li span').on('click', function() {
        $('.sl-nav li ul li span').removeClass('active');
        $(this).addClass('active')
        var thisval = $(this).text();

        $('.langval').text(thisval);

    })


    // Full width less than 800
    var windowWidth = $(window).width();
    if (windowWidth < 800) {
        $('.page-container').addClass('display-full');

    }
    // Full width less than 800


    // Btn web effect

    $(".btn").click(function(e) {


        $(".ripple").remove();

        var posX = $(this).offset().left,
            posY = $(this).offset().top,
            buttonWidth = $(this).width(),
            buttonHeight = $(this).height();


        $(this).prepend("<span class='ripple'></span>");



        if (buttonWidth >= buttonHeight) {
            buttonHeight = buttonWidth;
        } else {
            buttonWidth = buttonHeight;
        }


        var x = e.pageX - posX - buttonWidth / 2;
        var y = e.pageY - posY - buttonHeight / 2;



        $(".ripple").css({
            width: buttonWidth,
            height: buttonHeight,
            top: y + 'px',
            left: x + 'px'
        }).addClass("rippleEffect");
    });

    // Btn web effect

    // view password btn
    $('.passwordshowbtn').on('click', function() {
        $(this).find('i').toggleClass("icon-eye1 icon-key");
        var inputpass = $('.password').attr("type");

        if (inputpass == "password") {
            $('.password').attr("type", "text");
        } else {
            $('.password').attr("type", "password");
        }
    });

    // view password btn


    // Search panel
    $('.searchopen').on('click', function() {
            $('.search-sec').toggleClass('open');
            $(this).find('i').toggleClass('icon-angle-down icon-angle-up')
        })
        // Search panel

    // $('#search-click').on('click',function(){
    // //alert(0);
    //   $('.searchopen').trigger( "click" );
    // })

    // Input focus

    /*==== 1. Theme Script End====*/
    var lstorageval = localStorage.getItem("theme");
    // console.log(lstorageval)
    if (lstorageval !== "" && lstorageval !== null) {
        $('body').addClass(lstorageval);
    } else {
        $('body').addClass('black-theme');
    }

    $('.black-box').click(function() {

        if (typeof(Storage) !== "undefined") {
            localStorage.setItem("theme", "black-theme");
            var lstorageval = localStorage.getItem("theme");
            $('body').addClass(lstorageval);
        }

    });

    $('.original-box').click(function() {
        localStorage.setItem("theme", "light-theme");

        // localStorage.removeItem('theme');
        // alert(localStorage.getItem("theme"));
        $('body').removeClass('black-theme');
    });



    $(".form-control")
        .on('focus', function() {

            $(this).parents('.control-group').addClass('focused');
        })
        .on('focusout', function() {
            if ($(this).val() != "") {
                //alert(1)
                $(this).parents('.control-group').addClass('focused');
            } else {
                //alert(2)
                $(this).parents('.control-group').removeClass('focused');
            }
        });

    $(".control-group label").click(function() {
        $(this).parents('.control-group').addClass('focused');
        $(this).parents('.control-group').find('.form-control').focus();

    });

    // Input focus




    // Logout madal
    $('.logout').click(function() {

        $('.logout-modal').addClass('show');

        setTimeout(function() {
            $('.logout-modal').removeClass('show');

        }, 5000);
    })


    $('.nologout').click(function() {
            $('.logout-modal').removeClass('show')
        })
        // Logout madal
        // Logout madal


});

$('.covid360').click(function() {
    window.open("https://covid360orissa.secure.force.com/Registration/", "CovidWindow", "width=" + $(window).width() + ",height=" + $(window).height() + "");
    // window.open("https://covid360orissa.secure.force.com/Registration/",'_blank','directories=no,titlebar=no,toolbar=no,location=no,status=no,menubar=no,scrollbars=no,resizable=no,left=0');
});

// Slim scroll funtion
(function($) {
    $(".notifications ul,.fixed-height,.instruction-details").mCustomScrollbar({
        theme: "inset-2-dark"
    });

})(jQuery);
// Slim scroll funtion

var windowWidth = $(window).width();
if (windowWidth < 800) {
    $(document).on("click", function(event) {
        var $trigger = $(".nav-toggle-btn");
        if ($trigger !== event.target && !$trigger.has(event.target).length) {
            $('.page-container').addClass('display-full');
            $('.sidemenu').removeClass('active');
        }
    });




}
if (windowWidth > 800) {
    (function($) {
        $(".sidemenu .navbar").mCustomScrollbar({
            theme: "inset-2-dark"
        });

    })(jQuery);
}


$(window).scroll(function() {
    var height = $(window).scrollTop();
    if (height > 0) {

        $('header').addClass('active');
    } else {
        $('header').removeClass('active');

    }
    if (height > 0) {

        $('.page-controls-section,.user-profile,.mainpanel').addClass('active');




    } else {


        $('.page-controls-section,.user-profile,.mainpanel').removeClass('active');

    }
});