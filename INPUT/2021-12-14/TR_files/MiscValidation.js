﻿$(document).ready(function () {
    $(".numberinput").forceNumeric();

    //Disable Cut Copy Paste
    $('.ccp-disable').bind('cut copy paste', function (e) {
        e.preventDefault();
        //alert("Cut / Copy / Paste Disabled.");
    });

    $('.typing-disable').keypress(function (e) {
        e.preventDefault();
    });
});

// forceNumeric() plug-in implementation
jQuery.fn.forceNumeric = function () {
    return this.each(function () {
        $(this).keydown(function (e) {
            var key = e.which || e.keyCode;

            if (!e.shiftKey && !e.altKey && !e.ctrlKey &&
                // numbers   
                key >= 48 && key <= 57 ||
                // Numeric keypad
                key >= 96 && key <= 105 ||
                // comma, period and minus, . on keypad
                //key == 190 || key == 188 || key == 109 || key == 110 ||
                // Backspace and Tab and Enter
               key == 8 || key == 9 || key == 13 ||
                // Home and End
               key == 35 || key == 36 ||
                // left and right arrows
               key == 37 || key == 39 ||
                // Del and Ins
               key == 46 || key == 45)
                return true;

            return false;
        });
    });
}