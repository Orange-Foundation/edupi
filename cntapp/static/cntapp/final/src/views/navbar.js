define([
    'underscore',
    'backbone',
    'text!templates/navbar.html'
], function (_, Backbone, navbarTemplate) {

    var NAVBAR_TEMPLATE = _.template(navbarTemplate);

    var IndexView = Backbone.View.extend({

        initialize: function () {
        },

        render: function () {
            this.$el.html(NAVBAR_TEMPLATE());
            return this;
        },

        events: {
            'submit form': 'submit',
        },

        submit: function (event) {
            event.preventDefault();
            console.log('submit research...');
            // TODO check the input
            var name = this.$('input[name="search-text"]').val();
            name = name.trim().split(' ').join('+');

            // Go to the research page
            var searchUrl = '#documents?search=' + name + '&order=asc&limit=10&offset=0';
            finalApp.router.navigate(searchUrl, {trigger: true});
        }

    });

    return IndexView;
});
