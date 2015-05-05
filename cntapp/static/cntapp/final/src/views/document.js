define([
    'underscore',
    'backbone',
    'text!templates/document.html',
    'text!templates/file_play_modal.html'
], function (_, Backbone,
             documentTemplate, filePlayModalTemplate) {

    var TEMPLATE = _.template(documentTemplate);
    var FILE_PLAY_MODAL_TEMPLATE = _.template(filePlayModalTemplate);

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
            }
        }
    });

    return DocumentView;
});