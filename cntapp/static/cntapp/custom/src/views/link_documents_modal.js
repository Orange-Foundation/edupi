/*
This is a modal view
 */
define([
    'underscore', 'backbone',
    'text!templates/link_documents_modal.html'
], function (_, Backbone, linkDocumentsModal) {
    var LinkDocumentModalView, TEMPLATE;

    TEMPLATE = _.template(linkDocumentsModal);

    LinkDocumentModalView = Backbone.View.extend({
        render: function () {
            this.$el.html(TEMPLATE());
            return this;
        },
        toggle: function () {
            this.$('#link-documents-modal').modal('toggle');
        }
    });

    return LinkDocumentModalView
});