// Custom function, create by Ione3

function show_popup() {
    if (localStorage.getItem('HasSeenPopup') == null) {
        $(window).on('load', function() {
            $('#modal-video-01').modal('show');
        });

        localStorage.setItem('HasSeenPopup','True');
    }   
};

function show_modal(pURL){
    // $('.video-mo-02').css('opacity','1');
    // setTimeout(function(){
    //     $('.video-mo-02').css('opacity','0');
    // },300);
    //$('.video-mo-02').html('<iframe width="853" height="480" src="https://www.youtube.com/embed/8KDOFMAhWCc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>');
    // https://www.youtube.com/embed/_P7FX8rhXk4
    // alert(pURL)
    // pURL = "https://www.youtube.com/embed/yZ9gUeNUt5c";
    // height="427"
    $('.video-mo-02').html('<iframe frameborder="0" height="600" src="'+ pURL + '?autoplay=0" title="YouTube video player" width="759" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>');
    
    //$('.video-mo-02').children('iframe')[0].src += "?autoplay=1";
    $('#modal-video-02').modal();
};

function show_modal_image(pURL){
    //alert(pURL);
    // $('.video-mo-02').css('opacity','1');
    // setTimeout(function(){
    //     $('.video-mo-02').css('opacity','0');
    // },300);
    //$('.video-mo-02').html('<iframe width="853" height="480" src="https://www.youtube.com/embed/8KDOFMAhWCc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>');
    // https://www.youtube.com/embed/_P7FX8rhXk4
    //alert(pURL)
    //$('.video-mo-01').html('<iframe frameborder="0" height="427" src="'+ pURL + '?autoplay=1" title="YouTube video player" width="759" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>');
    //alert(pURL);
    $('#modal-video-03').find('.video-mo-03').html('<img class="img-fluid img-thumbnail" src="'+ pURL +'" alt="IMG">');
    //$('.video-mo-02').children('iframe')[0].src += "?autoplay=1";
    $('#modal-video-03').modal();
};

// (function($) {
$(document).ready(function() {
    $('#modal-video-02').on('hide.bs.modal', () => {
        // console.log($('.video-mo-02').html());
        $('.video-mo-02').find('iframe').attr('src', '');
        // console.log($('.video-mo-02').html());
    });

    // Perbaiki isi berita, untuk tag ul ol dll
    $('.isi-berita p').addClass("f1-s-11 cl6 p-b-25 text-justify");
    $('.isi-berita ol').css(
        {
            'display': 'block',
            'list-style-type': 'decimal',
            'margin-top': '1em',
            'margin-bottom': '1em',
            'margin-left': '0',
            'margin-right': '0',
            'padding-left': '40px',
        }
    ); 

    $('.isi-berita ul').css(
        {
            'display': 'block',
            'list-style-type': 'disc',
            'margin-top': '1em',
            'margin-bottom': '1em',
            'margin-left': '0',
            'margin-right': '0',
            'padding-left': '40px',
        }
    );

    $('.isi-berita blockquote').css(
        {
            'display': 'block',
            'margin-top': '1em',
            'margin-bottom': '1em',
            'margin-left': '40px',
            'margin-right': '40px',
        }
    );

    $('.isi-berita img').removeAttr("style");
    $('.isi-berita img').addClass('img-fluid'); // bootstratp 4   

    
    // loader show
// }(jQuery));
});
