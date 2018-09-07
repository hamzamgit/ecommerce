$(document).ready(function () {

    var title = $('#id_rating_title').val();
    var revierw = $('#id_rating_review').val();

    // $('#rating_submit').click(function () {
    //     if (!($('#id_rating_rating_0').parent().hasClass("fa-star"))) {
    //         $('#rating_error').html("Select the rating");
    //     }
    //     });

       $('#rating_submit').click(function () {
        var not_checked = true;
        $('[id *="id_rating_rating_"]').each(function () {
            var c = $(this).attr('checked');
            if (c == "checked") {
                not_checked = false;
            }
        });
        if (not_checked) {
            $('#rating_error').html("Select the rating");
        }
    });

    $('input[type=radio]').each(function () {
        $(this).css('display', 'none');});

    $('[for*="id_rating_rating_"]').each(function () {
        $(this).addClass('fa');
        $(this).addClass('fa-star-o');
    });

    $('[id*="id_rating_rating_"]').click(function () {

        $('label[class="fa fa-star"]').each(function () {
            $(this).removeClass('fa-star');
            $(this).addClass('fa-star-o');
        });
        var id = $(this).attr('id');
        id = id.slice(id.length - 1);
        for (var i = id; i >= 0; i--){
            var final_id = 'id_rating_rating_' + i;
            $('label[for=' + final_id + ']').removeClass('fa-star-o');
            $('label[for= ' + final_id + ']').addClass('fa-star');
            $('#rating_error').html("");
          }
    });




});

