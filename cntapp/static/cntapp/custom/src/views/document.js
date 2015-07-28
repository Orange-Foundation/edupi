define([
    'underscore',
    'backbone',
    'text!templates/document.html',
    'text!templates/document_edit.html',
    'text!templates/file_play_modal.html',
    'text!templates/confirm_modal.html',
    'text!templates/path_list.html'
], function (_, Backbone,
             documentTemplate,
             documentEditTemplate,
             filePlayModalTemplate,
             confirmModalTemplate,
             pathListTemplate) {

    var TEMPLATE = _.template(documentTemplate);
    var EDIT_TEMPLATE = _.template(documentEditTemplate);
    var FILE_PLAY_MODAL_TEMPLATE = _.template(filePlayModalTemplate);
    var CONFIRM_MODAL_TEMPLATE = _.template(confirmModalTemplate);
    var PATH_LIST_TEMPLATE = _.template(pathListTemplate);

    var DocumentView = Backbone.View.extend({
        tagName: "li",
        className: "list-group-item",

        initialize: function (options) {
            options = options || {};

            this.isSearchResult = typeof options.isSearchResult === "boolean" ? options.isSearchResult : false;
            this.model.on("change", this.render, this);
            this.model.on("destroy", this.destroy, this);

            this.model.on('invalid', function (model, error) {
                this.$('.error-msg').html(error);
            }, this);

            this.allPaths = [];
        },

        render: function () {
            this.$el.html(TEMPLATE({model: this.model, isSearchResult: this.isSearchResult}));
            this.$(".glyphicon").hide();
            this.$(".error-msg").hide();
            this.$el.i18n();
            return this;
        },

        createInstantConfirmModal: function (message, confirmCallback) {
            var that = this,
                wrappedCallback;
            if (typeof confirmCallback === 'undefined') {
                throw Error('No callback function for confirm dialog.');
            }

            console.log('searching modal-area');
            this.$('.modal-area').html(CONFIRM_MODAL_TEMPLATE({
                title: null,
                message: message
            }));
            this.$(".modal").on('hidden.bs.modal', function () {
                $(this).data('bs.modal', null);
                $(this).remove();
            });
            this.$('.modal').on('shown.bs.modal', function () {
                that.$('.btn-confirmed').focus();
            });
            wrappedCallback = _.wrap(confirmCallback, function (callback) {
                callback();
                that.$('.modal').modal('hide');
            });

            this.$('.modal-area').i18n();
            this.$('.modal-area .btn-confirmed').click(wrappedCallback);
        },

        destroy: function () {
            // remove this view, only called when document model destroy event is triggered.
            this.$el.fadeOut(200, function () {
                $(this).remove();
            });
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
                this.$el.i18n();
            },
            'click .btn-cancel': function () {
                this.render();
            },
            'click .glyphicon-link': function () {
                var that = this;
                this.createInstantConfirmModal(
                    i18n.t('doc-unlink-confirm-msg'),
                    function () {
                        that.model.trigger('unlink', that.model);
                    }
                );
            },
            'click .glyphicon-trash': function () {
                var that = this;
                this.createInstantConfirmModal(
                    i18n.t("doc-delete-confirm-msg"),
                    function () {
                        that.model.destroy();
                    }
                );
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
            },
            'click .paths': function () {
                if (this.allPaths.length > 0) {
                    return;
                }

                var that = this;
                var parents = that.model.get('directory_set');
                var fetchedNum = 0;
                for (var i = 0; i < parents.length; i++) {
                    $.get(cntapp.apiRoots.directories + parents[i]['id'] + '/paths/')
                        .done(function (paths) {
                            that.allPaths = that.allPaths.concat(paths);
                            if (++fetchedNum === parents.length) {
                                // TODO: find a proper way to sort the result
                                that.allPaths = that.allPaths.sort(function (a, b) {
                                    return a[0]['name'] >= b['0']['name'];
                                });

                                that.$('span[data-toggle="path-popover"]').popover({
                                    html: true,
                                    container: 'body',
                                    content: function () {
                                        return PATH_LIST_TEMPLATE({
                                            paths: that.allPaths
                                        });
                                    }
                                }).popover('show');
                            }
                        });
                }
            }
        },

        saveDocument: function () {
            var name = this.$('input[name="name"]').val().trim();
            var description = this.$('textarea[name="description"]').val().trim();
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