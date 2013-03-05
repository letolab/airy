var airy;

airy = {
    socket: null,
    history: null,
    initialized: false,

    defaults: {
        'method': 'get',
        'change_state': false,
        'callback': null
    },

    init: function() {
        if (!airy.initialized) {
            airy.history = window.History;
            airy.configure.history();
            airy.configure.links();
            airy.configure.forms();
            airy.initialized = true;
        }
        airy.request('get', airy.history.getState().hash);
        airy.socket.emit('set_state', airy.history.getState().hash);
    },

    call: function(params) {
        var options = $.extend({}, airy.defaults, params);
        var url = airy.util.fix_url(airy.history.getState().hash);
        options.url = airy.util.fix_url(options.url);
        if (url == options.url || !options.change_state) {
            var params = [options.method, options.url];
            if (options.data)
                $.merge(params, [options.data]);
            if (typeof(options.callback) == "function")
                $.merge(params, [options.callback]);
            airy.socket.emit.apply(airy.socket, params);
        } else {
            airy.history.pushState(options, null, options.url);
        }
    },

    request: function(method, url, data, nostate) {
        // deprecated functionality
        if (airy.history.getState().hash == url || nostate) {
            airy.call({method: method, url: url, data: data, change_state: !nostate});
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
        },
        prepend: function(target, data) {
            $(target).prepend(data);
        },
        remove: function(target) {
            $(target).remove();
        },
        after: function(target, data) {
            $(target).after(data);
        },
        title: function(text) {
            document.title = text;
        },
        meta: {
            description: function(text) {
                var desc = $('head meta[name="description"]').first();
                if (desc) {
                    desc.attr('value', text);
                }
            }
        },
        redirect: function(url) {
            airy.history.pushState({}, null, url);
        }
    },

    configure: {
        history: function() {
            airy.history.Adapter.bind(window, 'statechange', function() {
                var State = airy.history.getState();
                airy.call({method: State.data.method, url: State.hash, data: State.data.data, change_state: false});
                airy.socket.emit('set_state', State.hash);
            });
        },
        links: function() {
            $('a').live('click', function() {
                if (airy.options.is_airy_link($(this))) {
                    airy.call({url: $(this).attr('href'), change_state: !airy.options.no_state_change(this)});
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
                    if ($(this).attr('data-action')) {
                        form_url = $(this).attr('data-action');
                        $(this).attr('action', form_url);
                    }
                    if ($(this).attr('method').toLowerCase() == 'get') {
                        airy.request('get', form_url+'?'+$(this).serialize(), null, airy.options.no_state_change($(this)));
                        return false;
                    } else if ($(this).attr('method').toLowerCase() == 'post') {
                        return $(this).serializeForm(function(data, form) {
                            airy.request('post', form_url, data, airy.options.no_state_change(form));
                        }, $(this));
                    }
                }
            });
        }
    },

    options: {
        is_airy_link: function(link) {
            if (!link.attr('href')) {
                return false;
            }
            if (link.attr('href') && !link.attr('target') && !link.attr('nofollow') && !link.hasClass('no-airy')) {
                return true;
            }
            return false;
        },

        is_airy_form: function(form) {
            return !form.hasClass('no-airy');
        },

        no_state_change: function(item) {
            // when true airy will attempt to change the URL
            return $(item).hasClass('no-airy-state');
        }
    },

    util: {
        fix_url: function(url) {
            if (url.indexOf('.') == 0) {
                url = url.substring(1);
            }
            if (url.indexOf('/') != 0) {
                url = "/"+url;
            }
            return url;
        }
    }
}

$(function() {

    airy.socket = new io.connect(window.location.protocol + "//" + window.location.host, {'connect timeout': 1000});

    airy.socket.on('connect', function() {
        airy.init();
    });

    airy.socket.on('execute', function(data) {
        try {
            eval(data);
        } catch(err) {

        }
    });

});


