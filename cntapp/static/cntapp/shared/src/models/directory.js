define([
    'backbone',
    'models/base_model'
], function (Backbone, BaseModel) {

    var MAX_DIR_NAME_LENGTH = 60;

    var Directory = BaseModel.extend({

        urlRoot: '/api/directories',

        validate: function (attrs, options) {
            if (attrs.name.length <= 0) {
                return i18n.t('msg-input-error-empty-name');
            }
            if (attrs.name.length >= MAX_DIR_NAME_LENGTH) {
                return i18n.t(
                    'msg-input-error-name-too-long',
                    {
                        postProcess: 'sprintf', sprintf: [attrs.name.length, MAX_DIR_NAME_LENGTH]
                    }
                );
            }
        }
    });

    return Directory;
});
