define([
    'underscore',
    'backbone',
    'text!templates/index.html'
], function (_, Backbone, indexTemplate) {
    var IndexView = Backbone.View.extend({

        initialize: function () {
            this.template = _.template(indexTemplate);
        },

        render: function () {
            this.$el.html(this.template({}));
            return this;
        }
    });

    return IndexView;
});
