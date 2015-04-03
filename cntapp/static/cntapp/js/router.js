(function ($, Backbone, _, app) {
    var AppRouter = Backbone.Router.extend({
        routes: {
            '': 'listDirectories',
            'create': 'createDirectory',
            ':id': 'listDirectories',
            ':id/edit': 'editDirectory',
            ':id/create': 'createDirectory'
        },

        initialize: function (options) {
            Backbone.history.start();
        },

        listDirectories: function (parentId) {
            var view = new app.views.DirectoriesView({
                el: "#content",
                parentId: parentId
            });
            app.currentDirectories = view.collection;
            view.fetchAndRefresh();
        },

        /* Form views */

        createDirectory: function (parentId) {
            this.renderToContent(new app.views.CreateDirectoryView({parentId: parentId}));
        },

        editDirectory: function (id) {
            this.renderToContent(new app.views.EditDirectoryView({
                directory: app.currentDirectories.get(id)
            }));
        },

        renderToContent: function (view) {
            $("#content").html(view.render().$el);
        }

    });

    app.Router = AppRouter;
})(jQuery, Backbone, _, app);