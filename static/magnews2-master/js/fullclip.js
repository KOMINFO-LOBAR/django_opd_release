(function($) {
    // defaults full clip backround
    $.fn.fullClip = function(options) {
        var settings = $.extend({
        current: 0,
        images: [],
        category: [],
        title: [],
        admin: [],
        date: [],
        link: [],
        site: [],
        transitionTime: 1000,
        wait: 3000,
        static: false,
        //opacity: false,
        }, options);

        var elem = $(this);

        // preload images
        var i, end;
        for (i = 0, end = settings.images.length; i < end; ++i) {
            new Image().src = settings.images[i];        
        };
        
        if (settings.images.length == 1) settings.static = true;
        
        //if (settings.opacity == true)
        //    elem.find('img').css('opacity', 0);

        // sort out the transitions + specify vendor prefixes
        //$('.fullBackground')
        // $(this)
        elem.css('background-image', 'url(' + settings.images[settings.current] + ')')
            .css('-webkit-transition', + settings.transitionTime + 's ease-in-out')
            .css('-moz-transition', + settings.transitionTime + 'ms ease-in-out')
            .css('-ms-transition', + settings.transitionTime + 'ms ease-in-out')
            .css('-o-transition', + settings.transitionTime + 'ms ease-in-out')
            .css('transition', + settings.transitionTime + 'ms ease-in-out');

        // if only one image, set as static background
        if (settings.static) {
            elem.css('background-image', 'url(' + settings.images[settings.current] + ')');

            elem.find('.slider-category').html(settings.category[settings.current]);
            elem.find('.slider-title').html(settings.title[settings.current]);
            elem.find('.slider-site').html(settings.site[settings.current]);

            elem.find('.slider-admin').html(settings.admin[settings.current]);
            elem.find('.slider-date').html(settings.date[settings.current]);

            elem.find('.slider-link').attr("href", settings.link[settings.current]);
            elem.find('.slider-category').attr("href", settings.link[settings.current]);
            elem.find('.slider-title').attr("href", settings.link[settings.current]);
            return;
        };
        
        //elem.find('.slider-title').html('test');
        
        //$('.fullBackground').html(document.write('this = ' + this.find('.slider-category').text('aaaaa')));
        //$('.fullBackground').text('this = ' +   this.innerHTML);
        // set text
        //$("#slider-caption").text = "apa";
        //$('#slider-caption').fadeOut(500, function() {
        //    $(this).html(settings.header[settings.current]).fadeIn(500);
        //});

        // change the background image
        (function update() {
            settings.current = (settings.current + 1) % settings.images.length;
            //elem.find('.slider-category').html('test');
            elem.css('background-image', 'url(' + settings.images[settings.current] + ')');
                        
            elem.find('.slider-category').html(settings.category[settings.current]);
            elem.find('.slider-title').html(settings.title[settings.current]);
            elem.find('.slider-admin').html(settings.admin[settings.current]);
            elem.find('.slider-date').html(settings.date[settings.current]);
            
            elem.find('.slider-site').html(settings.site[settings.current]);

            elem.find('.slider-link').attr("href", settings.link[settings.current]);
            elem.find('.slider-category').attr("href", settings.link[settings.current]);
            elem.find('.slider-title').attr("href", settings.link[settings.current]);


            // Looping di indicator
            elem.find('.dot').removeClass('active2');
            elem.find('.dot').each(function(index) {
                //console.log(index);
                if (settings.current == index)
                    $(this).addClass('active2')
            });


            setTimeout(update, settings.wait);
        }());  
          
    };

    function multiply(x,y) {
        return x * y;
    };

    function refresh_img(elem, parent_img, settings) {
        parent_img.empty();
        parent_img.append(settings.searchPic[settings.current]);

        elem.find('img')
            .css('-webkit-transition', + settings.transitionTime + 's ease-in-out')
            .css('-moz-transition', + settings.transitionTime + 'ms ease-in-out')
            .css('-ms-transition', + settings.transitionTime + 'ms ease-in-out')
            .css('-o-transition', + settings.transitionTime + 'ms ease-in-out')
            .css('transition', + settings.transitionTime + 'ms ease-in-out');

        elem.find('a').attr('href', settings.link[settings.current]);

        //elem.find('.slider-category').html(settings.category[settings.current]);
        //if (settings.site[settings.current] != '')
        //    elem.find('.slider-title').html(settings.site[settings.current] + ', ' + settings.title[settings.current])
        //else 
        elem.find('.slider-title').html(settings.title[settings.current]);
        elem.find('.slider-site').html(settings.site[settings.current]);


        elem.find('.slider-admin').html(settings.admin[settings.current]);
        elem.find('.slider-date').html(settings.date[settings.current]);        

        elem.find('.dot').removeClass('active2');
        elem.find('.dot').each(function(index) {
            //console.log(index);
            if (settings.current == index) 
                $(this).addClass('active2')                                    
        });
    };            

    // Full clip Image
    $.fn.fullClipImg = function(options) {
        var settings = $.extend({
        current: 0,
        images: [],
        category: [],
        title: [],
        admin: [],
        date: [],
        link: [],
        site: [],
        transitionTime: 1000,
        wait: 3000,
        static: false,
        first_enter: true,     // for preload image
        searchPic: [],
        //opacity: false,
        }, options);

        var elem = $(this);
        var parent_img = elem.find('img').parent();
        // console.log('Data parent image = ');
        // console.log(parent_img);


        var timer;
        // preload images
        var i, end;
        //var searchPic = [];
        if (settings.first_enter) {            
            for (i = 0, end = settings.images.length; i < end; ++i) {
                //console.log('Data = ');
                settings.searchPic[i] = new Image();
                //console.log('url(' + settings.images[i] + ')');
                
                settings.searchPic[i].src = settings.images[i];        
                //console.log(settings.searchPic[i]);

                //console.log( multiply(2, 2) );
            }
            settings.first_enter = false;
        };

        //end = settings.images.length;
        //for (i = 0; i < end; ++i) {
        //    settings.images[i] = Image(i)
        //}
        
        if (settings.images.length == 1) settings.static = true;
        

        //elem.find('.dot').click(function(){});   
        elem.find('#dot0').on('click',function(ev) {
            //alert('ev0'); //or whatever you're trying to accomplish here
            settings.current = 0; //2;
            //setTimeout(update, 0);
            clearTimeout(timer);
            refresh_img(elem, parent_img, settings);
            //update()
            timer = setTimeout(this.update, settings.wait);
        });

        elem.find('#dot1').on('click',function(ev) {
            //alert('ev1'); //or whatever you're trying to accomplish here
            settings.current = 1;//0;
            //setTimeout(update, 0);
            clearTimeout(timer);
            refresh_img(elem, parent_img, settings);
            timer = setTimeout(this.update, settings.wait);
        });

        elem.find('#dot2').on('click',function(ev) {
            //alert('ev2'); //or whatever you're trying to accomplish here
            settings.current = 2;//1;
            //setTimeout(update, 0);
            clearTimeout(timer);
            refresh_img(elem, parent_img, settings);
            timer = setTimeout(this.update, settings.wait);
        });

        //if (settings.opacity == true)
        //    elem.find('img').css('opacity', 0);

        // sort out the transitions + specify vendor prefixes
        //$('.fullBackground')
        // $(this)
        //attr('src', settings.images[settings.current])

        refresh_img(elem, parent_img, settings);
        // parent_img.empty();
        // parent_img.append(settings.searchPic[settings.current]);

        // elem.find('img')
        //     .css('-webkit-transition', + settings.transitionTime + 's ease-in-out')
        //     .css('-moz-transition', + settings.transitionTime + 'ms ease-in-out')
        //     .css('-ms-transition', + settings.transitionTime + 'ms ease-in-out')
        //     .css('-o-transition', + settings.transitionTime + 'ms ease-in-out')
        //     .css('transition', + settings.transitionTime + 'ms ease-in-out');

        // if only one image, set as static background
        if (settings.static) {
            refresh_img(elem, parent_img, settings);
            //console.log('url(' + settings.images[settings.current] + ')');
            //elem.find('img').attr('src', settings.searchPic[settings.current] );
            // parent_img.empty();
            // parent_img.append(settings.searchPic[settings.current]);

            // elem.find('img')
            //     .css('-webkit-transition', + settings.transitionTime + 's ease-in-out')
            //     .css('-moz-transition', + settings.transitionTime + 'ms ease-in-out')
            //     .css('-ms-transition', + settings.transitionTime + 'ms ease-in-out')
            //     .css('-o-transition', + settings.transitionTime + 'ms ease-in-out')
            //     .css('transition', + settings.transitionTime + 'ms ease-in-out');

            // elem.find('a').attr('href', settings.link[settings.current]);

            // //elem.find('.slider-category').html(settings.category[settings.current]);
            // //if (settings.site[settings.current] != '')
            // //    elem.find('.slider-title').html(settings.site[settings.current] + ', ' + settings.title[settings.current])
            // //else 
            // elem.find('.slider-title').html(settings.title[settings.current]);
            // elem.find('.slider-site').html(settings.site[settings.current]);


            // elem.find('.slider-admin').html(settings.admin[settings.current]);
            // elem.find('.slider-date').html(settings.date[settings.current]);

            //elem.find('.slider-link').attr("href", settings.link[settings.current]);
            //elem.find('.slider-category').attr("href", settings.link[settings.current]);
            //elem.find('.slider-title').attr("href", settings.link[settings.current]);
            return;
        };
        
        //elem.find('.slider-title').html('test');
        
        //$('.fullBackground').html(document.write('this = ' + this.find('.slider-category').text('aaaaa')));
        //$('.fullBackground').text('this = ' +   this.innerHTML);
        // set text
        //$("#slider-caption").text = "apa";
        //$('#slider-caption').fadeOut(500, function() {
        //    $(this).html(settings.header[settings.current]).fadeIn(500);
        //});

        // change the background image
        (function update() {           
            settings.current = (settings.current + 1) % settings.images.length;
            
            //console.log(settings.images[settings.current]);
            //elem.find('.slider-category').html('test');
            
            //elem.find('img').css('opacity: 0.0');
            //elem.find('img').remove().append(settings.searchPic[settings.current]);
            refresh_img(elem, parent_img, settings);
            // parent_img.empty();
            // parent_img.append(settings.searchPic[settings.current]);

            // elem.find('img')
            //     .css('-webkit-transition', + settings.transitionTime + 's ease-in-out')
            //     .css('-moz-transition', + settings.transitionTime + 'ms ease-in-out')
            //     .css('-ms-transition', + settings.transitionTime + 'ms ease-in-out')
            //     .css('-o-transition', + settings.transitionTime + 'ms ease-in-out')
            //     .css('transition', + settings.transitionTime + 'ms ease-in-out');

            // //elem.find('img').fadeTo( "slow", 1.0 );

            // //elem.find('img').animate({opacity: '0.0'}, 500, function () {
            //     //elem.css('background-image', 'url(' + settings.images[settings.current] + ')')
            // //    elem.find('img').attr('src', settings.images[settings.current]);
            // //    elem.find('img').css('opacity', '1.0');
            // //});

            // elem.find('a').attr('href', settings.link[settings.current]);
            // //elem.find('.slider-category').html(settings.category[settings.current]);
            // //elem.find('.slider-title').html(settings.site[settings.current] + ', ' + settings.title[settings.current]);
            // //if (settings.site[settings.current] != '')
            // //    elem.find('.slider-title').html(settings.site[settings.current] + ', ' + settings.title[settings.current])
            // //else 
            // elem.find('.slider-title').html(settings.title[settings.current]);
            // elem.find('.slider-site').html(settings.site[settings.current]);

            // elem.find('.slider-admin').html(settings.admin[settings.current]);
            // elem.find('.slider-date').html(settings.date[settings.current]);


            // Looping di indicator
            // elem.find('.dot').removeClass('active2');
            // elem.find('.dot').each(function(index) {
            //     //console.log(index);
            //     if (settings.current == index) 
            //         $(this).addClass('active2')                                    
            // });
          
            
            //$('#foo').bind('click', function() {
            //    alert('User clicked on "foo."');
            //});

            //elem.find('#dot0').on('click',function(ev) {            
            //    alert('pp');
                //settings.current = 0;
                //setTimeout(update, 0);
            //});

            //elem.find('.slider-link').attr("href", settings.link[settings.current]);
            //elem.find('.slider-category').attr("href", settings.link[settings.current]);
            //elem.find('.slider-title').attr("href", settings.link[settings.current]);
            timer = setTimeout(update, settings.wait);
        }());
        
    };

    /* Create by ione 
    $.fn.videoClip = function() {
        var elem = $(this);

        try {
            var srcOld = elem.children('iframe').attr('src');

            $('#write-here').html('srcOld.title');

            elem.find('[data-target="#modal-video-01"]').on('click',function(){
                elem.children('iframe')[0].src += "&autoplay=1";

                setTimeout(function(){
                    elem.css('opacity','1');
                },300);      
            });

            elem.find('[data-dismiss="modal"]').on('click',function(){
                elem.children('iframe')[0].src = srcOld;
                elem.css('opacity','0');
            });
        } catch(er) {console.log(er);}
        
    }; */
    

}(jQuery));
