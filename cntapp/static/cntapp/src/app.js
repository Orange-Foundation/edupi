define([
    'backbone',
    'router'
], function (Backbone, AppRouter) {

    var app = function () {
        // initialization
        var router = new AppRouter();

        return {
            getRouter: function () {
                return router;
            }
        };
    }();

    return app;
});
