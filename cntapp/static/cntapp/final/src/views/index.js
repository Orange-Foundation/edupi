define([
    'underscore',
    'backbone',
    'text!templates/index.html'
], function (_, Backbone, indexTemplate) {

    var INDEX_TEMPLATE = _.template(indexTemplate);
    var CACHE = {};

    var IndexView = Backbone.View.extend({

        initialize: function (options) {
            options = options || {};

            if (typeof options.rootDirectories === 'undefined') {
                throw new Error('root directories not defined!');
            }
            this.collection = options.rootDirectories;
        },

        render: function () {
            this.$el.html(INDEX_TEMPLATE({
                directories: (this.collection && this.collection.models) || null
            }));
            this.$el.i18n();
            return this;
        }
    });

    return IndexView;
});
