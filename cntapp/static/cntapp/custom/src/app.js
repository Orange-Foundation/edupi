define([
    'underscore', 'backbone', 'router',
    'views/nav', 'views/page_wrapper',
    'collections/directories',
    'text!templates/container.html'
], function (_, Backbone, AppRouter,
             NavbarView, PageWrapperView,
             DirectoriesCollection,
             containerTemplate) {

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
        directoriesCollection.fetch({
            reset: true,
            success: function () {
                $("body").html(_.template(containerTemplate)());
                $("#navbar").html(navbar.render().el);
                $("#page-wrapper").html(pageWrapper.render().el);
                Backbone.history.start();
            }
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
            isLoggedIn: false
        };
    }();

    return app;
});
