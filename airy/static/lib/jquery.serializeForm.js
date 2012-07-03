$(function () {

    $.fn.serializeObject = function(){
        var obj = {};

        $.each( this.serializeArray(), function(i,o){
            var n = o.name,
                v = o.value;

            obj[n] = obj[n] === undefined ? v
                : $.isArray( obj[n] ) ? obj[n].concat( v )
                : [ obj[n], v ];
        });

        return obj;
    };

    $.fn.serializeForm = function(callback, data) {
        // process ordinary form fields
        var obj = $(this).serializeObject();

        function toArray(list) {
            return Array.prototype.slice.call(list || [], 0);
        }

        var formFiles = $(this).find('input[type="file"]:enabled');
        if (formFiles.length == 0) {
            callback(obj, data);
        }

        var elems = 0;
        var inputs = formFiles.length;

        function appendFiles(id, arg) {
            obj[id] = arg;
            elems++;
            if (elems == inputs) {
                callback(obj, data);
            }
        }

        if (formFiles.length > 0) {
            // process file uploads separately

            if (typeof(FileReader) == 'undefined') {

                // FileAPI not available, use iframe instead
                $(this).iframePostForm({
                    'json': true,
                    'complete': function(response) {
                        if (response.files) {
                            for (name in response.files) {
                                appendFiles(name, response.files[name]);
                            }
                        }
                    }
                })

            } else {

                // process files via File API
                formFiles.each(function() {
                    var files = this.files;
                    var id = $(this).attr("name");

                    if (toArray(files).length > 0) {

                        toArray(files).forEach(function(file) {
                            var fReader = new FileReader();

                            fReader.onload = function(e) {
                                var result = e.target.result;
                                appendFiles(id, {'name': file.name, 'content': result});
                            }

                            fReader.readAsDataURL(file);
                        });

                    } else {
                        appendFiles(id, null);
                    }

                });

                return false;
            }
        }

    }

});



/**
 * jQuery plugin for posting form including file inputs.
 *
 * Copyright (c) 2010 - 2011 Ewen Elder
 *
 * Licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 *
 * @author: Ewen Elder <ewen at jainaewen dot com> <glomainn at yahoo dot co dot uk>
 * @version: 1.1.1 (2011-07-29)
 *
 * Modified by LetoLab Ltd for Airy framework
 **/
(function ($)
{
    $.fn.iframePostForm = function (options)
    {
        var response,
            returnReponse,
            element,
            status = true,
            iframe;

        options = $.extend({}, $.fn.iframePostForm.defaults, options);


        // Add the iframe.
        if (!$('#' + options.iframeID).length)
        {
            $('body').append('<iframe id="' + options.iframeID + '" name="' + options.iframeID + '" style="display:none" />');
        }


        $(this).each(function ()
        {
            element = $(this);

            // Target the iframe.
            element.attr('target', options.iframeID);

            // Temporary store original URL (to send data later)
            element.attr('data-action', element.attr('action'));
            // Set URL to Airy form processor
            element.attr('action', '/airy/form/');
            // Set content type
            element.attr('enctype', 'multipart/form-data')

            iframe = $('#' + options.iframeID).load(function ()
            {
                response = iframe.contents().find('body');

                if (options.json)
                {
                    returnReponse = $.parseJSON(response.html());
                }

                else
                {
                    returnReponse = response.html();
                }

                options.complete.apply(this, [returnReponse]);

                iframe.unbind('load');

                setTimeout(function ()
                {
                    response.html('');
                }, 1);
            });

        });
    };


    $.fn.iframePostForm.defaults =
    {
        iframeID : 'iframe-post-form',       // Iframe ID.
        json : false,                        // Parse server response as a json object.
        post : function () {},               // Form onsubmit.
        complete : function (response) {}    // After response from the server has been received.
    };
})(jQuery);