define([
    'backbone'
], function (Backbone) {

    var BaseModel = Backbone.Model.extend({

        url: function () {
            var origUrl = Backbone.Model.prototype.url.call(this);
            return origUrl + (origUrl.charAt(origUrl.length - 1) == '/' ? '' : '/');
        }

    });

    return BaseModel;
});
