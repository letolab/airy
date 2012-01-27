var project;

project = {

    init: function() {
        project.users.init();
    },

    users: {
        init: function() {
            $('.content-editable').live('click', function() {
                if ( $(this).attr('contenteditable') == undefined ) {
                    $(this).editableText({ newlinesEnabled: false });
                    $(this).click();
                }
            });

            $('.content-editable').live('change', function() {
                airy.request('post', '/accounts/profile/change/', { 'field': $(this).attr('field'), 'value': $(this).text() }, true);
            });

        },

        picture_init: function() {
            var holder = document.getElementById('profile-picture');

            if (typeof window.FileReader === 'undefined') {
                $('#profile-picture-drop').remove();
                return;
            }

            holder.ondragover = function () { $(this).addClass('drop'); return false; };
            holder.ondragend = function () { $(this).removeClass('drop'); return false; };
            holder.ondrop = function (e) {
                $(this).removeClass('drop');
                e.preventDefault();

                var file = e.dataTransfer.files[0],
                    reader = new FileReader();

                reader.onload = function (event) {
                    var data = {'picture': {'name': file.name, 'content': event.target.result}};
                    airy.request('post', '/accounts/profile/picture/upload', data, true);
                };
                reader.readAsDataURL(file);

                return false;
            };
        }
    }

}

$(function() {
    project.init();
});