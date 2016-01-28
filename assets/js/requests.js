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

            savePriority : function(e) {

                var
                    $element = $(e),
                    $form = $element.parents("form"),
                    $input_priority = $form.find("input[name='priority']"),
                    originalPriority = $input_priority.attr("original-value"),
                    $loader = $form.find("span.ajax-loader"),
                    ajaxData = methods.prepareFormData.apply( this, [$form] );

                // Before send AJAX request check or the priority was changed.
                if (ajaxData["priority"] == originalPriority) {
                    console.log("No need to update the priority.");
                    return true;
                }

                ajaxData["event"] = "priority-update";
                ajaxData["csrfmiddlewaretoken"] = methods.getCookie.apply(this, ["csrftoken"]);

                methods.handleLoader.apply( this, [$loader, "show"] );

                _AJAX = $.ajax({
                    url: "/requests/",
                    type: "POST",
                    data: ajaxData,
                    success: function(data){
                        // Print info to console.
                        console.log("Priority updated successfully.");
                    }
                });

            },

            changeOrder : function(e, new_order) {

                var
                    $element = $(e),
                    $loader = $element.find("span.ajax-loader"),
                    ajaxData = {
                        "new-order": new_order,
                        "event": "change-order",
                        "csrfmiddlewaretoken": methods.getCookie.apply(this, ["csrftoken"]),
                    }

                methods.handleLoader.apply( this, [$loader, "show"] );

                _AJAX = $.ajax({
                    url: "/requests/",
                    type: "POST",
                    data: ajaxData,
                    success: function(data){
                        // Print info to console.
                        console.log("Order changed successfully.");
                        location.reload();
                    }
                });

            },

            prepareFormData : function (form, string) {

                if (string) {

                    var _data = "";
                    $.each( form.serializeArray(), function( name, field ) {
                        _data += field.name + "=" + field.value + "&";
                    });

                    return _data.substring(0, _data.length - 1);
                }

                var _data = {}
                $.each( form.serializeArray(), function( name, field ) {
                    _data[field.name] = field.value;
                });
                
                return _data;
            },

            handleLoader : function(loader, action) {

                switch(action) {
                    case "show":
                        loader.removeClass("hd");
                        break;
                    case "hide":
                        loader.addClass("hd");
                        break;
                    default:
                        loader.addClass("hd");
                }

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

        // $.RequestsList();
        
    });
})(jQuery);