(function ($, Backbone, _, app) {
    var AppRouter = Backbone.Router.extend({
        routes: {
            '': 'roots',
            'create': 'createRootDirectory',
            ':id': 'subDirectory',
            ':id/edit': 'editDirectory',
            ':id/create': 'createSubDirectory'
        },

        initialize: function (options) {
            Backbone.history.start();
        },

        roots: function () {
            var view = new app.views.DirectoriesView({el: "#content"});
            view.fetchAndRefresh();
        },

        subDirectory: function (parentId) {
            var view = new app.views.DirectoriesView({
                el: "#content",
                parentId: parentId
            });
            view.fetchAndRefresh();
        },

        /* Form views */

        createRootDirectory: function () {
            this.renderToContent(new app.views.CreateDirectoryView());
        },

        createSubDirectory: function (parentId) {
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