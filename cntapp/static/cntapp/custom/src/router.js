define([
    'backbone',
    'views/structure_content',
    'views/documents_table',
    'views/documents_upload',
    'views/directories_page', 'views/root_page',
    'models/directory'
], function (Backbone,
             StructureContentView,
             DocumentsTableView,
             DocumentsUploadView,
             DirectoriesPageView, RootPageView,
             Directory) {
    var PAGE_WRAPPER = "#page-wrapper";

    var AppRouter,
        _refreshCurrentPath;

    _refreshCurrentPath = function (pathCollection, pathArray) {
        pathCollection = pathCollection || new Backbone.Collection({model: Directory});
        var pathDirectories, d, i;
        pathDirectories = [];
        for (i = 0; i < pathArray.length; i++) {
            d = new Directory({id: pathArray[i]});
            d.fetch({
                success: function (directory) {
                    pathCollection.push(directory);
                }
            });
            pathDirectories.push(d);
        }
        pathCollection.reset(pathDirectories);
        return pathCollection;
    };

    AppRouter = Backbone.Router.extend({

        initialize: function () {
            this.route(/^directories$/, 'showRootPage');
            // valid path example: 1/22/33/44
            this.route(/^directories\/((?:\d+)(?:\/\d+)*)$/, 'showDirectoryPage');
            // documents
            this.route(/^documents$/, 'listDocuments');
            this.route(/^documents\/upload$/, 'uploadDocuments');
            this.route(/^$/, 'indexRoute');
        },

        renderToContent: function (view) {
            cntapp.views.pageWrapper.setContentView(view);
            cntapp.views.pageWrapper.render();
        },

        showRootPage: function () {
            var dirs = cntapp.collections.directories,
                that = this;
            dirs.fetch({
                reset: true,
                success: function () {
                    that.renderToContent(new RootPageView());
                }
            })
        },

        showDirectoryPage: function (path) {
            var dirs = cntapp.collections.directories,
                that = this;
            if (dirs.length > 0) {
                that.renderToContent(new DirectoriesPageView({path: path}));
            }
        },

        listDocuments: function () {
            new DocumentsTableView({el: PAGE_WRAPPER}).render();
        },

        uploadDocuments: function () {
            this.renderToContent(new DocumentsUploadView());
        },

        indexRoute: function () {
            this.navigate('#directories', {trigger: true});
        }
    });

    return AppRouter;
});
