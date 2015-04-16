define([
    'jquery',
    'underscore',
    'backbone',
    'models/directory',
    'text!templates/directories.html'
], function ($, _, Backbone, Directory, directoriesTemplate) {

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
            var context = this.getContext(),
                html = this.template(context);
            var that = this;
            this.$el.html(html);
            this.$("#create-directory").attr("href", function () {
                if (that.parentId) {
                    return "#" + that.parentId + "/create";
                } else {
                    return "#create";
                }
            });

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


