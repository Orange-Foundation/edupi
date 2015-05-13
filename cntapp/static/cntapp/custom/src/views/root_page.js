/**
 * this view only for showing root directories in home page
 */

define([
    'underscore',
    'backbone',
    'views/structure_content',
    'views/action_bar',
    'models/directory',
    'text!templates/directories_page.html',
    'text!templates/root_state_bar.html'
], function (_, Backbone,
             StructureContentView,
             ActionBarView,
             Directory,
             directoriesPageTemplate,
             rootStateBarTemplate) {
    var RootPageView, TEMPLATE, ROOT_STATE_BAR_TEMPLATE;

    TEMPLATE = _.template(directoriesPageTemplate);
    ROOT_STATE_BAR_TEMPLATE = _.template(rootStateBarTemplate);

    RootPageView = Backbone.View.extend({

        initialize: function () {
            this.currentDirectories = new Backbone.Collection({model: Directory});
        },

        render: function () {
            var contentView, actionBarView;
            this.$el.html(TEMPLATE());

            actionBarView = new ActionBarView();
            contentView = new StructureContentView({
                currentDirectories: this.currentDirectories
            });

            this.$('.directories').html(contentView.render().el);
            this.$('.action-bar').html(actionBarView.render().el);
            this.$('.state-bar').html(ROOT_STATE_BAR_TEMPLATE());
            return this;
        }
    });

    return RootPageView;
});
