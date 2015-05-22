/**
 * this view is for containing directories and all the states and actions
 */

define([
    'underscore',
    'backbone',
    'views/structure_content', 'views/state_bar', 'views/action_bar',
    'models/directory',
    'collections/directories', 'collections/documents',
    'text!templates/basic_page.html'
], function (_, Backbone,
             StructureContentView, StateBarView, ActionBarView,
             Directory,
             DirectoriesCollection, DocumentsCollection,
             basicPageTemplate) {
    var DirectoriesPageView, TEMPLATE;

    TEMPLATE = _.template(basicPageTemplate);

    DirectoriesPageView = Backbone.View.extend({

        initialize: function (options) {
            this.path = options.path;
            this.pathArray = options.path.split('/');
            this.parentId = this.pathArray[this.pathArray.length - 1];
            this.currentDirectories = new DirectoriesCollection({model: Directory});
            this.currentDocuments = new DocumentsCollection();
        },

        render: function () {
            var contentView, stateBarView, actionBarView;
            this.$el.html(TEMPLATE());

            stateBarView = new StateBarView({path: this.path});
            actionBarView = new ActionBarView({
                path: this.path,
                parentId: this.parentId,
                currentDocuments: this.currentDocuments
            });
            contentView = new StructureContentView({
                currentDirectories: this.currentDirectories,
                currentDocuments: this.currentDocuments,
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
