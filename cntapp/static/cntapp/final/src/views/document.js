define([
    'underscore',
    'backbone',
    'text!templates/document.html',
], function (_, Backbone,
             documentTemplate) {

    var TEMPLATE = _.template(documentTemplate);

    var DocumentView = Backbone.View.extend({
        tagName: "li",
        className: "list-group-item",

        initialize: function () {
            this.model.on("change", this.render, this);
        },

        render: function () {
            this.$el.html(TEMPLATE({model: this.model}));
            return this;
        },

        events: {
            'click .document-row': function () {
                window.open(this.model.get('file'));
            }
        }
    });

    return DocumentView;
});