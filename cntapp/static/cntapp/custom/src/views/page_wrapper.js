define([
    'underscore',
    'backbone',
    'text!templates/page_wrapper.html'
], function (_, Backbone, pageWrapperTemplate) {
    var PageWrapperView = Backbone.View.extend({

        initialize: function (options) {
            this.template = _.template(pageWrapperTemplate);
            this.stateBarView = null;
            this.actionBarView = null;
            this.contentView = null;
        },

        render: function () {
            // create the page skeleton
            this.$el.html(this.template());

            //if (this.stateBarView) {
            //    this.$("#state-bar").html(this.stateBarView.el);
            //}
            //
            //if (this.actionBarView) {
            //    this.$("#action-bar").html(this.actionBarView.render().el);
            //}

            if (this.contentView) {
                this.$("#content").html(this.contentView.render().el);
            }

            return this;
        },

        setStateBarView: function (stateBarView) {
            this.stateBarView = stateBarView;
        },

        setActionBarView: function (actionBarView) {
            this.actionBarView = actionBarView;
        },

        setContentView: function (contentView) {
            this.contentView = contentView;
        },

        getContentView: function () {
            return this.contentView;
        },

        getStateBarView: function () {
            return this.stateBarView;
        },

        getActionBarView: function () {
            return this.actionBarView;
        }
    });

    return PageWrapperView;
});