define([
    'underscore',
    'backbone',
    'text!templates/index.html'
], function (_, Backbone, indexTemplate) {

    var INDEX_TEMPLATE = _.template(indexTemplate);

    var IndexView = Backbone.View.extend({

        initialize: function () {
            this.collection = new Backbone.Collection({model: Backbone.Model});
            this.listenTo(this.collection, 'reset', this.render);
        },

        render: function () {
            this.$el.html(INDEX_TEMPLATE({
                directories: (this.collection && this.collection.models) || null
            }));
            return this;
        },

        fetchAndRender: function () {
            // get the root directories
            var that, url;
            that = this;
            url = "/api/directories/?root=true";
            $.getJSON(url)
                .done(function (data) {
                    that.collection.reset(data);
                });
            return this;
        }
    });

    return IndexView;
});
