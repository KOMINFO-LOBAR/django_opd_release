(function ($) {
    if (document.getElementById('slide_wrap')) {
        const timing = 5000; // 8000            
            
        new lc_micro_slider('#slide_wrap', {
            fixed_slide_type    : 'image',  
            slide_fx            : 'zoom-out',
            animation_time	    : 500, // 1000,
            slideshow_time	    : timing,
            nav_arrows          : true,  
            slideshow_cmd       : false,
            autoplay            : true,
            pause_on_hover      : true, // false
            addit_classes       : ['lcms_default_theme']    
        });
                                    
        //// ken burns effect
        let ken_burns_intval,
            curr_comb = '';
        
        document.getElementById('slide_wrap').addEventListener('lcms_slide_shown', (e) => {
            const $subj = e.target,
                slide_index = e.detail.slide_index;

            if(ken_burns_intval) {
                clearInterval(ken_burns_intval);    
            }
            ken_burns_intval = setInterval(() => {
                ken_burns_fx($subj, slide_index);
            }, timing);    

            ken_burns_fx($subj, slide_index);
        });
        
        const ken_burns_fx = function($subj, slide_index) {
                vert_opts     = ["top", "bottom"],
                horiz_opts    = ["left", "right"];
            
            if(document.getElementById('lcms_kenburns')) {
                document.getElementById('lcms_kenburns').remove();        
            }

            const vert_rule  = vert_opts[Math.floor(Math.random() * vert_opts.length)], 
                horiz_rule = horiz_opts[Math.floor(Math.random() * horiz_opts.length)];
                
            // force movement
            if(curr_comb == vert_rule+horiz_rule) {
                ken_burns_fx($subj, slide_index);      
            }
            
            
            let animation = {
                top: 0,
                right: 0,
                bottom: 0,
                left: 0
            };
            animation[ vert_rule ] = '-3%'; // '-20%';
            animation[ horiz_rule ] = '-3%';

            document.querySelector('#slide_wrap .lcms_slide[data-index="'+ slide_index +'"] .lcms_bg').animate(
                animation,
                {
                    duration: timing,
                    iterations: 1,
                    fill: 'forwards'
                }
            );       
        };  
    ;}  

})(jQuery);