define([
    'underscore', 'backbone',
    'router',
    'views/nav', 'views/page_wrapper',
    'collections/directories',
    'text!templates/container.html',

    'bootstrap',
    'bootstrap_editable',
    'bootstrap_table',
    'bootstrap_table_editable',
    'i18n'
], function (_, Backbone,
             AppRouter,
             NavbarView, PageWrapperView,
             DirectoriesCollection,
             containerTemplate,
             i18n
) {

    var app,
        csrfToken,
        getCookie,
        csrfSafeMethod;

    getCookie = function (name) {
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
    };

    csrfSafeMethod = function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    csrfToken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        }
    });

    app = function () {
        // initialization

        var router = new AppRouter();
        var navbar, pageWrapper,
            directoriesCollection;

        navbar = new NavbarView();
        pageWrapper = new PageWrapperView();
        directoriesCollection = new DirectoriesCollection();

        // 1. get i18n resources
        // 2. get directories
        // 3. render page structure and start the Backbone app

        $.i18n.init({
            resGetPath: '/static/cntapp/custom/locales/__lng__/__ns__.json',
            lng: getCookie('i18next') || navigator.language || navigator.userLanguage
        }, function () {
            directoriesCollection.fetch({
                reset: true,
                success: function () {
                    var body = $("body");
                    body.html(_.template(containerTemplate)());
                    $("#navbar").html(navbar.render().el);
                    $("#page-wrapper").html(pageWrapper.render().el);
                    body.i18n();
                    Backbone.history.start();
                }
            });
        });


        return {
            router: router,
            views: {
                navbar: navbar,
                pageWrapper: pageWrapper
            },
            collections: {
                directories: directoriesCollection
            },
            apiRoots: {
                directories: '/api/directories/',
                documents: '/api/documents/'
            },
            csrfToken: csrfToken,
            getCookie: getCookie
        };
    }();

    return app;
});
