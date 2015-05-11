define([
    'underscore',
    'backbone',
    'text!templates/navbar.html'
], function (_, Backbone, navbarTemplate) {

    var NAVBAR_TEMPLATE = _.template(navbarTemplate);

    var IndexView = Backbone.View.extend({

        initialize: function () {
        },

        render: function () {
            this.$el.html(NAVBAR_TEMPLATE());
            return this;
        }
    });

    return IndexView;
});
