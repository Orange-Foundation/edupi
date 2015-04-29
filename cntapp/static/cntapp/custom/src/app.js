define([
    'underscore',
    'backbone',
    'router',
    'views/nav',
    'views/page_wrapper',
    'text!templates/container.html'
], function (_, Backbone, AppRouter, NavbarView, PageWrapperView, containerTemplate) {

    var app;

    app = function () {
        // initialization
        var router = new AppRouter();
        var navbar, pageWrapper;

        $("body").html(_.template(containerTemplate)());

        navbar = new NavbarView({el: "#navbar"});
        pageWrapper = new PageWrapperView({el: "#page-wrapper"}).render();

        return {
            router: router,
            views: {
                navbar: navbar,
                pageWrapper: pageWrapper
            }
        };
    }();

    return app;
});
