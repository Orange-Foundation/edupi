define([
    'underscore',
    'backbone',
    'text!templates/directory_list.html'
], function (_, Backbone, directoryListTemplate) {

    var DIRECTORY_LIST_TEMPLATE = _.template(directoryListTemplate);

    var DirectoryListView = Backbone.View.extend({

        initialize: function () {
        },

        render: function () {
            this.$el.html(DIRECTORY_LIST_TEMPLATE());
            return this;
        }
    });

    return DirectoryListView;
});
