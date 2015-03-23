(function ($, Backbone, _, app) {
    var DirectoriesView = Backbone.View.extend({
        el: "#content",

        render: function () {
            var template = _.template($("#directories-template").html());
            this.$el.html(template({}));
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

    app.views.DirectoriesView = DirectoriesView;
    app.views.EditDirectoryView = EditDirectoryView;
    app.views.CreateDirectoryView = CreateDirectoryView;

})(jQuery, Backbone, _, app);