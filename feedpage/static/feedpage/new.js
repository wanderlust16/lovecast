
$(document).ready(function() { 
  var placeholderTarget = $('.title_box input[type="text"], .story input[type="text"], .hashtag_text input[type="text"]'); 

  //포커스시 
  placeholderTarget.on('focus', function(){ 
      $(this).siblings('label').fadeOut('fast'); }); 
      
  //포커스아웃시
  placeholderTarget.on('focusout', function(){ 
      if($(this).val() == ''){ 
          $(this).siblings('label').fadeIn('fast'); 
      } 
  }); 
});