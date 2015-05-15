define([
    'backbone',
    'models/base_model'
], function (Backbone, BaseModel) {

    var Directory = BaseModel.extend({

        urlRoot: '/api/directories',

        validate: function (attrs, options) {
            if (attrs.name.length <= 0) {
                return "name must not be empty";
            }
        }
    });

    return Directory;
});
