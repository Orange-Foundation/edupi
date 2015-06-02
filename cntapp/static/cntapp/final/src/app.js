define([
    'underscore',
    'backbone',
    'router',
    'collections/directories',
    'views/body_structure'
], function (_, Backbone, AppRouter,
             DirectoriesCollection,
             BodyStructureView) {

    var app;

    app = function () {
        // initialization
        var router = new AppRouter();
        var directoriesCollection;

        directoriesCollection = new DirectoriesCollection();
        directoriesCollection.fetch({
            reset: true,
            success: function () {
                $('body').html(new BodyStructureView().render().el);
                Backbone.history.start();
            }
        });

        return {
            router: router,
            collections: {
                directories: directoriesCollection
            }
        };
    }();

    return app;
});
