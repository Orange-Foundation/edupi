define([
    'backbone',
    'router'
], function (Backbone, router) {
    return {
        initialize: function () {
            router.initialize();
            Backbone.history.start();
        }
    };
});
