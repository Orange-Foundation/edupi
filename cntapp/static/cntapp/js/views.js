(function ($, Backbone, _, app) {
    $.fn.serializeObject = function () {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };

    var RootDirectoriesView = Backbone.View.extend({
        el: "#content",
        templateName: "#directories-template",

        render: function () {
            var that = this;
            this.getDirectories().fetch({
                success: function (directories) {
                    var template = _.template($(that.templateName).html());
                    that.$el.html(template({directories: directories.models}));
                }
            });
        },

        getDirectories: function () {
            return new app.collections.RootDirectories();
        }
    });

    var SubDirectoriesView = RootDirectoriesView.extend({
        initialize: function (options) {
            this.parentId = options.parentId;
        },

        getDirectories: function () {
            return new app.collections.SubDirectories({parentId: this.parentId});
        }
    });

    var EditDirectoryView = Marionette.View.extend({
        el: "#content",

        initialize: function (options) {
            this.directory = new Directory({id: options.id});
        },

        render: function () {
            var that = this;
            that.directory.fetch({
                success: function (directory) {
                    var template = _.template($("#directory-edit-template").html());
                    that.$el.html(template({directory: directory}));
                }
            });
        },

        events: {
            'click #dir-delete': 'delete'
        },

        delete: function (ev) {
            console.warn('deleting!!');
            ev.stopPropagation();
            this.directory.destroy({
                success: function () {
                    app.router.navigate('', {trigger: true});
                }
            });
            return true;
        }
    });

    var CreateDirectoryView = Marionette.View.extend({
        el: "#content",

        events: {
            'submit #directory-create-form': 'create',
            'click #cancel': 'cancel'
        },

        create: function (ev) {
            ev.stopPropagation();
            var dirDetails = $(ev.currentTarget).serializeObject();
            var roots = new app.collections.RootDirectories();
            roots.fetch({
                type: 'POST',
                data: JSON.stringify(dirDetails),
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('Content-Type', 'application/json');
                },
                success: function () {
                    app.router.navigate('', {trigger: true});
                }
            });
            return false;
        },

        cancel: function () {
            window.history.back();
        },

        render: function () {
            var template = _.template($("#create-directory-template").html());
            this.$el.html(template({}))
        }
    });

    app.views.RootDirectoriesView = RootDirectoriesView;
    app.views.SubDirectoriesView = SubDirectoriesView;
    app.views.EditDirectoryView = EditDirectoryView;
    app.views.CreateDirectoryView = CreateDirectoryView;

})(jQuery, Backbone, _, app);