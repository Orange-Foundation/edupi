define([
    'underscore',
    'backbone',
    'text!templates/page_wrapper.html'
], function (_, Backbone, pageWrapperTemplate) {
    var PageWrapperView = Backbone.View.extend({

        initialize: function (options) {
            this.template = _.template(pageWrapperTemplate);
            // create the page skeleton
            this.$el.html(this.template());
            this.contentView = null;
        },

        render: function () {
            if (this.contentView) {
                this.$("#content").html(this.contentView.render().el);
            }
            return this;
        },

        setContentView: function (contentView) {
            this.contentView = contentView;
        },

        getContentView: function () {
            return this.contentView;
        }

    });

    return PageWrapperView;
});