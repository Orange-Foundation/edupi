define([
    'backbone'
], function (Backbone) {
    var Directory = Backbone.Model.extend({

        urlRoot: '/api/directories',

        url: function () {
            var origUrl = Backbone.Model.prototype.url.call(this);
            return origUrl + (origUrl.charAt(origUrl.length - 1) == '/' ? '' : '/');
        },

        defaults: {
            id: -1
        }
    });

    return Directory;
});
