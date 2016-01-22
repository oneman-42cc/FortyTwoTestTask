(function($) {
    $( document ).ready(function() {

        var methods = {

            init : function( options ) {
                window.__admin_media_prefix__ = "/static/admin/";
            },

            save : function( e ) {

                var
                    $form = $(e),
                    Data = new FormData(e);

                console.log("Start to save a form.");

                methods.handleLoader.apply( this, ["show"] );
                methods.disableElements.apply( this, [$form, "disable"] );

                $.ajax({
                    url: "/edit/",
                    type: "POST",
                    data: Data,
                    cache: false,
                    processData: false,
                    contentType: false,
                    success: function(jsondata){
                        console.log("A form was save successfully.");
                        window.location.href = jsondata.success_url;
                    },
                    error : function(xhr, errmsg, err) {

                        var
                            jsondata = $.parseJSON(xhr.responseText);

                        $form.replaceWith(jsondata.form);
                        methods.initWidgets.apply( this, [] );

                    }
                });

            },

            disableElements : function($form, action) {

                var
                    $photo = $form.find("label[for='id_photo']"),
                    $inputs = $form.find("input, textarea"),
                    $calendar = $form.find(".datetimeshortcuts");

                if (action == "enable" ) {
                    $inputs.prop("disabled", false);
                    $photo.removeClass("hd");
                    $calendar.removeClass("hd");
                }

                if (action == "disable" ) {
                    $inputs.prop("disabled", true);
                    $photo.addClass("hd");
                    $calendar.addClass("hd");
                }

            },

            prepareFormData : function (form, string) {

                if (string) {

                    var _data = "";
                    $.each( form[0], function( name, field ) {
                        _data += field.name + "=" + field.value + "&";
                    });

                    return _data.substring(0, _data.length - 1);
                }

                var _data = {}
                $.each( form[0], function( name, field ) {
                    _data[field.name] = field.value;
                });
                
                return _data;
            },

            initWidgets : function() {
                // Init popup calendar widget.
                DateTimeShortcuts.init();
            },

            handleLoader : function(action) {

                var
                    $loader = $("span.ajax-loader");

                switch(action) {
                    case "show":
                        $loader.removeClass("hd");
                        break;
                    case "hide":
                        $loader.addClass("hd");
                        break;
                    default:
                        $loader.addClass("hd");
                }

            }

        };

        $.ProfileUpdateForm = function(method) {
            if ( methods[method] ) {
                return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
            } else if ( typeof method === 'object' || ! method ) {
                return methods.init.apply( this, arguments );
            } else {
                $.error( 'Has no jQuery.ProfileUpdateForm method ' +  method + "().");
            } 
        }

        $.ProfileUpdateForm();
        
    });
})(jQuery);