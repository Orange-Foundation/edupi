define([
    'jquery',
    'underscore',
    'backbone',
    'views/template',
    'text!templates/documents_table.html',

    'bootstrap_table'
], function ($, _, Backbone, TemplateView, documentsTableTemplate) {
    var DocumentsTableView = TemplateView.extend({
        initialize: function () {
            this.template = _.template(documentsTableTemplate);
        },
        render: function () {
            TemplateView.prototype.render.apply(this);
            // convert Document models to native JSON objects and pass to table
            $('#table').bootstrapTable();
            // adjust the header
            $('#table').bootstrapTable('resetView');
            return this;
        }
    });

    return DocumentsTableView;
});



