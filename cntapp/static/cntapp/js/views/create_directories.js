define([
    'jquery',
    'underscore',
    'backbone',
    'models/directory',
    'views/form'
], function ($, _, Backbone, Directory, FormView) {

    var CreateDirectoryView = FormView.extend({
        templateName: "#create-directory-template",

        initialize: function (options) {
            FormView.prototype.initialize.apply(this, options);
            if (options && options.parentId) {
                this.parentId = options.parentId;
            }
        },

        submit: function (event) {
            FormView.prototype.submit.apply(this, arguments);
            var data = this.serializeForm(this.form);
            var url = "/api/directories/";
            if (this.parentId) {
                url = url + this.parentId + "/create_sub_directory/";
            }

            $.post(url, data)
                .success($.proxy(this.createSuccess, this))
                .fail($.proxy(this.failure, this));
        },

        createSuccess: function () {
            console.log("create success");
            this.done();
            window.history.back();
        },

        failure: function () {
            console.warn("fail to create");
        }
    });

    return CreateDirectoryView;

});
