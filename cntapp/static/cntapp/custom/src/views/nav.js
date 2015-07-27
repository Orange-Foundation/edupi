define([
    'underscore',
    'backbone',
    'text!templates/nav.html'
], function (_, Backbone, navTemplate) {
    var SEARCH_FIRE_DELAY = 800; // millisecond

    var NavView = Backbone.View.extend({
        initialize: function () {
            this.render();
        },
        render: function () {
            var template = _.template(navTemplate);
            this.$el.html(template());
            return this;
        },
        setCookie: function (cname, cvalue, exdays) {
            var d = new Date();
            d.setTime(d.getTime() + (exdays*24*60*60*1000));
            var expires = "expires="+d.toUTCString();
            document.cookie = cname + "=" + cvalue + "; " + expires;
        },
        events: {
            'click .lang-en': function () {
                this.setCookie('i18next', 'en', 1);
                location.reload();
            },
            'click .lang-fr': function () {
                this.setCookie('i18next', 'fr', 1);
                location.reload();
            },
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
            var SEARCH_MAX_ITEM_PER_PAGE = 20;
            var SEARCH_TEXT_MIN_LENGTH = 0;

            if (searchText.length < SEARCH_TEXT_MIN_LENGTH) {
                return;
            }

            // Go to the research page
            var searchUrl = [
                '#documents?search=', searchText,
                '&order=asc&limit=', SEARCH_MAX_ITEM_PER_PAGE,
                '&offset=0'
            ].join('');
            console.log(searchUrl);
            cntapp.router.navigate(searchUrl, {trigger: true});
        }
    });

    return NavView;
});