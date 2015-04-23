define([
    'underscore',
    'backbone',
    'text!templates/action_bar.html'
], function (_, Backbone, actionBarTemplate) {

    var ActionBarView = Backbone.View.extend({
        initialize: function (option) {
            this.template = _.template(actionBarTemplate);
        },

        render: function () {
            var that = this;
            var html = this.template({
                parentId: this.parentId
            });
            this.$el.html(html);
            this.$("#create-directory").attr("href", function () {
                if (that.parentId) {
                    return "#directories/" + that.parentId + "/create";
                } else {
                    return "#directories/create";
                }
            });
            return this;
        },

        setParentId: function (parentId) {
            this.parentId = parentId;
        }
    });

    return ActionBarView;
});