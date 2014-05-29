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
        
    }
    
});

