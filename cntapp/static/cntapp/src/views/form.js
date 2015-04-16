define([
    'underscore',
    'backbone',
    'views/template'
], function (_, Backbone, TemplateView) {

    var FormView = TemplateView.extend({
        events: {
            'submit form': 'submit'
        },

        submit: function (event) {
            event.preventDefault();
            this.form = $(event.currentTarget);
        },

        done: function (event) {
            if (event) {
                event.preventDefault();
            }
            this.remove();
        },

        serializeForm: function (form) {
            return _.object(_.map(form.serializeArray(), function (item) {
                return [item.name, item.value];
            }));
        }
    });

    return FormView;
});
