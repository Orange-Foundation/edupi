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

            this.directories = new Backbone.Collection({model: Backbone.Model});
            this.documents = new Backbone.Collection({model: Backbone.Model});
        },

        render: function () {
            var that, dirId, url,
                dirsView, documentsView;

            this.$el.html(TEMPLATE());

            that = this;
            dirId = this.path.slice(this.path.lastIndexOf('/') + 1);
            url = "/api/directories/" + dirId + "/sub_content/";
            $.getJSON(url)
                .done(function (data) {
                    that.$('.content-info').html("");

                    // show directories and documents
                    that.directories.reset(data["directories"]);
                    that.documents.reset(data["documents"]);

                    // check if there is any content
                    if (that.directories.length === 0
                        && that.documents.length === 0) {
                        console.log('empty directory');
                        that.$('.content-info').html("Nothing here :(");
                        return
                    }

                    // show content: directories and documents
                    dirsView = new DirectoryListView({
                        path: that.path,
                        directories: that.directories
                    });
                    that.$("#directories-container").html(dirsView.render().el);

                    documentsView = new DocumentListView({
                        parentId: that.parentId,
                        documents: that.documents
                    });
                    that.$("#documents-container").html(documentsView.render().el);
                });
            return this;
        }
    });

    return ContentStructureView;
});
