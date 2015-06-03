define([
    'underscore',
    'backbone',
    'views/navbar',
    'views/statebar',
    'text!templates/body_structure.html',
    'text!templates/footer.html',
], function (_, Backbone,
             NavbarView, StateBarView,
             bodyStructureTemplate, footerTemplate) {


    var PAGE_STRUCTURE_TEMPLATE = _.template(bodyStructureTemplate);
    var FOOTER_TEMPLATE = _.template(footerTemplate);

    var ContentView = Backbone.View.extend({
        render: function () {
            this.$el.html(PAGE_STRUCTURE_TEMPLATE());
            this.$("#main-nav").html(new NavbarView().render().el);
            this.$("#footer-zone").append(FOOTER_TEMPLATE());
            return this;
        }
    });

    return ContentView;
});
