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
            this.parentId = options.parentId;
            //this.template = _.template(actionBarTemplate);
        },

        render: function () {
            var that = this;
            this.$el.html(ACTION_BAR_TEMPLATE({parentId: this.parentId}));
            return this;
        },

        events: {
            'click .btn-create': function () {
                console.log('creating ...');
                this.$el.append(CREATE_DIRECTORY_MODAL());
                this.$('.modal-area').html(CREATE_DIRECTORY_MODAL());
            },

            'submit form': 'submit'
        },

        submit: function (event) {
            event.preventDefault();
            console.log('prevent submit');
            this.form = this.$(event.currentTarget);
            var data = this.serializeForm(this.form);
            var url = "/api/directories/";
            if (this.parentId) {
                url = url + this.parentId + "/create_sub_directory/";
            }

            $.post(url, data)
                .success($.proxy(this.createSuccess, this))
                .fail($.proxy(this.failure, this));
        },

        createSuccess: function () {
            this.$('.modal').modal('hide');
            Backbone.history.loadUrl(Backbone.history.fragment);
        },

        serializeForm: function (form) {
            return _.object(_.map(form.serializeArray(), function (item) {
                return [item.name, item.value];
            }));
        }
    });

    return ActionBarView;
});