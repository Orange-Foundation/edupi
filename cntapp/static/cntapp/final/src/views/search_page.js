define([
    'underscore',
    'backbone',
    'views/navbar', 'views/statebar',
    'views/document_search',
    'text!templates/body_structure.html',
    'text!templates/footer.html',
], function (_, Backbone,
             NavbarView, StateBarView,
             DocumentSearchView,
             bodyStructureTemplate, footerTemplate) {


    var PAGE_STRUCTURE_TEMPLATE = _.template(bodyStructureTemplate);
    var FOOTER_TEMPLATE = _.template(footerTemplate);


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
            this.$el.html(new DocumentSearchView({queryString: this.queryString}).render().el);
            return this;
        }
    });

    return SearchPageView;
});
