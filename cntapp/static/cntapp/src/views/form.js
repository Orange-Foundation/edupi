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

        /* turn a form into an Object

        Example:
             <input name='name' value='Javascript:The Good Part'>
             <input name='description' value='computer science'>
             ...
        =>
            {
                ['name', 'Javascript:The Good Part'],
                ['description', 'computer science'],
                ...
            }
         */
        serializeForm: function (form) {
            return _.object(_.map(form.serializeArray(), function (item) {
                return [item.name, item.value];
            }));
        }
    });

    return FormView;
});
