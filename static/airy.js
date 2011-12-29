var airy;

airy = {
    socket: null,
    history: null,
    initialized: false,

    init: function() {
        if (!airy.initialized) {
            airy.history = window.History;
            airy.configure.history();
            airy.configure.links();
            airy.configure.forms();
            airy.initialized = true;
        }
        airy.request('get', airy.history.getState().hash);
    },

    request: function(method, url, data) {
        if (airy.history.getState().hash == url) {
            if (data) {
                airy.socket.emit(method, url, data);
            } else {
                airy.socket.emit(method, url);
            }
        } else {
            airy.history.pushState({method: method, data: data}, null, url);
        }
    },

    set_cookie: function(name, value, options) {
        $.cookie(name, value, options)
    },

    ui: {
        insert: function(target, data) {
            $(target).html(data);
        },
        append: function(target, data) {
            $(target).append(data);
        }
    },

    configure: {
        history: function() {
            airy.history.Adapter.bind(window, 'statechange', function() {
                var State = airy.history.getState();
                if (State.data.data) {
                    airy.socket.emit(State.data.method, State.hash, State.data.data);
                } else {
                    airy.socket.emit(State.data.method, State.hash);
                }
            });
        },
        links: function() {
            $('a').live('click', function() {
                if (airy.options.is_airy_link($(this))) {
                    airy.request('get', $(this).attr('href'));
                    return false;
                }
            });
        },
        forms: function() {
            $('form').live('submit', function() {
                if (airy.options.is_airy_form($(this))) {
                    var form_url = airy.history.getState().hash;
                    if ($(this).attr('action').length > 0) {
                        form_url = $(this).attr('action');
                    }
                    if ($(this).attr('method').toLowerCase() == 'get') {
                        airy.request('get', form_url+'?'+$(this).serialize());
                    } else if ($(this).attr('method').toLowerCase() == 'post') {
                        airy.request('post', form_url, $(this).serializeObject());
                    }
                    return false;
                }
            });
        }
    },

    options: {
        is_airy_link: function(link) {
            if (link.attr('href') && !link.attr('target') && !link.hasClass('no-airy')) {
                return true;
            }
            return false;
        },

        is_airy_form: function(form) {
            if (!form.hasClass('no-airy')) {
                return true;
            }
            return false;
        }
    }
}

$(function() {

    airy.socket = new io.connect("http://" + window.location.host);

    airy.socket.on('connect', function() {
        airy.init();
    });

    airy.socket.on('execute', function(data) {
        eval(data);
    });

});


