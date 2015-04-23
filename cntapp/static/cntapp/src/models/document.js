define([
    'backbone',
    'models/base_model'

], function (Backbone, BaseModel) {

    var DocumentModel = BaseModel.extend({
        urlRoot: '/api/documents/'
    });

    return DocumentModel;
});