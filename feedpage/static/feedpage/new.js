
$('.fileInput').change(function() {
    var numfiles = $(this)[0].files.length;
    var parent = $(this).closest('.input-file');
    parent.find('ins').remove();
    for (i = 0; i < numfiles; i++) { 
      parent.append('<ins>' + $(this)[0].files[i].name + '</ins>')
    }
  });
  