define([
    'jquery',
    'underscore',
    'backbone',
    'views/form',
    'text!templates/edit_directory.html'
], function ($, _, Backbone, FormView, editDirectoryTemplate) {

    var EditDirectoryView = FormView.extend({

        initialize: function (options) {
            this.template = _.template(editDirectoryTemplate);
            this.directory = options.directory;
        },

        getContext: function () {
            return {directory: this.directory};
        },

        submit: function (event) {
            FormView.prototype.submit.apply(this, arguments);
            var data = this.serializeForm(this.form);
            console.log(JSON.stringify(data));
            var url = "/api/directories/" + this.directory.id + "/update/";
            $.ajax({
                type: "PUT",
                url: url,
                contentType: "application/json",
                data: JSON.stringify(data),
                success: function (result) {
                    console.log("updated");
                    window.history.back();
                }
            });
        },

        events: {
            'submit form': 'submit',
            'click #dir-delete': 'deleteDirectory'
        },

        deleteDirectory: function (ev) {
            var that = this;
            $.ajax({
                url: "/api/directories/" + this.directory.id,
                type: 'DELETE',
                success: function (result) {
                    console.log("element deleted:" + result);
                    that.done();
                    window.history.back();
                }
            });
        }
    });

    return EditDirectoryView;
});
