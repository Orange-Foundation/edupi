define([
    'underscore',
    'backbone',
    'views/search/document_search',
    'text!templates/search/search_page.html'
], function (_, Backbone,
             DocumentSearchView,
             searchPageTemplate
) {

    var TEMPLATE = _.template(searchPageTemplate);

    var SearchPageView = Backbone.View.extend({

        initialize: function (options) {
            options = options || {};
            if (typeof options.queryString === 'undefined') {
                throw new Error('querySrring not defined.')
            }
            if (options.queryString === '') {  // TODO check
                throw new Error('nothing to query.')
            }

            this.queryString = options.queryString;
        },

        render: function () {
            this.$el.html(searchPageTemplate);
            this.$el.i18n();
            this.$('.search-result').html(new DocumentSearchView({queryString: this.queryString}).render().el);
            return this;
        }
    });

    return SearchPageView;
});
