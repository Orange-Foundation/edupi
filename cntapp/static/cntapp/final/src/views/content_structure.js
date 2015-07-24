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
    var CACHE = {};

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

        showContent: function (request, url) {
            var that = this,
                dirsView, documentsView;
            request.done(function (data) {
                that.$('.content-info').html("");

                // show directories and documents
                that.directories.reset(data["directories"]);
                that.documents.reset(data["documents"]);

                // check if there is any content
                if (that.directories.length === 0
                    && that.documents.length === 0) {
                    console.log('empty directory');
                    that.showErrorMsg("There is nothing here :(");
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

            request.error(function (XMLHttpRequest, textStatus, errorThrown) {
                if (XMLHttpRequest.readyState == 0) {
                    that.showErrorMsg(
                        "Failed to retrieve content from the Server, there might be something wrong with your network."
                    );
                } else if (XMLHttpRequest.status === 404) {
                    that.showErrorMsg("The content that you requested does not exist!");
                } else {
                    that.showErrorMsg("Failed to retrieve content from the Server, and I don't know why :(");
                }
                CACHE[url] = null; // remove failed request from cache.
            });
        },

        showErrorMsg: function (msg) {
            this.$('.content-info').html(msg);
        },

        render: function () {
            var that, dirId, url,
                dirsView, documentsView;

            this.$el.html(TEMPLATE());

            that = this;
            dirId = this.path.slice(this.path.lastIndexOf('/') + 1);
            url = "/api/directories/" + dirId + "/sub_content/";

            var cachedRequest = CACHE[url];
            if (typeof cachedRequest != 'undefined' && cachedRequest !== null) {
                console.log('render the content from cache');
                this.showContent(cachedRequest);
            } else {
                var request = $.get(url);
                this.showContent(request, url);
                CACHE[url] = request;
            }

            return this;
        }
    });

    return ContentStructureView;
});
