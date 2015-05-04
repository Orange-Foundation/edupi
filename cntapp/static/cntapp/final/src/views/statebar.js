define([
    'underscore',
    'backbone',
    'text!templates/statebar.html'
], function (_, Backbone, navbarTemplate) {

    var STATEBAR_TEMPLATE = _.template(navbarTemplate);

    var StateBarView = Backbone.View.extend({

        initialize: function (options) {
            // the path is a collection of directories
            this.path = options.path;
            this.listenTo(this.path, 'change', this.render);
        },

        render: function () {
            var context = {
                path: this.path.models
            };
            this.$el.html(STATEBAR_TEMPLATE(context));
            return this;
        }
    });

    return StateBarView;
});
