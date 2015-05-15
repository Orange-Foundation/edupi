define([
    'backbone'
], function (Backbone) {

    var BaseCollection = Backbone.Collection.extend({

        url: function () {
            var origUrl = Backbone.Collection.prototype.url.call(this);
            return origUrl + (origUrl.charAt(origUrl.length - 1) == '/' ? '' : '/');
        }

    });

    return BaseCollection;
});
