define([
    'backbone'
], function (Backbone) {
    return Backbone.Model.extend({
        urlRoot: '/api/directories',
        defaults: {
            id: -1
        }
    });
});
