/* 입력창에 커서 올렸을 때 글자 사라지는 interaction */

$(document).ready(function() { 
    var placeholderTarget = $('.email_box input[type="text"], .password_box input[type="password"]'); 

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
