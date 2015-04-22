define([
    'backbone',
    'views/list_directories',
    'views/create_directory',
    'views/edit_directory',
    'views/documents_table',
    'views/documents_upload',
    'views/upload_document_to_directory',
    'models/directory'
], function (Backbone,
             ListDirectoriesView, CreateDirectoryView,
             EditDirectoryView, DocumentsTableView,
             DocumentsUploadView,
             UploadDocumentToDirectoryView,
             Directory) {
    var PAGE_WRAPPER = "#page-wrapper";

    var AppRouter,
        currentDirectories,
        currentPath,
        initialize;

    AppRouter = Backbone.Router.extend({
        initialize: function () {

            // root directories
            this.route(/^directories$/, 'listDirectories');
            this.route(/^directories\/create$/, 'createDirectory');

            // sub directories
            this.route(/^directories\/(\d+)\/create$/, 'createDirectory');
            this.route(/^directories\/(\d+)$/, 'listDirectories');
            this.route(/^directories\/(\d+)\/edit$/, 'editDirectory');
            this.route(/^directories\/(\d+)\/upload$/, 'uploadFileToDirectory');

            // documents
            this.route(/^documents$/, 'listDocuments');
            this.route(/^documents\/upload$/, 'uploadDocuments');
        },

        go: function () {
            return this.navigate(_.toArray(arguments).join("/"), true);
        },

        renderToContent: function (view) {
            $(PAGE_WRAPPER).html(view.render().$el);
        },

        uploadFileToDirectory: function (parentId) {
            this.renderToContent(new UploadDocumentToDirectoryView({parentId: parentId}));
        },

        listDirectories: function (parentId) {
            var view = cntapp.views.directories;
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

            if (typeof view == "undefined") {
                view = new ListDirectoriesView({el: PAGE_WRAPPER});
                cntapp.views.directories = view;
                currentDirectories = view.collection;
            }

            // update the view
            view.fetchAndRefresh({parentId: parentId, path: currentPath.getPath()});
        },

        createDirectory: function (parentId) {
            this.renderToContent(new CreateDirectoryView({parentId: parentId}));
        },

        editDirectory: function (id) {
            this.renderToContent(new EditDirectoryView({
                directory: currentDirectories.get(id)
            }));
        },

        listDocuments: function () {
            new DocumentsTableView({el: PAGE_WRAPPER}).render();
        },

        uploadDocuments: function () {
            this.renderToContent(new DocumentsUploadView());
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

    return AppRouter;
});
