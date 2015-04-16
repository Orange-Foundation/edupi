define([
    'jquery',
    'underscore',
    'backbone'
], function ($, _, Backbone) {
    var TemplateView = Backbone.View.extend({
        templateName: '',
        initialize: function () {
            this.template = _.template($(this.templateName).html());
        },
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

