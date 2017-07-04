$(document).ready(function() {
    
   $('.search-row').keyup(function(event) {
       var query = $('#query').val();
       if ($.trim(query)) {
            $('#submit-btn').prop('disabled', false);
       } else {
            $('#submit-btn').prop('disabled', true);
       }
   });
   
   $('.footer').click(function() {
      if($('.footer').hasClass('slide-up')) {
        $('.footer').addClass('slide-down', 1000, 'easeOutBounce');
        $('.footer').removeClass('slide-up'); 
      } else {
        $('.footer').removeClass('slide-down');
        $('.footer').addClass('slide-up', 1000, 'easeOutBounce'); 
      }
  });
});