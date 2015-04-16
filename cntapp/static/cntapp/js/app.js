define([
    'jquery',
    'underscore',
    'backbone',
    'router'
], function ($, _, Backbone, router) {
    return {
        initialize: function () {
            router.initialize();
            Backbone.history.start();
        }
    };
});
