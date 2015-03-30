(function ($, Backbone, _, app) {

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

    var EditDirectoryView = Backbone.View.extend({
        el: "#content",

        render: function () {
            var template = _.template($("#directory-edit-template").html());
            this.$el.html(template({}))
        }
    });

    var CreateDirectoryView = Backbone.View.extend({
        el: "#content",

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