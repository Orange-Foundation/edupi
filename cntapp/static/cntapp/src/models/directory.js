define([
    'backbone',
    'models/base_model'
], function (Backbone, BaseModel) {

    var Directory = BaseModel.extend({

        urlRoot: '/api/directories',

        defaults: {
            id: -1
        }
    });

    return Directory;
});
