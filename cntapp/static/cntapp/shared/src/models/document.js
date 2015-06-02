define([
    'backbone',
    'models/base_model'

], function (Backbone, BaseModel) {

    var DocumentModel = BaseModel.extend({

        urlRoot: '/api/documents/',

        validate: function (attrs, options) {
            if (attrs.name.length <= 0) {
                return "name must not be empty";
            }
        }
    });

    return DocumentModel;
});