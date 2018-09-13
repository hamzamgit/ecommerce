$(document).ready(function () {

    $('input[type=radio]').each(function () {
        $(this).css('display', 'none');
    });

    $('[for*="id_rating_rating_"]').each(function () {
        $(this).addClass('fa');
        $(this).addClass('fa-star-o');
    });

    $('#rating_submit').click(function () {
        $('#rating_submit').animate({opacity: 0.6}, 200);
        $('#rating_submit').animate({opacity: 1}, 200);
        var not_checked = true;
        $('[id *="id_rating_rating_"]').each(function () {
            var c = $(this).attr('checked');
            if (c === "checked") {
                console.log(c + not_checked);
                not_checked = false;
            }
        });
        if (not_checked) {
            if (($('#rating-form')).attr('novalidate') !== "") {
                $('#rating_error').html("Select the rating");
            }
            else{
            $(this).addClass('active');
            }

        }
    });

    $('[id*="id_rating_rating_"]').click(function () {
        $('label[class="fa fa-star"]').each(function () {
            $(this).removeClass('fa-star');
            $(this).addClass('fa-star-o');
        });
        var id = $(this).attr('id');
        id = id.slice(id.length - 1);
        for (var i = id; i >= 0; i--) {
            var final_id = 'id_rating_rating_' + i;
            $('label[for=' + final_id + ']').removeClass('fa-star-o');
            $('label[for= ' + final_id + ']').addClass('fa-star');
            $('#rating_error').html("");
        }
    });

    if (getQueryVariable('active_tab') === 'reviews') {
        $('a[href="#product-reviews"]').click();
        setTimeout(function () {
            // $('a[href="#product-reviews"]').focus();
            $('html, body').animate({scrollTop: ($('a[href="#product-reviews"]').offset().top)}, 500);
        }, 500);
    }
    if (getQueryVariable('active_tab') === 'error') {
        $('a[href="#product-reviews"]').click();
        setTimeout(function () {
            $('html, body').animate({scrollTop: ($('.review-form').offset().top)}, 500);
        }, 500);
    }

});


function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) === variable) {
            return decodeURIComponent(pair[1]);
        }
    }
    return '';
}
