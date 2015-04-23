define([
    'backbone',
    'router',
    'views/nav',
    'views/page_wrapper'
], function (Backbone, AppRouter, NavbarView, PageWrapperView) {

    var app;

    app = function () {
        // initialization
        var router = new AppRouter();
        var navbar, pageWrapper;

        // create the basic page structure
        $("body").append("<div id='wrapper'></div>");
        $("#wrapper").append("<div id='navbar'></div><div id='page-wrapper'></div>");
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
