define([
    'backbone',
    'views/documents_table',
    'views/directories_page', 'views/root_page', 'views/upload_page',
    'models/directory'
], function (Backbone,
             DocumentsTableView,
             DirectoriesPageView, RootPageView, UploadPageView,
             Directory) {
    var PAGE_WRAPPER = "#page-wrapper";

    var AppRouter;

    AppRouter = Backbone.Router.extend({

        initialize: function () {
            // root directories
            this.route(/^directories$/, 'showRootPage');

            // sub directories directories
            // valid path example: 1/22/33/44
            this.route(/^directories\/((?:\d+)(?:\/\d+)*)$/, 'showDirectoryPage');
            this.route(/^directories\/((?:\d+)(?:\/\d+)*)\/upload$/, 'showUploadPage');

            // documents
            this.route(/^documents$/, 'listDocuments');

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

        showUploadPage: function (path) {
            this.renderToContent(new UploadPageView({path: path}))
        },

        listDocuments: function () {
            new DocumentsTableView({el: PAGE_WRAPPER}).render();
        },

        indexRoute: function () {
            this.navigate('#directories', {trigger: true});
        }
    });

    return AppRouter;
});
