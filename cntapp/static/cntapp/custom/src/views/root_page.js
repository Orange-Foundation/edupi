/**
 * this view only for showing root directories in home page
 */

define([
    'underscore',
    'backbone',
    'views/structure_content', 'views/action_bar',
    'models/directory',
    'collections/directories',
    'text!templates/basic_page.html',
    'text!templates/root_state_bar.html'
], function (_, Backbone,
             StructureContentView, ActionBarView,
             Directory,
             DirectoriesCollection,
             basicPageTemplate,
             rootStateBarTemplate) {
    var RootPageView, TEMPLATE, ROOT_STATE_BAR_TEMPLATE;

    TEMPLATE = _.template(basicPageTemplate);
    ROOT_STATE_BAR_TEMPLATE = _.template(rootStateBarTemplate);

    RootPageView = Backbone.View.extend({

        initialize: function () {
            this.currentDirectories = new DirectoriesCollection({model: Directory});
        },

        render: function () {
            var contentView, actionBarView;
            this.$el.html(TEMPLATE());

            actionBarView = new ActionBarView();
            contentView = new StructureContentView({
                currentDirectories: this.currentDirectories
            });

            this.$('.main-content').html(contentView.render().el);
            this.$('.action-bar').html(actionBarView.render().el);
            this.$('.state-bar').html(ROOT_STATE_BAR_TEMPLATE());
            this.$('.state-bar').i18n();
            return this;
        }
    });

    return RootPageView;
});
