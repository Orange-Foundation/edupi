define([
    'underscore',
    'backbone',
    'text!templates/nav.html'
], function (_, Backbone, navTemplate) {

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
            }
        }
    });

    return NavView;
});