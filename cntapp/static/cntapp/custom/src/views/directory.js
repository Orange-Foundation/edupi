define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/directory.html',
    'text!templates/edit_directory_modal.html',
    'text!templates/confirm_modal.html',

], function ($, _, Backbone, directoryTemplate, editDirectoryModalTemplate, confirmModalTemplate) {

    var DirectoryView, TEMPLATE, EDIT_DIRECTORY_MODAL_TEMPLATE, CONFIRM_MODAL_TEMPLATE,
        UNLINK_CONFIRM_MSG = 'Are you sure to unlink this directory? ' +
            'Unlinked directory can be found in root directories.';

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
            this.$el.i18n();
            return this;
        },

        createInstantConfirmModal: function (message, confirmCallback) {
            if (typeof confirmCallback === 'undefined') {
                throw Error('No callback function for confirm dialog.');
            }

            this.$('.modal-area').html(CONFIRM_MODAL_TEMPLATE({
                title: null,
                message: message
            }));
            this.$(".modal").on('hidden.bs.modal', function () {
                $(this).data('bs.modal', null);
                $(this).remove();
            });
            this.$('.modal-area').i18n();
            this.$('.modal-area .btn-confirmed').click(confirmCallback);
        },

        removeModalAndItem: function () {
            this.$('.modal').modal('hide');
            this.$el.fadeOut(200, function () {
                $(this).remove();
            });
        },

        events: {
            'click .btn-edit': function () {
                var that = this;
                this.$("div.modal-area").html(EDIT_DIRECTORY_MODAL_TEMPLATE({model: this.model}));
                this.$('.modal').on('shown.bs.modal', function () {
                    that.$('input[name="name"]').focus();
                });
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
                var that = this;
                this.createInstantConfirmModal(
                    i18n.t('dir-delete-confirm-msg'),
                    function () {
                        console.debug('recursively deleting directory id="' + that.model.get('id') + '"');
                        if (that.path) {  // sub directory
                            var pathArray = that.path.split('/');
                            var parentId = pathArray[pathArray.length - 1];
                            $.ajax({
                                url: cntapp.apiRoots.directories + parentId + '/delete/',
                                type: 'DELETE',
                                data: {'id': that.model.get('id')},
                                success: that.removeModalAndItem()
                            });
                        } else {  // root directory
                            that.model.destroy({
                                success: that.removeModalAndItem()
                            });
                        }
                    }
                );
            },

            'click .btn-unlink-directory': function () {
                var that = this;
                this.createInstantConfirmModal(
                    i18n.t('dir-unlink-confirm-msg'),
                    function () {
                        var pathArray = that.path.split('/');
                        var parentId = pathArray[pathArray.length - 1];
                        $.ajax({
                            url: cntapp.apiRoots.directories + parentId + '/directories/',
                            type: 'DELETE',
                            data: {'id': that.model.get('id')},
                            success: that.removeModalAndItem()
                        });
                    }
                );
            }

        }
    });

    return DirectoryView;
});
