$(document).ready(function(){
    $('[type="checkbox"]').change(function(){
    if(this.checked){
        $('[type="checkbox"]').not(this).prop('checked', false);
    }    
});
});
$(document).ready(function() {
    $('.flexslider').flexslider({
      animation: "slide"
    });
});

