(function($) {
    $( document ).ready(function() {

        var methods = {

            init : function( options ) {

                $(window).on("focus", function() {
                    setTimeout(function() {
                        // On focus reset counter of new requests and page
                        // meta title.
                        _NUMBER = 0;
                        methods.updateTitle.apply( this, [true] );
                        // And abort existing ajax request.
                        _AJAX.abort();
                    }, 500);
                });

                methods.getRequests.apply( this, [] );
            },

            getCookie : function( name ) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            },

            getRequests : function() {

                var
                    $table = $("table.rp");

                console.log("Start new request.");
                console.log(_TITLE);

                _AJAX = $.ajax({
                    url: "/requests/async/",
                    type: "POST",
                    data: ({
                        "numbernew": _NUMBER,
                        "csrfmiddlewaretoken": methods.getCookie.apply(this, ["csrftoken"]),
                    }),
                    success: function(data){
                        // Print info to console.
                        console.log("Request finished success:");
                        console.log(data);
                        // Update page meta title - add number new requests.
                        if (data.requests_new) {
                            _NUMBER = data.requests_new
                            methods.updateTitle.apply( this, [] );
                        }
                        // Update a list of requests.
                        $table.empty().append(data.requests_list);
                        // Send request again.
                        methods.getRequests.apply( this, [] );
                    },

                    error: function (xhr, ajaxOptions, thrownError) {
                        // Print info about 
                        console.log("Request finished with errors:");
                        console.log(xhr.status + ": " + xhr.responseText);
                        // Send request again.
                        methods.getRequests.apply( this, [] );
                    }
                });
            },

            updateTitle : function(reset) {

                var
                    $metatitle = $("title");
                    text_ = reset ? _TITLE : ("(" + _NUMBER + ") " + _TITLE);

                $metatitle.text(text_);

            },

        };

        $.RequestsList = function(method) {
            if ( methods[method] ) {
                return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
            } else if ( typeof method === 'object' || ! method ) {
                return methods.init.apply( this, arguments );
            } else {
                $.error( 'Has no jQuery.RequestsList method ' +  method + "().");
            } 
        }

        _AJAX = null;
        _NUMBER = 0;
        _TITLE = $("title").text();

        $.RequestsList();
        
    });
})(jQuery);