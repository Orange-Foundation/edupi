define([
    'backbone',
    'views/state_bar',
    'views/structure_content',
    'views/create_directory',
    'views/edit_directory',
    'views/documents_table',
    'views/documents_upload',
    'views/upload_document_to_directory',
    'models/directory'
], function (Backbone,
             StateBarView,
             StructureContentView, CreateDirectoryView,
             EditDirectoryView, DocumentsTableView,
             DocumentsUploadView,
             UploadDocumentToDirectoryView,
             Directory) {
    var PAGE_WRAPPER = "#page-wrapper";

    var AppRouter,
        currentDirectories,
        currentPath;

    AppRouter = Backbone.Router.extend({
        initialize: function () {

            // root directories
            this.route(/^directories$/, 'structure');
            this.route(/^directories\/create$/, 'createDirectory');

            // sub directories
            this.route(/^directories\/(\d+)\/create$/, 'createDirectory');
            this.route(/^directories\/(\d+)$/, 'structure');
            this.route(/^directories\/(\d+)\/edit$/, 'editDirectory');
            this.route(/^directories\/(\d+)\/upload$/, 'uploadFileToDirectory');

            // documents
            this.route(/^documents$/, 'listDocuments');
            this.route(/^documents\/upload$/, 'uploadDocuments');

            this.route(/^$/, 'indexRoute');

            if (!currentDirectories) {
                currentDirectories = new Backbone.Collection({model: Directory});
            }
        },

        go: function () {
            return this.navigate(_.toArray(arguments).join("/"), true);
        },

        renderToContent: function (view) {
            cntapp.views.pageWrapper.setContentView(view);
            cntapp.views.pageWrapper.render();
        },

        uploadFileToDirectory: function (parentId) {
            this.renderToContent(new UploadDocumentToDirectoryView({parentId: parentId}));
        },

        updatePath: function (parentId, currentPath, currentDirectories) {
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
        },

        structure: function (parentId) {
            var contentView = cntapp.views.structureContentView;

            if (typeof contentView == "undefined") {
                contentView = new StructureContentView({
                    currentDirectories: currentDirectories
                });
                cntapp.views.structureContentView = contentView;
            }

            var stateBarView = cntapp.views.stateBarView;
            if (typeof stateBarView == "undefined") {
                stateBarView = new StateBarView();
                cntapp.views.stateBarView = stateBarView;
            }

            this.updatePath(parentId, currentPath, currentDirectories);

            contentView.setParentId(parentId);
            stateBarView.setCurrentPath(currentPath.getPath());

            cntapp.views.pageWrapper.setStateBarView(stateBarView);
            cntapp.views.pageWrapper.setContentView(contentView);
            cntapp.views.pageWrapper.render();
        },

        createDirectory: function (parentId) {
            this.renderToContent(new CreateDirectoryView({parentId: parentId}));
        },

        editDirectory: function (id) {
            var directory = currentDirectories.get(id);
            var that = this;

            if (directory) {
                this.renderToContent(new EditDirectoryView({
                    directory: directory
                }));
            } else {
                directory = new Directory({id: id});
                directory.fetch({
                    success: function () {
                        that.renderToContent(new EditDirectoryView({
                            directory: directory
                        }));
                    }
                });
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
