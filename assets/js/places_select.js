$(document).ready(function() {
    $('select[name="departamento"]').on('change', function() {
        var departamento = $(this).val();

        $.ajax({
            url: '/get_departamento_ciudad_barrio/',
            data: {
                departamento: departamento
            },
            success: function(data) {
                $('select[name="ciudad"]').removeAttr('disabled');
                $('select[name="ciudad"]').empty();

                $(data.ciudades).each(function(index, ciudad) {
                    $('select[name="ciudad"]').append('<option value="' + ciudad + '">' + ciudad + '</option>');
                });
            }
        });
    });

    $('select[name="ciudad"]').on('change', function() {
        var ciudad = $(this).val();

        $.ajax({
            url: '/get_departamento_ciudad_barrio/',
            data: {
                ciudad: ciudad
            },
            success: function(data) {
                $('select[name="barrio"]').removeAttr('disabled');
                $('select[name="barrio"]').empty();

                $(data.barrios).each(function(index, barrio) {
                    $('select[name="barrio"]').append('<option value="' + barrio + '">' + barrio + '</option>');
                });
            }
        });
    });
});
