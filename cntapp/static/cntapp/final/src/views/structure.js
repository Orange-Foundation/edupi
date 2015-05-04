define([
    'underscore',
    'backbone',
    'views/navbar',
    'views/statebar',
    'text!templates/page_structure.html',
    'text!templates/footer.html',
], function (_, Backbone,
             NavbarView, StateBarView,
             pageStructureTemplate, footerTemplate) {


    var PAGE_STRUCTURE_TEMPLATE = _.template(pageStructureTemplate);
    var FOOTER_TEMPLATE = _.template(footerTemplate);

    var ContentView = Backbone.View.extend({

        render: function () {
            this.$el.html(PAGE_STRUCTURE_TEMPLATE());
            this.$("#nav-zone").html(new NavbarView().render().el);
            //this.$("#nav-zone").append(new StateBarView({path: path}).render().el);
            this.$("#footer-zone").append(FOOTER_TEMPLATE());
            return this;
        }
    });

    return ContentView;
});
