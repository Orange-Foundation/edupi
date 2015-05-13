/**
 * this view is for containing directories and all the states and actions
 */

define([
    'underscore',
    'backbone',
    'views/structure_content', 'views/state_bar', 'views/action_bar',
    'models/directory',
    'collections/directories',
    'text!templates/basic_page.html'
], function (_, Backbone,
             StructureContentView, StateBarView, ActionBarView,
             Directory,
             DirectoriesCollection,
             basicPageTemplate) {
    var DirectoriesPageView, TEMPLATE;

    TEMPLATE = _.template(basicPageTemplate);

    DirectoriesPageView = Backbone.View.extend({

        initialize: function (options) {
            this.path = options.path;
            this.pathArray = options.path.split('/');
            this.parentId = this.pathArray[this.pathArray.length - 1];
            this.currentDirectories = new DirectoriesCollection({model: Directory});
        },

        render: function () {
            var contentView, stateBarView, actionBarView;
            this.$el.html(TEMPLATE());

            stateBarView = new StateBarView({path: this.path});
            actionBarView = new ActionBarView({path: this.path, parentId: this.parentId});
            contentView = new StructureContentView({
                currentDirectories: this.currentDirectories,
                path: this.path,
                parentId: this.parentId
            });

            this.$('.main-content').html(contentView.render().el);
            this.$('.state-bar').html(stateBarView.refreshAndRender().el);
            this.$('.action-bar').html(actionBarView.render().el);
            return this;
        }
    });

    return DirectoriesPageView;
});
