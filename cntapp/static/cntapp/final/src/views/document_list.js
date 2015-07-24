define([
    'underscore',
    'backbone',
    'views/document',
    'models/document',
    'collections/documents',
    'text!templates/document_list.html'
], function (_, Backbone,
             DocumentView, Document, Documents,
             documentListTemplate) {

    var DocumentList = Backbone.Collection.extend({
        model: Backbone.Model
    });

    var DocumentListView = Backbone.View.extend({
        tagName: "ul",
        className: "col-sm-offset-2 col-sm-8",
        id: "document-list",

        initialize: function (options) {
            options = options || {};

            if (!options.parentId) {
                console.error("no directory id specified");
                return;
            }

            if (typeof options.documents === 'undefined') {
                throw new Error("documents not defined!");
            }

            this.parentId = options.parentId;
            this.collection = options.documents;
        },

        render: function () {
            var that = this;
            _(that.collection.models).each(function (doc) {
                that.$el.append(
                    new DocumentView({model: doc, id: "document-" + doc.get('id')}).render().el);
            });
            return this;
        }
    });

    return DocumentListView;
});
