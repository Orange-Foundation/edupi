define([
    'underscore',
    'backbone',
    'text!templates/directory_list.html'
], function (_, Backbone, directoryListTemplate) {

    var DIRECTORY_LIST_TEMPLATE = _.template(directoryListTemplate);

    var DirectoryListView = Backbone.View.extend({

        initialize: function (options) {
            this.path = options.path;
            this.collection = new Backbone.Collection({model: Backbone.Model});
            this.listenTo(this.collection, 'reset', this.render);
        },

        render: function () {
            var context = {
                directories: (this.collection && this.collection.models) || null,
                path: this.path
            };
            this.$el.html(DIRECTORY_LIST_TEMPLATE(context));
            return this;
        },

        fetchAndRender: function () {
            var that, dirId, url;
            that = this;
            dirId = this.path.slice(this.path.lastIndexOf('/') + 1);
            url = "/api/directories/" + dirId + "/sub_directories/";
            $.getJSON(url)
                .done(function (data) {
                    that.collection.reset(data);
                });
            return this;
        }
    });

    return DirectoryListView;
});
