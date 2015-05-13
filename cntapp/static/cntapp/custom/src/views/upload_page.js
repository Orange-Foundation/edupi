define([
    'underscore', 'backbone',
    'views/state_bar', 'views/upload_document_to_directory',
    'models/directory',
    'text!templates/basic_page.html'
], function (_, Backbone,
             StateBarView, UploadView,
             Directory,
             basicPageTemplate) {
    var UploadPageView, TEMPLATE;

    TEMPLATE = _.template(basicPageTemplate);

    UploadPageView = Backbone.View.extend({

        initialize: function (options) {
            this.path = options.path;
            this.pathArray = options.path.split('/');
            this.parentId = this.pathArray[this.pathArray.length - 1];
        },

        render: function () {
            var stateBarView;
            this.$el.html(TEMPLATE());

            stateBarView = new StateBarView({path: this.path});
            this.$('.state-bar').html(stateBarView.refreshAndRender().el);
            this.$('.main-content').html(new UploadView({path: this.path, parentId: this.parentId}).render().el);
            return this;
        }
    });

    return UploadPageView;
});
