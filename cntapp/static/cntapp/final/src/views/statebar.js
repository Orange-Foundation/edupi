define([
    'underscore',
    'backbone',
    'text!templates/statebar.html'
], function (_, Backbone, navbarTemplate) {

    var STATEBAR_TEMPLATE = _.template(navbarTemplate);

    var StateBarView = Backbone.View.extend({

        initialize: function () {
        },

        render: function () {
            this.$el.html(STATEBAR_TEMPLATE());
            return this;
        }
    });

    return StateBarView;
});
