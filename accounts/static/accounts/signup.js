
$(document).ready(function() { 
    var placeholderTarget = $('.email_box input[type="text"], .password_box1 input[type="password"], .password_box2 input[type="password"], .nickname_box input[type="text"]'); 

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


$(function(){
	var container = $('.container'), inputFile = $('#file'), img, btn, txt = '사진 넣기', txtAfter = '다른 사진 넣기';
			
	if(!container.find('#upload').length){
		container.find('.input').append('<input type="button" value="'+txt+'" id="upload">');
		btn = $('#upload');
		container.prepend('<img src="" class="hidden" alt="Uploaded file" id="uploadImg" width="100">');
		img = $('#uploadImg');
	}
			
	btn.on('click', function(){
		img.animate({opacity: 0}, 300);
		inputFile.click();
	});

	inputFile.on('change', function(e){
		container.find('label').html( inputFile.val() );
		
		var i = 0;
		for(i; i < e.originalEvent.srcElement.files.length; i++) {
			var file = e.originalEvent.srcElement.files[i], 
				reader = new FileReader();

			reader.onloadend = function(){
				img.attr('src', reader.result).animate({opacity: 1}, 700);
			}
			reader.readAsDataURL(file);
			img.removeClass('hidden');
		}
		
		btn.val( txtAfter );
	});
});