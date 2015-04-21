define([
    'underscore',
    'backbone',
    'text!templates/document_list.html'
], function (_, Backbone, documentListTemplate) {

    var DocumentList = Backbone.View.extend({
        initialize: function (options) {
            if (!options.parentId) {
                console.error("no directory id specified");
                return;
            }

            this.parentId = options.parentId;
            this.template = _.template(documentListTemplate);
        },

        render: function () {
            var that = this;
            var url = '/api/directories/' + this.parentId + '/documents/';
            $.get(url)
                .done(function (data) {
                    var context = {documents: data};
                    that.$el.html(that.template(context))
                });
        }
    });

    return DocumentList;
});