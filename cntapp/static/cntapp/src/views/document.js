define([
    'underscore',
    'backbone',
    'text!templates/document.html'
], function (_, Backbone, documentTemplate) {

    var TEMPLATE = _.template(documentTemplate);

    var DocumentView = Backbone.View.extend({
        tagName: "li",
        className: "list-group-item",

        initialize: function () {
            this.model.on("change:name", this.render, this);
            this.model.on("change:description", this.render, this);
        },

        render: function () {
            this.$el.html(TEMPLATE({model: this.model}));
            return this;
        }
    });

    return DocumentView;
});