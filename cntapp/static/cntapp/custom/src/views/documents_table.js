define([
    'underscore',
    'backbone',

    'bootstrap_table'
], function (_, Backbone) {

    var DocumentsTableView = Backbone.View.extend({
        render: function () {
            this.$el.html("<table id='table'></table>");

            this.$('#table').bootstrapTable({
                height: 519,
                url: '/api/documents/',
                pagination: 'true',
                showRefresh: 'true',
                showColumns: 'true',
                showToggle: 'true',
                search: 'true',
                sidePagination: 'server',

                columns: [{
                    field: 'name',
                    title: 'Name'
                }, {
                    field: 'description',
                    title: 'Description'
                }, {
                    field: 'action',
                    title: 'Action',
                    formatter: function () {
                        return [
                            '<a class="remove" href="javascript:void(0)" title="Remove">',
                            '<i class="glyphicon glyphicon-remove"></i>',
                            '</a>'
                        ].join('');
                    }
                }]
            });
            // adjust the header
            this.$('#table').bootstrapTable('resetView');
            return this;
        }
    });

    return DocumentsTableView;
});



