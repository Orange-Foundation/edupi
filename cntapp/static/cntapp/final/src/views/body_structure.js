define([
    'underscore',
    'backbone',
    'views/navbar', 'views/statebar', 'views/footer',
    'text!templates/body_structure.html',
], function (_, Backbone,
             NavbarView, StateBarView, FooterView,
             bodyStructureTemplate) {


    var PAGE_STRUCTURE_TEMPLATE = _.template(bodyStructureTemplate);

    var ContentView = Backbone.View.extend({
        render: function () {
            this.$el.html(PAGE_STRUCTURE_TEMPLATE());
            this.$("#main-nav").html(new NavbarView().render().el);
            this.$("#footer-zone").append(new FooterView().render().el);
            return this;
        }
    });

    return ContentView;
});
