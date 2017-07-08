$(document).ready(function() {
    
    $('.search-row').keyup(function(event) {
        var query = $('#query').val();
        if ($.trim(query)) {
            $('#submit-btn').prop('disabled', false);
        } else {
            $('#submit-btn').prop('disabled', true);
        }
    });
   
    if (window.location.pathname == "/") {
        $('#search').addClass('active-page');
    }
    
    if (window.location.pathname == "/compare") {
        $('#compare').addClass('active-page');
    }
    
    if (window.location.pathname == "/trending") {
        $('#trending').addClass('active-page');
    }
    
    if ($('.results-statement:contains("Positive")').length) {
        $('.results-well').addClass('positive-well');
    } else if ($('.results-statement:contains("Negative")').length) {
        $('.results-well').addClass('negative-well');
    }
    
    
    
    
    
    $('#collapseOne').on('show.bs.collapse', function () {    
        $('.panel-heading').animate({
            backgroundColor: "#515151"
        }, 500);   
    })
    
    $('#collapseOne').on('hide.bs.collapse', function () {    
        $('.panel-heading').animate({
            backgroundColor: "#00B4FF"
        }, 500);   
    })
    
});