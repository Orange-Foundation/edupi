define([
    'backbone',
    'views/index', 'views/body_structure',
    'views/directory_list', 'views/statebar',
    'views/document_list', 'views/content_structure',
    'models/directory'
], function (Backbone,
             IndexView, BodyStructureView,
             DirectoryListView, StateBarView,
             DocumentListView, ContentStructureView,
             Directory) {
    var AppRouter, _currentPath, _refreshCurrentPath;

    AppRouter = Backbone.Router.extend({

        initialize: function () {
            // valid path example: 1/22/33/44
            this.route(/^directories\/((?:\d+)(?:\/\d+)*)$/, 'showDirectoryContent');
            this.route(/^$/, 'indexRoute');
        },

        indexRoute: function () {
            // root directories are shown in the index page
            var view = new IndexView();
            $("#state-nav").html("");  // clean the state-nav-bar
            $("#content").html(view.fetchAndRender().el);
        },

        renderToContent: function (view) {
            $('#content').html(view.render().el);
        },

        showDirectoryContent: function (path) {
            $("#state-nav").html(new StateBarView({path: path}).refreshAndRender().el);
            this.renderToContent(new ContentStructureView({path: path}));
        }

    });

    return AppRouter;
});
