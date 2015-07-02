define([
    'underscore', 'backbone',
    'collections/directories',
    'text!templates/link_directory_modal.html',
    'text!templates/root_directory_list.html'
], function (_, Backbone,
             DirectoriesCollection,
             linkDirectoryModal, rootDirectoriesTemplate) {
    var LinkDirectoryModalView, TEMPLATE, ROOT_DIRECTORIES_TEMPLATE;

    TEMPLATE = _.template(linkDirectoryModal);
    ROOT_DIRECTORIES_TEMPLATE = _.template(rootDirectoriesTemplate);

    LinkDirectoryModalView = Backbone.View.extend({
        initialize: function (options) {
            options = options || {};
            if (typeof options.parentId === 'undefined') {
                throw Error('parentId not specified.');
            }
            if (typeof options.path === 'undefined') {
                throw Error('path not specified.');
            }
            this.parentId = options.parentId;
            this.path = options.path;
            this.collection = new DirectoriesCollection();
            this.listenTo(this.collection, 'reset', this.refreshContent);
        },

        render: function () {
            this.$el.html(TEMPLATE());
            this.$el.i18n();
            this.fetchAndRefresh();
            return this;
        },

        refreshContent: function () {
            var current_root_id = this.path.split('/')[0];
            this.$('.modal-body').html(ROOT_DIRECTORIES_TEMPLATE({
                directories: this.collection.models,
                current_root_id: current_root_id
            }))
        },

        fetchAndRefresh: function () {
            var that = this;
            var url = cntapp.apiRoots.directories + "?root=true";
            $.getJSON(url)
                .done(function (data) {
                    that.collection.reset(data);
                });
        },

        toggle: function () {
            this.$('#link-directory-modal').modal('toggle');
        },

        events: {
            'click .btn-confirm': function () {
                // get the selected value
                var selected, url, data,
                    that = this;
                if (this.$('input[name="root-dir"]:checked').length < 1) {
                    return;
                }
                selected = this.$('input[name="root-dir"]:checked').val();
                url = cntapp.apiRoots.directories + this.parentId + '/directories/';
                data = {'id': selected};
                $.post(url, data)
                    .success(function () {
                        that.$('.modal').modal('hide');
                        Backbone.history.loadUrl(Backbone.history.fragment);  // reload current url for refreshing page
                    })
                    .fail(function (reason) {
                        console.error('fail to link directory, reason:' + reason);
                    });
            }
        }
    });

    return LinkDirectoryModalView
});