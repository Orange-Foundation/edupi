define([
    'underscore',
    'backbone',
    'models/document',
    'views/document',
    'text!templates/document_list.html'
], function (_, Backbone,
             Document,
             DocumentView,
             documentListTemplate) {

    var DocumentListView = Backbone.View.extend({
        tagName: "ul",
        className: "list-group",
        id: "document-list",

        initialize: function (options) {
            if (!options.parentId) {
                console.error("no directory id specified");
                return;
            }

            this.parentId = options.parentId;
            this.template = _.template(documentListTemplate);
            this.collection = options.currentDocuments;
            this.collection.on('render', this.render, this);
            this.collection.on('unlink', this.unlink, this);
            _.bind(this.unlink, this);
        },

        unlink: function (documentModel) {
            var url,
                data,
                that = this;
            url = cntapp.apiRoots.directories + this.parentId + '/documents/';
            data = {"documents": documentModel.get('id')};

            $.ajax({
                type: 'DELETE', url: url, data: data, traditional: true,
                success: function () {
                    that.collection.remove(documentModel);
                    documentModel.trigger('destroy'); // remove the document view
                },
                error: function (request, status, error) {
                    alert(error);
                }
            });
        },

        render: function () {
            var docs = [];
            var that = this;
            var url = '/api/directories/' + this.parentId + '/documents/';
            that.$el.html('');
            $.get(url)
                .done(function (data) {
                    _(data).each(function (obj) {
                        var m = new Document(obj);
                        that.$el.append(
                            new DocumentView({model: m, id: "document-" + m.id}).render().el);
                        docs.push(m);
                    });
                    // must use `reset` instead of `set`, otherwise the pre-existed models cannot fire events.
                    // it's a bug of Backbone.js?
                    that.collection.reset(docs);
                });
            return this;
        }
    });

    return DocumentListView;
});