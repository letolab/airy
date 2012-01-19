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

        // process files via File API
        formFiles.each(function() {
            var files = this.files;
            var id = $(this).attr("name");

            toArray(files).forEach(function(file) {
                var fReader = new FileReader();

                fReader.onload = function(e) {
                    var result = e.target.result;
                    appendFiles(id, {'name': file.name, 'content': result});
                }

                fReader.readAsDataURL(file);
            });
        });

        var elems = 0;
        var inputs = formFiles.length
        function appendFiles(id, arg) {
            obj[id] = arg;
            elems++;
            if (elems == inputs) {
                callback(obj, data);
            }
        }

    }

});