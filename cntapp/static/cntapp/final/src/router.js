define([
    'backbone',
    'views/index',
    'views/structure',
    'views/directory_list'
], function (Backbone, IndexView, StructureView, DirectoryListView) {
    var AppRouter;

    AppRouter = Backbone.Router.extend({
        initialize: function () {
            this.route(/^$/, 'indexRoute');
            this.route(/^directories$/, 'directories');
        },

        indexRoute: function () {
            $("body").html(new IndexView().render().el);
        },

        directories: function () {
            // (re-)init page structure
            $("body").html(new StructureView().render().el);
            // show directories
            $("#content").html(new DirectoryListView().render().el)
        }

    });

    return AppRouter;
});
