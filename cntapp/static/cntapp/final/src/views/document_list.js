define([
    'underscore',
    'backbone',
    'views/document',
    'models/document',
    'text!templates/document_list.html'
], function (_, Backbone,
             DocumentView, Document,
             documentListTemplate) {

    var DocumentList = Backbone.Collection.extend({
        model: Backbone.Model
    });

    var DocumentListView = Backbone.View.extend({
        tagName: "ul",
        className: "col-sm-offset-2 col-sm-8",
        id: "document-list",

        initialize: function (options) {
            if (!options.parentId) {
                console.error("no directory id specified");
                return;
            }

            this.parentId = options.parentId;
            this.collection = new DocumentList();
        },

        render: function () {
            var that = this;
            var url = '/api/directories/' + this.parentId + '/documents/';
            $.get(url)
                .done(function (data) {
                    _(data).each(function (obj) {
                        var m = new Document(obj);
                        that.$el.append(
                            new DocumentView({model: m, id: "document-" + m.id}).render().el);
                        that.collection.add(m);
                    });
                });
            return this;
        }
    });

    return DocumentListView;
});
