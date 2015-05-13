define([
    'underscore', 'backbone',
    'text!templates/action_bar.html',
    'text!templates/create_directory_modal.html'
], function (_, Backbone,
             actionBarTemplate, createDirectoryModalTemplate) {

    var CREATE_DIRECTORY_MODAL = _.template(createDirectoryModalTemplate),
        ACTION_BAR_TEMPLATE = _.template(actionBarTemplate);

    var ActionBarView = Backbone.View.extend({
        initialize: function (options) {
            options = options || {};
            this.path = options.path;
            this.parentId = options.parentId;
        },

        render: function () {
            var that = this;
            this.$el.html(ACTION_BAR_TEMPLATE({path: this.path, parentId: this.parentId}));
            return this;
        },

        events: {
            'click .btn-create': function () {
                this.$('.modal-area').html(CREATE_DIRECTORY_MODAL());
                console.debug('show create-directory-modal');
            },

            'submit form': 'submit'
        },

        submit: function (event) {
            var data, url,
                that = this;

            event.preventDefault();
            this.form = this.$(event.currentTarget);
            data = this.serializeForm(this.form);
            url = cntapp.apiRoots.directories;
            url = this.parentId ? url + this.parentId + "/create_sub_directory/" : url;

            $.post(url, data)
                .success(function () {
                    that.$('.modal').modal('hide');
                    Backbone.history.loadUrl(Backbone.history.fragment);  // reload current url for refreshing page
                })
                .fail(function (reason) {
                    console.error('fail to create directory, reason:' + reason);
                });
        },

        serializeForm: function (form) {
            return _.object(_.map(form.serializeArray(), function (item) {
                return [item.name, item.value];
            }));
        }
    });

    return ActionBarView;
});