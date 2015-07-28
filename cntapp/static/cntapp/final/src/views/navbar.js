define([
    'underscore',
    'backbone',
    'text!templates/navbar.html'
], function (_, Backbone, navbarTemplate) {

    var NAVBAR_TEMPLATE = _.template(navbarTemplate);
    var SEARCH_MAX_ITEM_PER_PAGE = 20;
    var SEARCH_TEXT_MIN_LENGTH = 2;
    var SEARCH_FIRE_DELAY = 800; // millisecond

    var IndexView = Backbone.View.extend({

        initialize: function () {
        },

        render: function () {
            this.$el.html(NAVBAR_TEMPLATE());
            this.$el.i18n();
            return this;
        },

        events: {
            'submit form': 'submit',
            'keyup input[name="search-text"]': function (e) {
                var that = this;
                var currentText = this.$('input[name="search-text"]').val();
                setTimeout(function () {
                    // detect if the text has changed
                    var newText = that.$('input[name="search-text"]').val();
                    if (newText === currentText) {
                        that.search(newText);
                    }
                }, SEARCH_FIRE_DELAY);
            }
        },

        submit: function (event) {
            event.preventDefault();
            this.search(this.$('input[name="search-text"]').val());
        },

        search: function (searchText) {
            searchText = searchText.trim().split(' ').join('+');

            if (searchText.length < SEARCH_TEXT_MIN_LENGTH) {
                return;
            }

            // Go to the research page
            var searchUrl = [
                '#documents?search=', searchText,
                '&order=asc&limit=', SEARCH_MAX_ITEM_PER_PAGE,
                '&offset=0'
            ].join('');
            finalApp.router.navigate(searchUrl, {trigger: true});
        }

    });

    return IndexView;
});
