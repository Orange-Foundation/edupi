define([
    'backbone',
    'views/index', 'views/body_structure',
    'views/directory_list', 'views/statebar',
    'views/document_list', 'views/content_structure',
    'views/search_page',
    'models/directory'
], function (Backbone,
             IndexView, BodyStructureView,
             DirectoryListView, StateBarView,
             DocumentListView, ContentStructureView,
             SearchPageView,
             Directory) {
    var AppRouter, _currentPath, _refreshCurrentPath;

    AppRouter = Backbone.Router.extend({

        initialize: function () {
            // valid path example: 1/22/33/44
            this.route(/^directories\/((?:\d+)(?:\/\d+)*)$/, 'showDirectoryContent');

            // querystring: #documents?queryString
            this.route(/^documents\?(.*)$/, 'showSearchResult');

            this.route(/^$/, 'indexRoute');
        },

        indexRoute: function () {
            // root directories are shown in the index page
            var view = new IndexView({rootDirectories: finalApp.rootDirectories});
            $("#state-nav").html("");  // clean the state-nav-bar
            this.renderToContent(view);
        },

        renderToContent: function (view) {
            $('#content').html(view.render().el);
        },

        showDirectoryContent: function (path) {
            $("#state-nav").html(new StateBarView({path: path}).refreshAndRender().el);
            this.renderToContent(new ContentStructureView({path: path}));
        },

        showSearchResult: function (queryString) {
            $('#state-nav').html('');
            console.log('search documents with querystring="' + queryString + '"');
            this.renderToContent(new SearchPageView({queryString: queryString}));
        }

    });

    return AppRouter;
});
