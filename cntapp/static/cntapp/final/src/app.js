define([
    'underscore',
    'backbone',
    'router',
], function (_, Backbone, AppRouter, NavbarView, PageWrapperView, containerTemplate) {

    var app;

    app = function () {
        // initialization
        var router = new AppRouter();

        return {
            router: router
        };
    }();

    return app;
});
