define([
    'jquery',
    'underscore',
    'backbone',
    'views/document_list',
    'models/directory',
    'text!templates/directories.html'
], function ($, _, Backbone,
             DocumentListView, Directory, directoriesTemplate) {

    var DirectoriesView = Backbone.View.extend({

        initialize: function (options) {
            this.template = _.template(directoriesTemplate);
            this.collection = new Backbone.Collection({model: Directory});
            this.listenTo(this.collection, 'reset', this.render);

            if (options.parentId) {
                this.parentId = options.parentId;
                this.current_path = options.path;
            }
        },

        render: function () {
            var context = this.getContext();
            var that = this;
            this.$el.html('<div id="directories_table" class="col-md-12"></div>');
            this.$("#directories_table").html(this.template(context));
            this.$("#create-directory").attr("href", function () {
                if (that.parentId) {
                    return "#directories/" + that.parentId + "/create";
                } else {
                    return "#directories/create";
                }
            });

            // show documents
            if (this.parentId) {
                this.$el.append('<div id="documents_table" class="col-md-12"></div>');
                var documentListView = new DocumentListView({
                    el: "#documents_table",
                    parentId: this.parentId
                });
                documentListView.render();
            }

            return this;
        },

        fetchAndRefresh: function () {
            var that = this;
            var url = "/api/directories/";
            url += (this.parentId ? this.parentId + "/sub_directories/" : "?root=true");

            $.getJSON(url)
                .done(function (data) {
                    that.collection.reset(data);
                });
        },

        getContext: function () {
            return {
                directories: (this.collection && this.collection.models) || null,
                current_path: this.current_path || null
            };
        }
    });

    return DirectoriesView;
});


