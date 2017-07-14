/* global $ */
$(document).ready(function() {
    
    // disables submit button until text is typed
    $('#search-row').keyup(function(event) {
        var query = $('#query').val();
        if ($.trim(query)) {
            $('#submit-btn').removeAttr('disabled');
            $('svg circle').css('stroke', 'white');
            $('svg line').css('stroke', 'white');
            $('#submit-btn').css('background', '#66bb6a');
        } else {
            $('#submit-btn').prop('disabled', true);
            $('svg circle').css('stroke', 'rgb(160, 160, 160)');
            $('svg line').css('stroke', 'rgb(160, 160, 160)');
            $('#submit-btn').css('background', 'none');
        }
    });
   
    if (window.location.pathname == "/") {
        $('#search').addClass('active-page');
    } else if (window.location.pathname == "/compare") {
        $('#compare').addClass('active-page');
    } else if (window.location.pathname == "/trending") {
        $('#trending').addClass('active-page');
    } else if (window.location.pathname == "/info") {
        $('#info').addClass('active-page');
    }
    
    
    // colors the result well
    $('.results-group .results-well').each(function() {
        if ($(this).find('.results-statement:contains("Positive")').length || $(this).find('.results-statement:contains("Maximum Positivity")').length) {
            $(this).addClass('positive-well');
        } else if ($(this).find('.results-statement:contains("Negative")').length || $(this).find('.results-statement:contains("Maximum Negativity")').length) {
            $(this).addClass('negative-well');
    }
    });
    
    
    // allows search icon color to be changed with css

    $('img.svg').each(function(){
        var $img = $(this);
        var imgID = $img.attr('id');
        var imgClass = $img.attr('class');
        var imgURL = $img.attr('src');

        $.get(imgURL, function(data) {
            // Get the SVG tag, ignore the rest
            var $svg = $(data).find('svg');

            // Add replaced image's ID to the new SVG
            if(typeof imgID !== 'undefined') {
                $svg = $svg.attr('id', imgID);
            }
            // Add replaced image's classes to the new SVG
            if(typeof imgClass !== 'undefined') {
                $svg = $svg.attr('class', imgClass+' replaced-svg');
            }

            // Remove any invalid XML tags as per http://validator.w3.org
            $svg = $svg.removeAttr('xmlns:a');

            // Replace image with new SVG
            $img.replaceWith($svg);

        }, 'xml');

    });

        
    $('.submit-btn-cover').hover(function(){
        // on mouse enter
        if ($('#submit-btn').is(':disabled')) {
            $('svg circle').css('stroke', '#e57373');
            $('svg line').css('stroke', '#e57373');
        } else {
            $('#submit-btn').css('background', '#98ee99');
        }
    }, function(){
        // on mouse leave
        if ($('#submit-btn').is(':disabled')) {
            $('svg circle').css('stroke', 'rgb(160, 160, 160)');
            $('svg line').css('stroke', 'rgb(160, 160, 160)');
            $('#submit-btn').css('background', 'none');
        } else {
            $('#submit-btn').css('background', '#66bb6a');
        }
    });
    
    // compare page scripts
    
    var newSearchBar = `
        <li>
            <br>
            <div class="row">
                <div class="col-md-6 col-md-offset-3">
                    <div class="search-row compare-query" id="#compare-row">
                        <input id="query" type="text" name="query" autocomplete="off">
                        <button class="close-btn" type="reset">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg close-icon replaced-svg">
                                <line x1="18" y1="6" x2="6" y2="18" style="stroke: rgb(229, 57, 53);"></line>
                                <line x1="6" y1="6" x2="18" y2="18" style="stroke: rgb(229, 57, 53);"></line>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </li>`;
    
    $('#add-btn').click(function() {
        event.preventDefault();
        $('#compare-btn').prop('disabled', true);
        if ($('#compare-search-bars li').length < 9) {
            $('#compare-search-bars').append(newSearchBar);
        } else if ($('#compare-search-bars li').length == 9) {
            $('#compare-search-bars').append(newSearchBar);
            $('#add-btn').hide();
        }
        if ($('#compare-search-bars li').length == 4) {
            $('#warning').css('display', 'flex');
        }
    });
    
    $('ul').on({
        mouseenter: function() {
            $(this).find('line').css('stroke', '#ff6f60');
        },
        mouseleave: function() {
            $(this).find('line').css('stroke', '#e53935');
        }
    }, '.close-btn');
    
    $('ul').on('click', '.close-btn', function() {
        $(this).closest('li').remove();
        if ($('#compare-search-bars li').length == 9) {
            $('#add-btn').show();
        }
        setCompareButton();
    });
    
    function setCompareButton() {
        var emptyBox = false;
        $('#compare-search-bars > li').each(function() {
            var query = $(this).find('#query').val();
            if (!($.trim(query))) {
                emptyBox = true;
            }
        });
        if (emptyBox) {
            $('#compare-btn').prop('disabled', true);
        } else {
            $('#compare-btn').removeAttr('disabled');
        }
    }
    $('#compare-search-bars').keyup(function(event) {
        setCompareButton();
    });
    
    $('#warning').hide();
    $('#warning').click(function() {
        $('#warning').remove();
    });
    
    if (window.location.pathname == "/trending") {
        $.ajax({
            url: "/trending",
            data: {"start": 0},
            dataType: "json",
            success: function(response) {
                // console.log(response);
                $('.loader').hide();
                for (var i = 0; i < 5; i++) {
                    var currentName = response.results[i].name;
                    var currentGroup = $('.results-group').find($('.unanalyzed:contains('+currentName+')'));
                    currentGroup.find('.statement').text(response.results[i].statement);
                    currentGroup.find('.analysis').text(response.results[i].analysis);
                    currentGroup.removeClass('unanalyzed');
                }
                $('#trend-btn').show();
            },
            error: function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
    var startingIndex = 5;
    $('#trend-btn').click(function() {
        $('#trend-btn').hide();
        $('.loader').show();
        $.ajax({
            url: "/trending",
            data: {"start": startingIndex},
            dataType: "json",
            success: function(response) {
                console.log(response);
                startingIndex += 5;
                $('.loader').hide();
                for (var i = 0; i < 5; i++) {
                    var currentName = response.results[i].name;
                    var currentGroup = $('.results-group').find($('.unanalyzed:contains('+currentName+')'));
                    currentGroup.find('.statement').text(response.results[i].statement);
                    currentGroup.find('.analysis').text(response.results[i].analysis);
                    currentGroup.removeClass('unanalyzed');
                }
                if (!response.complete) {
                    $('#trend-btn').show();
                }
            },
            error: function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });

    
});