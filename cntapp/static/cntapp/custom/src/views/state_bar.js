define([
    'underscore',
    'backbone',
    'text!templates/state_bar.html'
], function (_, Backbone, stateBarTemplate) {
    var StateBarView = Backbone.View.extend({

        initialize: function (options) {
            this.template = _.template(stateBarTemplate);
        },

        render: function () {
            var html = this.template({
               current_path: this.currentPath || null
            });

            this.$el.html(html);
            return this;
        },

        setCurrentPath: function (currentPath) {
            this.currentPath = currentPath;
        }

    });
    return StateBarView;
});