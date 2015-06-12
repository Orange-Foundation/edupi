define([
    'underscore',
    'backbone',
    'views/directory_list',
    'views/document_list',
    'text!templates/content_structure.html'
], function (_, Backbone,
             DirectoryListView, DocumentListView,
             contentStructureTemplate) {


    var TEMPLATE = _.template(contentStructureTemplate);

    var ContentStructureView = Backbone.View.extend({
        initialize: function (options) {
            options = options || {};
            if (typeof options.path === 'undefined') {
                throw new Error('path not defined.');
            }

            this.path = options.path;
            this.parentId = this.path.slice(this.path.lastIndexOf('/') + 1);
        },

        render: function () {
            var dirsView, documentsView;
            this.$el.html(TEMPLATE());

            // show directories
            dirsView = new DirectoryListView({path: this.path});
            this.$("#directories-container").html(dirsView.fetchAndRender().el);


            documentsView = new DocumentListView({parentId: this.parentId});
            this.$("#documents-container").html(documentsView.render().el);
            return this;
        }
    });

    return ContentStructureView;
});
