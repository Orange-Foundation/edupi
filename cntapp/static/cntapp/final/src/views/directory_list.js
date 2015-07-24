define([
    'underscore',
    'backbone',
    'text!templates/directory_list.html'
], function (_, Backbone, directoryListTemplate) {

    var DIRECTORY_LIST_TEMPLATE = _.template(directoryListTemplate);

    var DirectoryListView = Backbone.View.extend({

        initialize: function (options) {
            options = options || {};
            if (typeof options.directories === 'undefined' || typeof options.path === 'undefined') {
                throw new Error('no directories or path defined!');
            }
            this.path = options.path;
            this.collection = options.directories
        },

        render: function () {
            var context = {
                directories: (this.collection && this.collection.models) || null,
                path: this.path
            };
            this.$el.html(DIRECTORY_LIST_TEMPLATE(context));
            return this;
        }
    });

    return DirectoryListView;
});
