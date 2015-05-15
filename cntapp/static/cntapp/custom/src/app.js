define([
    'underscore', 'backbone', 'router',
    'views/nav', 'views/page_wrapper',
    'collections/directories',
    'text!templates/container.html'
], function (_, Backbone, AppRouter,
             NavbarView, PageWrapperView,
             DirectoriesCollection,
             containerTemplate) {

    var app;

    app = function () {
        // initialization
        var router = new AppRouter();
        var navbar, pageWrapper,
            directoriesCollection;

        navbar = new NavbarView();
        pageWrapper = new PageWrapperView();

        directoriesCollection = new DirectoriesCollection();
        directoriesCollection.fetch({
            reset: true,
            success: function () {
                $("body").html(_.template(containerTemplate)());
                $("#navbar").html(navbar.render().el);
                $("#page-wrapper").html(pageWrapper.render().el);
                Backbone.history.start();
            }
        });

        return {
            router: router,
            views: {
                navbar: navbar,
                pageWrapper: pageWrapper
            },
            collections: {
                directories: directoriesCollection
            },
            apiRoots: {
                directories: '/api/directories/',
                documents: '/api/documents/'
            }
        };
    }();

    return app;
});
