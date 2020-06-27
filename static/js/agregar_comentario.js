$(document).ready(function() {
    $('#agregarComentario').click(function() {
        var serializerData =
            $("#nuevoComentario").serialize();
        console.log(serializerData)
        $.ajax({
            url: $("nuevoComentario").data('url'),
            data: serializerData,
            dataType: 'json',
            type: 'post',
            success: function(response) {
                console.log(response)

                var toJson = JSON.parse(response);
                console.log(toJson)
                document.getElementById('mostrarComentario').innerHTML = toJson

                $("mostrarComentario").
                append('<div class="post-comment"><img src=""alt="" class="profile-photo-sm" /><p><a href="" class="profile-link">' + toJson.comentario.nombre + response.comentario.apellido + '</a>' + response.comentario.comentario + '</p></div>')
            }

        });
    });
});