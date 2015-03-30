(function ($, Backbone, _, app) {

    app.collections.RootDirectories = Backbone.Collection.extend({
        model: Directory,
        url: '/api/directories/?root=true'
    });

    app.collections.SubDirectories = Backbone.Collection.extend({
        model: Directory,

        initialize: function (options) {
            options || (options = {});
            this.parentId = options.parentId;
        },

        url: function () {
            return '/api/directories/' + this.parentId + '/sub_directories/';
        }
    });
})(jQuery, Backbone, _, app);

