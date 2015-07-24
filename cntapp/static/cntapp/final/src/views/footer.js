define([
    'underscore',
    'backbone',
    'text!templates/footer.html',
], function (_, Backbone,
             footerTemplate) {
    var TEMPLATE = _.template(footerTemplate);

    var FooterView = Backbone.View.extend({
        render: function () {
            this.$el.html(TEMPLATE());
            this.$el.i18n();
            return this;
        },

        // TODO: this code is extracted from the `custom` module, may be need to put into `shared` ?
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


    return FooterView;
});