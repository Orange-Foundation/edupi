(function ($, Backbone, _, app) {

    app.currentPath = function () {
        var path = [];
        if (sessionStorage.getItem('current_path')) {
            var objects = JSON.parse(sessionStorage.getItem('current_path'));
            var i;
            for (i = 0; i < objects.length; i++) {
                path.push(new app.models.Directory(objects[i]));
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
        if (app.currentPath) {
            sessionStorage.setItem("current_path", JSON.stringify(app.currentPath.getPath()));
        }
    };

    var AppRouter = Backbone.Router.extend({
        routes: {
            '': 'listDirectories',
            'create': 'createDirectory',
            ':id': 'listDirectories',
            ':id/edit': 'editDirectory',
            ':id/create': 'createDirectory'
        },

        initialize: function (options) {
            Backbone.history.start();
        },

        listDirectories: function (parentId) {
            if (!parentId) {
                app.currentPath.clear();
            } else {
                if (!app.currentPath.popToDirectory(parentId)) {
                    // push
                    if (app.currentDirectories && app.currentDirectories.get(parentId)) {
                        app.currentPath.push(app.currentDirectories.get(parentId))
                    } else {
                        var d = new app.models.Directory({id: parentId});
                        d.fetch({
                            success: function (directory) {
                                app.currentPath.push(directory);
                            }
                        });
                    }
                }
            }

            var view = new app.views.DirectoriesView({
                el: "#content",
                parentId: parentId,
                path: app.currentPath.getPath()
            });
            app.currentDirectories = view.collection;
            view.fetchAndRefresh();
        },

        /* Form views */

        createDirectory: function (parentId) {
            this.renderToContent(new app.views.CreateDirectoryView({parentId: parentId}));
        },

        editDirectory: function (id) {
            this.renderToContent(new app.views.EditDirectoryView({
                directory: app.currentDirectories.get(id)
            }));
        },

        renderToContent: function (view) {
            $("#content").html(view.render().$el);
        }

    });

    app.Router = AppRouter;
})(jQuery, Backbone, _, app);