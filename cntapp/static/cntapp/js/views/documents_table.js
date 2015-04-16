define([
    'jquery',
    'underscore',
    'backbone',
    'views/template',
    'bootstrap_table'
], function ($, _, Backbone, TemplateView) {
    var DocumentsTableView = TemplateView.extend({
        templateName: "#documents-template",
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



