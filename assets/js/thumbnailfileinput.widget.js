(function($) {
    $( document ).ready(function() {

        var methods = {

            init : function( options ) {},

            change : function(e) {

                var
                    $container = $(".wThumbnailField"),
                    $span = $container.find(".fileName"),
                    $input = $container.find("input[type='file']");

                $span.text("to " + $input.val());

            },

        };

        $.ThumbnailFileInput = function(method) {
            if ( methods[method] ) {
                return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
            } else if ( typeof method === 'object' || ! method ) {
                return methods.init.apply( this, arguments );
            } else {
                $.error( 'Has no jQuery.ThumbnailFileInput method ' +  method + "().");
            } 
        }

        $.ThumbnailFileInput();
        
    });
})(jQuery);