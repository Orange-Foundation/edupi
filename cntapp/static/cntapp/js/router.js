define([
    'jquery',
    'underscore',
    'backbone',
    'views/list_directories',
    'views/create_directories',
    'views/edit_directory',
    'views/documents_table',
    'models/directory'
], function ($, _, Backbone,
             ListDirectoriesView, CreateDirectoryView,
             EditDirectoryView, DocumentsTableView,
             Directory) {

    var AppRouter,
        currentDirectories,
        currentPath,
        initialize;

    AppRouter = Backbone.Router.extend({
        routes: {
            '': 'listDirectories',
            'create': 'createDirectory',
            'documents': 'listDocuments',
            ':id': 'listDirectories',
            ':id/edit': 'editDirectory',
            ':id/create': 'createDirectory'
        },

        renderToContent: function (view) {
            $("#content").html(view.render().$el);
        }
    });

    currentPath = function () {
        var path = [];
        if (sessionStorage.getItem('current_path')) {
            var objects = JSON.parse(sessionStorage.getItem('current_path'));
            var i;
            for (i = 0; i < objects.length; i++) {
                path.push(new Directory(objects[i]));
            }
        }
        return {
            getPath: function () {
                return path;
            },
            push: function (directory) {
                if (path[path.length - 1] !== directory) {
                    path.push(directory);
                }
            },
            pop: function () {
                return path.pop();
            },
            clear: function () {
                path = [];
            },
            contain: function (id) {
                var i;
                for (i = 0; i < path.length; i++) {
                    if (path[i].get("id") == id) {
                        return true;
                    }
                }
                return false;
            },
            popToDirectory: function (id) {
                if (!this.contain(id)) {
                    return false;
                }
                var d;
                d = this.pop();
                while (d.get("id") != id) {
                    d = this.pop();
                }
                this.push(d);
                return true;
            }
        }
    }();

    window.onbeforeunload = function (evt) {
        if (currentPath) {
            sessionStorage.setItem("current_path", JSON.stringify(currentPath.getPath()));
        }
    };


    // let's wire up everything
    initialize = function () {
        var appRouter = new AppRouter();

        appRouter.on("route:listDirectories", function (parentId) {
            var view;
            if (!parentId) {
                currentPath.clear(); // back to home
            } else {
                if (!currentPath.popToDirectory(parentId)) {
                    // push
                    if (currentDirectories && currentDirectories.get(parentId)) {
                        currentPath.push(currentDirectories.get(parentId))
                    } else {
                        var d = new Directory({id: parentId});
                        d.fetch({
                            success: function (directory) {
                                currentPath.push(directory);
                            }
                        });
                    }
                }
            }
            view = new ListDirectoriesView({
                el: "#content",
                parentId: parentId,
                path: currentPath.getPath()
            });
            currentDirectories = view.collection;
            view.fetchAndRefresh();
        });

        appRouter.on("route:createDirectory", function (parentId) {
            this.renderToContent(new CreateDirectoryView({parentId: parentId}));
        });

        appRouter.on("route:editDirectory", function (id) {
            this.renderToContent(new EditDirectoryView({
                directory: currentDirectories.get(id)
            }));
        });

        appRouter.on("route:listDocuments", function () {
            new DocumentsTableView({el: "#content"}).render();
        })
    };

    return {
        initialize: initialize
    }
});
