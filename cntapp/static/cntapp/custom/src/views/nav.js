define([
    'underscore',
    'backbone',
    'text!templates/nav.html'
], function (_, Backbone, navTemplate) {

    var NavView = Backbone.View.extend({
        initialize: function () {
            this.render();
        },
        render: function () {
            var template = _.template(navTemplate);
            this.$el.html(template());
            return this;
        }
    });

    return NavView;
});