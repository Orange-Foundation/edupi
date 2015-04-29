define([
    'jquery',
    'underscore',
    'backbone',
    'views/document_list',
    'views/directories',
    'models/directory'
], function ($, _, Backbone,
             DocumentListView, DirectoriesView,
             Directory) {

    var StructureContentView = Backbone.View.extend({

        initialize: function (options) {
            this.currentDirectories = options.currentDirectories;
        },

        setParentId: function (parentId) {
            this.parentId = parentId;
        },

        render: function () {
            // show directories
            this.$el.html('<div id="directories"></div>');
            this.directoriesView = new DirectoriesView({
                el: this.$("#directories"),
                collection: this.currentDirectories
            });
            this.directoriesView.fetchAndRefresh(this.parentId);

            // show documents
            if (this.parentId) {
                this.documentListView = new DocumentListView({parentId: this.parentId});
                this.$el.append('<div id="documents_table" class="col-md-12"></div>');
                this.$("#documents_table").html(this.documentListView.render().el);
            }

            return this;
        }
    });

    return StructureContentView;
});


