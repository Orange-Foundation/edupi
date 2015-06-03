define([
    'underscore',
    'backbone',
    'text!templates/navbar.html'
], function (_, Backbone, navbarTemplate) {

    var NAVBAR_TEMPLATE = _.template(navbarTemplate);
    var SEARCH_MAX_ITEM_PER_PAGE = 20;

    var IndexView = Backbone.View.extend({

        initialize: function () {
        },

        render: function () {
            this.$el.html(NAVBAR_TEMPLATE());
            return this;
        },

        events: {
            'submit form': 'submit',
            'keyup input[name="search-text"]': function (e) {
                this.search();
            }
        },

        submit: function (event) {
            event.preventDefault();
        },

        search: function () {
            var name = this.$('input[name="search-text"]').val();
            name = name.trim().split(' ').join('+');

            if (name === "") {
                return;
            }

            // Go to the research page
            var searchUrl = [
                '#documents?search=', name,
                '&order=asc&limit=', SEARCH_MAX_ITEM_PER_PAGE,
                '&offset=0'
            ].join('');
            finalApp.router.navigate(searchUrl, {trigger: true});
        }

    });

    return IndexView;
});
