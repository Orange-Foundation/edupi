define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    var TemplateView = Backbone.View.extend({
        render: function () {
            var context = this.getContext(),
                html = this.template(context);
            this.$el.html(html);

            return this;
        },
        getContext: function () {
            return {};
        }
    });

    return TemplateView;
});

