$(document).ready(function() {
   
   $('#submit-btn').onclick(function(event) {
       event.preventDefault();
       var query = $('#query').val();
       var url = window.location.href;
       
       $.ajax({
           url: url,
           data: query,
           type: 'GET',
           dataType: 'text',
           success: function(response) {
               $(body).css('background', 'red');
           },
           error: function(error) {
               $(body).css('background', 'blue');
           }
       });
   });
    
});