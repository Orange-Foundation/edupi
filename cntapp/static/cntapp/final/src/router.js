define([
    'backbone',
    'views/index', 'views/structure',
    'views/directory_list', 'views/statebar',
    'views/document_list',
    'models/directory'
], function (Backbone,
             IndexView, StructureView,
             DirectoryListView, StateBarView,
             DocumentListView,
             Directory) {
    var AppRouter, _currentPath, _refreshCurrentPath;

    _currentPath = new Backbone.Collection({model: Directory});

    _refreshCurrentPath = function (pathCollection, path) {
        var pathArray, pathDirectories, d, i;
        pathDirectories = [];
        pathArray = path.split('/');
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
            // valid path example: 1/22/33/44
            this.route(/^directories\/((?:\d+)(?:\/\d+)*)$/, 'showDirectoryContent');
            this.route(/^$/, 'indexRoute');
        },

        indexRoute: function () {
            var view = new IndexView();
            $("body").html(view.fetchAndRender().el);
        },

        showDirectoryContent: function (path) {
            var structureView, dirsView, documentsView;

            // (re-)init page structure
            structureView = new StructureView();
            $("body").html(structureView.render().el);

            _refreshCurrentPath(_currentPath, path);
            $("#nav-zone").append(new StateBarView({path: _currentPath}).render().el);

            // show directories
            dirsView = new DirectoryListView({path: path});
            $("#content").html(dirsView.fetchAndRender().el);

            var dirId = path.slice(path.lastIndexOf('/') + 1);
            console.log("dirId:" + dirId);
            documentsView = new DocumentListView({parentId: dirId});
            $("#content").append(documentsView.render().el);
        }

    });

    return AppRouter;
});
