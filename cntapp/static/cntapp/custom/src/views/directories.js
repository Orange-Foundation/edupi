define([
    'jquery', 'underscore', 'backbone',
    'views/directory',
    'models/directory',
    'text!templates/directories.html'
], function ($, _, Backbone,
             DirectoryView,
             Directory,
             directoriesTemplate) {

    var DirectoriesView, TEMPLATE;

    TEMPLATE = _.template(directoriesTemplate);

    var DirectoriesView = Backbone.View.extend({

        initialize: function (options) {
            this.collection = options.collection;
            this.path = options.path || null;
            this.listenTo(this.collection, 'reset', this.render);
        },

        render: function () {
            var that = this;
            this.$el.html(TEMPLATE());
            if (this.collection.length === 0) {
                this.$('tbody').append('<tr><td data-i18n="no-sub-dirs-msg">there is no sub-directories</td></tr>')
            } else {
                _.each(this.collection.models, function (dir) {
                    that.$('tbody').append(new DirectoryView({model: dir, path: that.path}).render().el);
                });
            }
            this.$el.i18n();
            return this;
        },

        fetchAndRefresh: function (parentId) {
            var that = this;
            var url = "/api/directories/";
            url += (parentId ? parentId + "/sub_directories/" : "?root=true");
            $.getJSON(url)
                .done(function (data) {
                    that.collection.reset(data);
                    // update local directory collection.
                    cntapp.collections.directories.set(data, {remove: false});
                });
        }
    });

    return DirectoriesView;
});

