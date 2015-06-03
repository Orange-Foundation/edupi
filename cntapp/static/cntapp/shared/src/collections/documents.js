define([
    'backbone',
    'models/document'
], function (Backbone, Document) {

    var DocumentCollection = Backbone.Collection.extend({
        url: '/api/documents/',
        model: Document
    });

    return DocumentCollection;
});
