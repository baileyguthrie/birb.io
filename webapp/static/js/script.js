/* global $ */
$(document).ready(function() {
    
    // disables submit button until text is typed
    $('#search-row').keyup(function(event) {
        var query = $('.query').val();
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
   
    // shows active page
    if (window.location.pathname == "/") {
        $('#search').addClass('active-page');
    } else if (window.location.pathname == "/compare") {
        $('#compare').addClass('active-page');
    } else if (window.location.pathname == "/trending") {
        $('#trending').addClass('active-page');
    } else if (window.location.pathname == "/info") {
        $('#info').addClass('active-page');
    }
    
    // night mode enablers
    $('#night-check').change(function() {
        console.log("change");
        if (this.checked) {
            enableNightMode();
        } else {
            disableNightMode();
        }
    });
    if (localStorage.getItem('nightmode') == 'true') {
        enableNightMode();
        $('#night-check').prop('checked', true);
    }
    function enableNightMode() {
        localStorage.setItem('nightmode', 'true');
        $('html').addClass('night-mode');
        $('body').addClass('night-mode');
        $('#info-well').css({
            'background': '#303030',
            'color': 'white' 
        });
        $('.night-well').css({
            'background': '#303030',
            'color': 'white' 
        });
        $('.error-well').css({
            'background': '#303030',
            'color': 'white'
        });
        $('.query').addClass('night-bar');
        $('.night-text').css('color', 'white');
    }
    function disableNightMode() {
        localStorage.setItem('nightmode', 'false');
        $('html').removeClass('night-mode');
        $('body').removeClass('night-mode');
        $('#info-well').css({
            'background': 'white',
            'color': '#333' 
        });
        $('.night-well').css({
            'background': 'white',
            'color': '#333' 
        });
    }
    
    // colors the result well
    function colorCards() {
        $('.results-group .result-container').each(function() {
            var currentCard = $(this);
            switch ($(this).find('.statement').text()) {
                
                case "Neutral":
                    if (localStorage.getItem('nightmode') == 'true') {
                        currentCard.css({
                            'background': '#303030',
                            'color': 'white'
                        });
                    }
                    break;
                    
                case "Slightly Positive":
                    currentCard.css('background', '#d7ffd9');
                    break;
                case "Positive":
                    currentCard.css('background', '#c5fdc7');
                    break;
                case "Very Positive":
                    currentCard.css('background', '#b2fab4');
                    break;
                case "Extremely Positive":
                    currentCard.css('background', '#a5f4a7');
                    break;
                case "Maximum Positivity":
                    currentCard.css('background', '#98ee99');
                    break;
                    
                case "Slightly Negative":
                    currentCard.css('background', '#ffcccb');
                    break;
                case "Negative":
                    currentCard.css('background', '#ffb8b7');
                    break;
                case "Very Negative":
                    currentCard.css('background', '#ffa4a2');
                    break;
                case "Extremely Negative":
                    currentCard.css('background', '#ff958f');
                    break;
                case "Maximum Negativity":
                    currentCard.css('background', '#ff867c');
                    break;
            }
        });
    }
    colorCards();
    
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

    // search bar submit scripts    
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
        <div style="display: none" class="new-bar">
            <li>
                <br>
                <div class="row">
                    <div class="col-md-6 col-md-offset-3">
                        <div class="search-row compare-query" id="#compare-row">
                            <input class="query" type="text" name="query" autocomplete="off">
                            <button data-toggle="tooltip" title="Will search through mentions of and replies to user" class="user-btn user-btn-disabled user-btn-extra" type="button">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg replaced-svg">
                                    <path class="draw" d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                    <circle class="draw" cx="12" cy="7" r="4"></circle>
                                </svg>
                            </button>
                            <button class="close-btn" type="reset">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg close-icon replaced-svg">
                                    <line x1="18" y1="6" x2="6" y2="18" style="stroke: rgb(229, 57, 53);"></line>
                                    <line x1="6" y1="6" x2="18" y2="18" style="stroke: rgb(229, 57, 53);"></line>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </li>
        </div>`;
    // compare page add button scripts
    $('#add-btn').click(function() {
        event.preventDefault();
        $('#compare-btn').prop('disabled', true);
        if ($('#compare-search-bars li').length < 9) {
            $('#compare-search-bars').append(newSearchBar);
            if (localStorage.getItem('nightmode') == 'true') {
                $('#compare-search-bars').find('.new-bar:last .query').addClass('night-bar');
            }
            $('#compare-search-bars').find(".new-bar:last").slideDown(150);
        } else if ($('#compare-search-bars li').length == 9) {
            $('#compare-search-bars').append(newSearchBar);
            $('#compare-search-bars').find(".new-bar:last").slideDown(150);
            $('#add-btn').hide();
        }
        if ($('#compare-search-bars li').length == 4) {
            $('#warning').slideDown({
                start: function() {
                    $('#warning').css('display', 'flex');
                    $('#warning').css('max-height', '52px');
                },
                duration: 150
            });
        }
    });
    
    // colors red x on compare bars
    $('ul').on({
        mouseenter: function() {
            $(this).find('line').css('stroke', '#ff6f60');
        },
        mouseleave: function() {
            $(this).find('line').css('stroke', '#e53935');
        }
    }, '.close-btn');
    
    // makes red x on compare bars functional
    $('ul').on('click', '.close-btn', function() {
        $(this).closest('li').remove();
        if ($('#compare-search-bars li').length == 9) {
            $('#add-btn').show();
        }
        setCompareButton();
    });
    
    // enables tooltips
    $(document).ready(function(){
        $('[data-toggle="tooltip"]').tooltip(); 
    });
    
    // user button scripts
    $('ul').on('click', '.user-btn', function() {
        if ($(this).hasClass('user-btn-disabled')) {
            $(this).removeClass('user-btn-disabled');
            $(this).addClass('user-btn-enabled');
            $(this).prop('title', "Will search through user's tweets");
            $(this).siblings($('.query')).prop('name', 'user-query');
        } else {
            $(this).removeClass('user-btn-enabled');
            $(this).addClass('user-btn-disabled');
            $(this).prop('title', "Will search through mentions of and replies to user");
            $(this).siblings($('.query')).prop('name', 'query');
        }
    });
    
    // enable or disable compare button
    function setCompareButton() {
        var emptyBox = false;
        $('#compare-search-bars li').each(function() {
            var currentList = $(this);
            var query = $(this).find('.query').val();
            if (!($.trim(query))) {
                emptyBox = true;
                userOption(currentList, false);
            } else if ($.trim(query)[0] == '@') {
                userOption(currentList, true);
            } else {
                userOption(currentList, false);
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
    
    // show or destroy user button
    function userOption(currentList, create) {
        if (create) {
            currentList.find('.user-btn').show();
            if (currentList.parent().hasClass('new-bar')) {
                currentList.find('.query').addClass('extra-padding');
            }
        } else { // destroy
            currentList.find('.user-btn').hide();
            currentList.find('.query').prop('name', 'query');
            if (currentList.parent().hasClass('new-bar')) {
                currentList.find('.query').removeClass('extra-padding');
            }
        }
    }
    
    // allow warning to be removed
    $('#warning').hide();
    $('#warning').click(function() {
        $('#warning').remove();
    });
    
    // hides compare search bars when results are present
    if ($('.results-group').length) {
        $('.compare-form').hide();
        $('.compare-show-btn').css('display', 'flex');
    }
    
    // shows compare search bars
    $('.compare-show-btn').click(function() {
        $(this).slideUp(150, function() {
            $(this).remove();
        });
        $('.compare-form').slideDown(150);
    });
    
    // animations for chart information
    $('#chart-info').on('click', function() {
        if ($(':animated').length) {
            return false;
        }
        if ($('#chart-info').hasClass('minimized')) {
            $('#chart-info svg').animate({ opacity: 0 }, 150, "swing", function() {
                $('#chart-info .svg').hide();
                $('#chart-info').animate({ width: '100%' }, 150, "swing", function() {
                    $('#chart-info').css('padding', '12px 16px');
                    $('#chart-info').css('height', 'auto');
                    $('#chart-info-text').slideToggle(150, function() {
                        $('#chart-info-text').animate({ opacity: 100 }, 150);
                    });
                });
            });
            $('#chart-info').toggleClass('minimized');
        } else {
            $('#chart-info-text').animate({ opacity: 0 }, 150, "swing", function() {
                $('#chart-info').css('padding', '0');
                $('#chart-info-text').slideToggle(150, function() {
                    $('#chart-info').css('height', '36px');
                    $('#chart-info').animate({width: '36px'}, 150, "swing", function() {
                        $('#chart-info .svg').show();
                        $('#chart-info .svg').animate({ opacity: 100 }, 150);
                    });
                });
            });
            $('#chart-info').toggleClass('minimized');
        }
    });
    
    // trending scripts
    
    // initial ajax request for trending
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
                    currentGroup.slideDown(400);
                    currentGroup.removeClass('unanalyzed');
                }
                colorCards();
                $('#trend-btn').slideDown(400);
            },
            error: function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
    // ajax requests for button
    var startingIndex = 5;
    $('#trend-btn').click(function() {
        $('#trend-btn').hide();
        $('.loader').show();
        $.ajax({
            url: "/trending",
            data: {"start": startingIndex},
            dataType: "json",
            success: function(response) {
                // console.log(response);
                startingIndex += 5;
                $('.loader').hide();
                for (var i = 0; i < 5; i++) {
                    var currentName = response.results[i].name;
                    var currentGroup = $('.results-group').find($('.unanalyzed:contains('+currentName+')'));
                    currentGroup.find('.statement').text(response.results[i].statement);
                    currentGroup.find('.analysis').text(response.results[i].analysis);
                    currentGroup.slideDown(400);
                    currentGroup.removeClass('unanalyzed');
                }
                if (!response.complete) {
                    $('#trend-btn').slideDown(400);
                }
                colorCards();
            },
            error: function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
    
    // gathers data for chart on compare page
    function getTransparentColor(color) {
        return color.replace('rgb', 'rgba').replace(')', ', 0.75)');
    }
    if ($('#chart').length) {
        var compareStats = {
            labels: [],
            backgroundColors: [],
            borderColors: [],
            scores: []
        };
        $('.result-container').each(function() {
            compareStats.labels.push($(this).find('.result-name').text());
            var color = $(this).css('background-color');
            compareStats.borderColors.push(color);
            compareStats.backgroundColors.push(getTransparentColor(color));
            
            var analysis = $(this).find('.analysis').text();
            var statement = $(this).find('.statement').text();
            if (/Maximum/.test(statement)) {
                var currentScore = 21.0;
            } else {
                var currentScore = parseFloat(/\d+\.\d{3}/.exec(analysis), 10);
            }
            currentScore -= 1;
            if (/neg/i.test(statement)) {
                currentScore *= -1;
            }
            currentScore = currentScore.toFixed(3);
            compareStats.scores.push(currentScore);
        });
        // console.log(compareStats);
        Chart.pluginService.register({
            beforeDraw: function (chart, easing) {
                if (chart.config.options.chartArea && chart.config.options.chartArea.backgroundColor) {
                    var helpers = Chart.helpers;
                    var ctx = chart.chart.ctx;
                    var chartArea = chart.chartArea;
        
                    ctx.save();
                    ctx.fillStyle = chart.config.options.chartArea.backgroundColor;
                    ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);
                    ctx.restore();
                }
            }
        });
        var ctx = $('#chart').get(0).getContext('2d');
        if (localStorage.getItem('nightmode') == 'true') {
            Chart.defaults.global.defaultFontColor = 'white';
            var gridColor = 'rgba(255,255,255,0.1)';
            var zeroColor = 'rgba(255,255,255,0.25)';
            var backgroundColor = '#303030';
        } else {
            var gridColor = 'rgba(0,0,0,0.1)';
            var zeroColor = 'rgba(0,0,0,0.25)';
            var backgroundColor = 'white';
        }
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: compareStats.labels,
                datasets: [{
                    label: 'Adjusted Score',
                    data: compareStats.scores,
                    backgroundColor: compareStats.backgroundColors,
                    borderColor: compareStats.borderColors,
                    borderWidth: 1
                }]
            },
            options: {
                chartArea: {
                    backgroundColor: backgroundColor
                },
                legend: {
                    display: false
                },
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Adjusted Score'
                        },
                        ticks: {
                            beginAtZero:true
                        },
                        gridLines: {
                            color: gridColor,
                            zeroLineColor: zeroColor
                        }
                    }],
                    xAxes: [{
                        gridLines: {
                            color: gridColor,
                            zeroLineColor: zeroColor
                        }
                    }]
                }
            }
        });
    }

});