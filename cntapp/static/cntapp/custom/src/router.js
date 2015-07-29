define([
    'backbone',
    'views/directories_page', 'views/root_page', 'views/upload_page',
    'views/sysinfo_page',
    'views/stats/stats_page',
    'views/search/search_page',
    'models/directory'
], function (Backbone,
             DirectoriesPageView, RootPageView, UploadPageView,
             SysInfoPageView,
             StatsPageView,
             SearchPageView,
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

            this.route(/^sysinfo$/, 'showSysInfo');
            this.route(/^stats$/, 'showStats');

            // querystring: #documents?queryString
            this.route(/^documents\?(.*)$/, 'showSearchResult');

            this.route(/^$/, 'indexRoute');
        },

        renderToContent: function (view) {
            cntapp.views.pageWrapper.setContentView(view);
            cntapp.views.pageWrapper.render();
        },

        showSearchResult: function (queryString) {
            console.log('search documents with querystring="' + queryString + '"');
            this.renderToContent(new SearchPageView({queryString: queryString}));
        },

        showSysInfo: function () {
            this.renderToContent(new SysInfoPageView())
        },

        showStats: function () {
            this.renderToContent(new StatsPageView())
        },

        showRootPage: function () {
            this.renderToContent(new RootPageView());
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

        indexRoute: function () {
            this.navigate('#directories', {trigger: true});
        }
    });

    return AppRouter;
});
