define([
    'backbone',
    'router',
    'views/nav'
], function (Backbone, AppRouter, NavbarView) {

    var initHtml, app;

    initHtml = function () {
        $("body").append("<div id='wrapper'></div>");
        $("#wrapper").append("<div id='navbar'></div><div id='page-wrapper'></div>");
        new NavbarView({el: "#navbar"});
    };

    app = function () {
        // initialization
        var router = new AppRouter();
        initHtml();

        return {
            router: router,
            views: {}
        };
    }();

    return app;
});
