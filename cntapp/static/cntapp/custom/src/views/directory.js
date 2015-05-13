define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/directory.html',
    'text!templates/edit_directory_modal.html',
    'text!templates/confirm_modal.html'

], function ($, _, Backbone, directoryTemplate, editDirectoryModalTemplate, confirmModalTemplate) {

    var DirectoryView, TEMPLATE, EDIT_DIRECTORY_MODAL_TEMPLATE, CONFIRM_MODAL_TEMPLATE,
        DELETE_CONFIRM_MSG = 'Are you sure to delete this directory? ' +
            'This will also delete its sub directories, but will not delete the linked documents.';

    TEMPLATE = _.template(directoryTemplate);
    EDIT_DIRECTORY_MODAL_TEMPLATE = _.template(editDirectoryModalTemplate);
    CONFIRM_MODAL_TEMPLATE = _.template(confirmModalTemplate);


    var DirectoryView = Backbone.View.extend({
        tagName: 'tr',

        initialize: function (options) {
            if (options.path && typeof options.path !== 'string') {
                throw new TypeError("expected 'string', by got:" + typeof options.path);
            }
            this.path = options.path;
            this.baseLink = '#directories';
            this.baseLink += this.path ? '/' + this.path : '';

            this.model.on('invalid', function (model, error) {
                this.$('.error-msg').html(error);
            }, this);
        },

        render: function () {
            this.$el.html(TEMPLATE({
                baseLink: this.baseLink,
                model: this.model
            }));
            return this;
        },

        events: {
            'click .btn-edit': function () {
                this.$("div.modal-area").html(EDIT_DIRECTORY_MODAL_TEMPLATE({model: this.model}));
            },

            'click .btn-edit-confirm': function () {
                var that = this,
                    name = this.$('input[name="name"]').val();
                if (name === this.model.get("name")) {
                    that.$('.modal').modal('hide');  // nothing to update
                } else {
                    this.model.save({"name": name}, {
                        patch: true,
                        success: function () {
                            that.$('.modal').modal('hide');
                            that.render();
                        }
                    });
                }
            },

            'click .btn-delete-directory': function () {
                this.$('.modal-area').html(CONFIRM_MODAL_TEMPLATE({
                    title: null,
                    message: DELETE_CONFIRM_MSG
                }));
            },

            'click .btn-confirmed': function () {
                console.debug('deleting directory id="' + this.model.get('id') + '"');

                var that = this;
                this.model.destroy({
                    success: function (model, response) {
                        that.$('.modal').modal('hide');
                        console.log('directory destroyed');
                        console.log(response);
                        that.$el.fadeOut(200, function () {
                            $(this).remove();
                        })
                    }
                });

            },

        }
    });

    return DirectoryView;
});
