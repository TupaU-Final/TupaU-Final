(function(){
    function filePreview(input){
        if(input.files && input.files[0]){
            var reader = new FileReader(); 

            reader.onload = function(e){
                $('#previewImage').html("<img src='"+e.target.result +"' alt='user' id='fotoPerfil' height='120' width='120'/>"); 
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

    $('#input-perfil').change(function(){
        filePreview(this);
    });
})(); 