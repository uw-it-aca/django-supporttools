$(function() {
    
    // if mobile... handle menu button click fo
    if (window.support.is_mobile || window.support.is_tablet) {
        $('a#tool_menu_button').click(function(event) {
            event.preventDefault();
            $('#tool_menu').toggleClass('hide-div').toggleClass('show-div');
        });
    }
    // else desktop... hide the menu button and show the full menu list
    else {
        $('a#tool_menu_button').hide();
        $('#tool_menu').removeClass('hide-div');
        
        // get correct height for sidebar
        calculate_sidebar_height();
        
    }
    
});

$(window).resize(function() {
    
    if (!window.support.is_mobile && !window.support.is_tablet) {
        // get correct height for sidebar
        calculate_sidebar_height();
    }
        
});


function calculate_sidebar_height() {
    
    var base_h = $(".header").height();
    var header_h = 60;
    var netid_h = $(".tool-app").outerHeight();
    var footer_h = $(".footer").outerHeight(); 
    
    var diff_h = base_h - (header_h + netid_h + footer_h) - 20;
    
    $(".tool-list-inner").height(diff_h);

}
