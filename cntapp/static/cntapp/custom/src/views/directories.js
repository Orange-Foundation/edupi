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
            //this.collection = new Backbone.Collection({model: Directory});
            this.collection = options.collection;
            this.path = options.path || null;
            this.listenTo(this.collection, 'reset', this.render);
        },

        render: function () {
            this.$el.html('<div id="directories_table" class="col-md-12"></div>');
            this.$("#directories_table").html(this.template(this.getContext()));
            return this;
        },

        getContext: function () {
            return {
                directories: (this.collection && this.collection.models) || null,
                path: this.path || null
            };
        },

        fetchAndRefresh: function (parentId) {
            var that = this;
            var url = "/api/directories/";
            url += (parentId ? parentId + "/sub_directories/" : "?root=true");
            $.getJSON(url)
                .done(function (data) {
                    that.collection.reset(data);
                });
        }
    });

    return DirectoriesView;
});

