define([
    'backbone',
    'views/index',
    'views/structure',
    'views/directory_list',
    'views/statebar',
    'models/directory'
], function (Backbone, IndexView, StructureView, DirectoryListView, StateBarView, Directory) {
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
        routes: {
            "": "indexRoute",
            "directories/*path": "showDirectoryContent",
        },

        indexRoute: function () {
            var view = new IndexView();
            $("body").html(view.fetchAndRender().el);
        },

        showDirectoryContent: function (path) {
            var structureView, dirsView;

            // (re-)init page structure
            structureView = new StructureView();
            $("body").html(structureView.render().el);

            _refreshCurrentPath(_currentPath, path);
            $("#nav-zone").append(new StateBarView({path: _currentPath}).render().el);

            // show directories
            dirsView = new DirectoryListView({path: path});
            $("#content").html(dirsView.fetchAndRender().el);


            // TODO: show documents
        }

    });

    return AppRouter;
});
