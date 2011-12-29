$.fn.serializeForm = function(callback) {
//    var serializedFiles = [];
    var obj = {};

    function toArray(list) {
        return Array.prototype.slice.call(list || [], 0);
    }

    $(this).find('input').each(function() {
        if (this.type == 'file' && 'files' in this && this.files.length > 0) {
            var files = this.files;
            var serializedFiles = [];
            var id = this.id;

            toArray(files).forEach(function(file) {
                var fReader = new FileReader();

                fReader.onload = function(e) {
                    var result = e.target.result;
                    serializedFiles.push({ 'name': file.name, 'content': result, 'type': 'file'});
                    if (serializedFiles.length == files.length) {
//                        appendFiles(id, serializedFiles);
                        appendFiles(id, result);
                    }
                }

                fReader.readAsDataURL(file);
            });
        }
    });

    var elems = 0;
    var inputs = $(this).find('input').length
    function appendFiles(id, arg) {
        obj[id] = arg;
        if (++elems == inputs - 1)
            callback(obj);
    }

}