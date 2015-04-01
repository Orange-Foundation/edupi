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
            this.crtView = null;
            Backbone.history.start();
        },

        roots: function () {
            this.render(new app.views.RootDirectoriesView());
        },

        subDirectory: function (parentId) {
            this.render(new app.views.SubDirectoriesView({parentId: parentId}));
        },

        createRootDirectory: function () {
            //this.render(new app.views.CreateDirectoryView());
            this.render(new app.views.CreateDirectoryView());
        },

        createSubDirectory: function () {
            this.render(new app.views.CreateDirectoryView());
        },

        editDirectory: function (id) {
            this.render(new app.views.EditDirectoryView({id: id}));
        },

        render: function (view) {
            if (this.crtView) {
                this.crtView.stopListening();
                this.crtView.$el = $();
                this.crtView.remove();
            }
            this.crtView = view;
            this.crtView.render();
        }
    });

    app.Router = AppRouter;
})(jQuery, Backbone, _, app);