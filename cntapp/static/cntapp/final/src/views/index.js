define([
    'underscore',
    'backbone',
    'views/navbar',
    'text!templates/index.html'
], function (_, Backbone, NavbarView, indexTemplate) {

    var INDEX_TEMPLATE = _.template(indexTemplate);

    var IndexView = Backbone.View.extend({

        initialize: function () {
        },

        render: function () {
            this.$el.html(INDEX_TEMPLATE());
            this.$('#nav-zone').html(new NavbarView().render().el);
            return this;
        }
    });

    return IndexView;
});
