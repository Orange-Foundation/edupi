define([
    'underscore',
    'backbone',

    'bootstrap_table',
    'bootstrap_table_editable'
], function (_, Backbone) {

    var DocumentsTableView = Backbone.View.extend({
        render: function () {
            this.$el.html([
                    '<link rel="stylesheet" href="/static/x-editable/dist/bootstrap3-editable/css/bootstrap-editable.css">',
                    "<table id='table'></table>",
                ].join('')
            );

            var that = this;

            this.$('#table').bootstrapTable({
                height: 519,
                url: '/api/documents/',
                pagination: 'true',
                showRefresh: 'true',
                showColumns: 'true',
                showToggle: 'true',
                search: 'true',
                sidePagination: 'server',

                onEditableSave: function (name, data) {
                    var url = "/api/documents/" + data.id + "/";
                    $.ajax({
                        type: "PATCH",
                        url: url,
                        contentType: "application/json",
                        data: JSON.stringify({
                                'name': data.name,
                                'description': data.description
                            }
                        ),
                        success: function (result) {
                            console.log("updated");
                            that.$('#table').bootstrapTable('resetView');
                        }
                    });
                },

                columns: [{
                    field: 'id',
                    title: 'ID',
                    sortable: true
                }, {
                    field: 'name',
                    title: 'Name',
                    sortable: true,
                    editable: true
                }, {
                    field: 'description',
                    title: 'Description',
                    sortable: true,
                    editable: true
                }, {
                    field: 'type',
                    title: 'Type',
                    sortable: true
                }, {
                    field: 'action',
                    title: 'Action',
                    formatter: function () {
                        return [
                            '<a class="detail" href="javascript:void(0)" title="Detail">',
                            '<i class="glyphicon glyphicon-plus-sign"></i>',
                            '</a> ',
                            '<a class="remove" href="javascript:void(0)" title="Remove">',
                            '<i class="glyphicon glyphicon-remove"></i>',
                            '</a>'
                        ].join('');
                    },
                    events: {
                        'click .detail': function (e, value, row, index) {
                            console.log("TODO: show document detail");
                        },
                        'click .remove': function (e, value, row, index) {
                            var url = "/api/documents/" + row.id + "/";
                            $.ajax({
                                url: url,
                                type: "DELETE",
                                success: function (result) {
                                    console.log("deleted");
                                    that.$('table').bootstrapTable('remove', {
                                        field: 'id',
                                        values: [row.id]
                                    });
                                }
                            });
                        }
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



