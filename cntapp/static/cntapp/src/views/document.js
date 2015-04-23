define([
    'underscore',
    'backbone',
    'text!templates/document.html',
    'text!templates/document_edit.html'
], function (_, Backbone,
             documentTemplate, documentEditTemplate) {

    var TEMPLATE = _.template(documentTemplate);
    var EDIT_TEMPLATE = _.template(documentEditTemplate);

    var DocumentView = Backbone.View.extend({
        tagName: "li",
        className: "list-group-item",

        initialize: function () {
            this.model.on("change", this.render, this);

            this.model.on('invalid', function (model, error) {
                this.$('.error-msg').html(error);
            }, this)
        },

        render: function () {
            this.$el.html(TEMPLATE({model: this.model}));
            this.$(".glyphicon-pencil").hide();
            this.$(".error-msg").hide();
            return this;
        },

        events: {
            'mouseenter': function () {
                this.$(".glyphicon-pencil").show();
            },
            'mouseleave': function () {
                this.$(".glyphicon-pencil").hide();
            },
            'click .glyphicon-pencil': function () {
                this.$el.html(EDIT_TEMPLATE({model: this.model}));
            },
            'click .btn-cancel': function () {
                this.render();
            },
            'click .btn-save': 'saveDocument',
            'keypress': function (e) {
                var code = e.keyCode || e.which;
                if (code === 10) {  // ctrl + enter
                    this.saveDocument();
                }
            }
        },

        saveDocument: function () {
            var name = this.$('input[name="name"]').val();
            var description = this.$('textarea[name="description"]').val();
            if (name !== this.model.get("name") || description !== this.model.get("description")) {
                this.model.save({
                    "name": name,
                    "description": description
                }, {patch: true});
            } else {
                this.render();
            }
        }
    });

    return DocumentView;
});