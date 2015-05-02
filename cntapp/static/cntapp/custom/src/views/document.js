define([
    'underscore',
    'backbone',
    'text!templates/document.html',
    'text!templates/document_edit.html',
    'text!templates/file_play_modal.html'
], function (_, Backbone,
             documentTemplate,
             documentEditTemplate,
             filePlayModalTemplate) {

    var TEMPLATE = _.template(documentTemplate);
    var EDIT_TEMPLATE = _.template(documentEditTemplate);
    var FILE_PLAY_MODAL_TEMPLATE = _.template(filePlayModalTemplate);

    var DocumentView = Backbone.View.extend({
        tagName: "li",
        className: "list-group-item",

        initialize: function () {
            this.model.on("change", this.render, this);

            this.model.on('invalid', function (model, error) {
                this.$('.error-msg').html(error);
            }, this);

        },

        render: function () {
            this.$el.html(TEMPLATE({model: this.model}));
            this.$(".glyphicon").hide();
            this.$(".error-msg").hide();

            this.$('span[data-toggle="popover"]').popover({
                html: true,
                content: function () {
                    return "<button class='btn btn-danger btn-block btn-delete-confirmed'>\
                        DELETE</button>";
                }
            });
            return this;
        },

        events: {
            'mouseenter': function () {
                this.$(".glyphicon").show();
            },
            'mouseleave': function () {
                this.$(".glyphicon").hide();
            },
            'click .glyphicon-pencil': function () {
                this.$el.html(EDIT_TEMPLATE({model: this.model}));
            },
            'click .btn-cancel': function () {
                this.render();
            },
            'click .btn-delete-confirmed': function () {
                var that = this;
                this.model.destroy({
                    success: function (model, response) {
                        console.log('model destroyed');
                        console.log(response);
                        that.$el.fadeOut(200, function () {
                            $(this).remove();
                        })
                    }
                });
            },
            'click .btn-play': function () {
                var that, modal_id, file_id;
                this.$el.append(FILE_PLAY_MODAL_TEMPLATE({model: this.model}));

                // auto-play video and audio
                if (['v', 'a'].indexOf(this.model.get('type')) > -1) {
                    modal_id = '#modal-' + this.model.get('id');
                    file_id = '#file-' + this.model.get('id');
                    that = this;
                    this.$(modal_id).on('hidden.bs.modal', function () {
                        that.$(file_id).get(0).pause();
                    });
                    this.$(modal_id).on('shown.bs.modal', function () {
                        that.$(file_id).get(0).play();
                    });
                }
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