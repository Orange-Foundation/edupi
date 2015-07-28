define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/document.html',
    'text!templates/file_play_modal.html'
], function ($, _, Backbone,
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

                // PDF does not display on a mobile, so open it in a new tab and that will trigger downloading the file.
                if (this.model.get('type') === 'p' && finalApp.isMobile) {
                    window.open(this.model.get('file'), '_blank');
                    return;
                }

                that = this;
                modal_id = '#modal-' + this.model.get('id');
                file_id = '#file-' + this.model.get('id');
                this.$el.append(FILE_PLAY_MODAL_TEMPLATE({model: this.model}));
                this.$el.i18n()

                // auto-play video and audio
                if (['v', 'a'].indexOf(this.model.get('type')) > -1) {
                    this.$(modal_id).on('hidden.bs.modal', function () {
                        that.$(file_id).get(0).pause();
                    });
                    this.$(modal_id).on('shown.bs.modal', function () {
                        that.$(file_id).get(0).play();
                    });
                }

                var tmpHash;
                this.$(modal_id).one("shown.bs.modal", function () { // any time a modal is shown
                    var s = location.hash;
                    var URL_SEPARATOR = '$';

                    // query string
                    if (s.lastIndexOf(URL_SEPARATOR) > s.indexOf('#')) {
                        // happens when refresh with a modal window
                        s = s.slice(0, s.indexOf(URL_SEPARATOR));
                        tmpHash = s + URL_SEPARATOR + modal_id;
                        history.replaceState(null, null, tmpHash); // push state that hash into the url
                    } else {
                        tmpHash = s + URL_SEPARATOR + modal_id;
                        history.pushState(null, null, tmpHash); // push state that hash into the url
                    }
                });

                this.$(modal_id).one('hidden.bs.modal', function () {
                    if (location.hash === tmpHash) {
                        var s = location.hash;
                        history.back(); // fire popstate
                    }
                });

                // If a pushstate has previously happened and the back button is clicked, hide any modals.
                $(window).one('popstate', function () {
                    $(modal_id).modal('hide');
                    console.log('pop state');
                });
            }
        }
    });

    return DocumentView;
});