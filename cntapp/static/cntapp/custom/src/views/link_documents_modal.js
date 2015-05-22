/*
 This is a modal view
 */
define([
    'underscore', 'backbone',
    'models/document',
    'text!templates/link_documents_modal.html',

    'bootstrap_table',
    //'bootstrap_table_editable'
], function (_, Backbone,
             Document,
             linkDocumentsModal) {
    var DocumentsTableView, LinkDocumentModalView, TEMPLATE;

    var UNLINK_SIGN = [
        '<a class="unlink" href="javascript:void(0)" title="Unlink">',
        '<i class="glyphicon glyphicon-minus-sign"></i>',
        '</a> '
    ].join('');

    var LINK_SIGN = [
        '<a class="link" href="javascript:void(0)" title="Link">',
        '<i class="glyphicon glyphicon-link"></i>',
        '</a> '
    ].join('');

    TEMPLATE = _.template(linkDocumentsModal);

    DocumentsTableView = Backbone.View.extend({
        initialize: function (options) {
            if (typeof options.currentDocuments === 'undefined') {
                throw Error('LinkDocumentModal not inited correctly.');
            }
            this.currentDocuments = options.currentDocuments;
            this.parentId = options.parentId;
        },

        render: function () {
            this.$el.html([
                    //'<link rel="stylesheet" href="/static/x-editable/dist/bootstrap3-editable/css/bootstrap-editable.css">',
                    "<table id='table'></table>",
                ].join('')
            );

            var that = this;

            this.$('#table').bootstrapTable({
                height: 519,
                url: '/api/documents/',
                showRefresh: 'true',
                showColumns: 'true',
                showToggle: 'true',
                search: 'true',
                pagination: 'true',
                sidePagination: 'server',

                columns: [{
                    field: 'id',
                    title: 'ID',
                    sortable: true
                }, {
                    field: 'name',
                    title: 'Name',
                    sortable: true
                }, {
                    field: 'description',
                    title: 'Description',
                    sortable: true
                }, {
                    field: 'type',
                    title: 'Type',
                    sortable: true,
                    formatter: function (value, row, index) {
                        var ret;
                        switch (value) {
                            case 'p':
                                ret = 'Pdf';
                                break;
                            case 'i':
                                ret = 'Image';
                                break;
                            case 'v':
                                ret = 'Video';
                                break;
                            case 'a':
                                ret = 'Audio';
                                break;
                            case 'g':
                                ret = 'Apk';
                                break;
                            default :
                                ret = 'Other';
                        }
                        return ret;
                    }
                }, {
                    field: 'action',
                    title: 'Action',
                    formatter: function (value, row, index) {
                        if (value) {
                            return value;
                        }
                        var length = that.currentDocuments.length;
                        // Search if the document is in the current directory
                        for (var i = 0; i < length; i++) {
                            if (row.id == that.currentDocuments.at(i).get('id')) {
                                return UNLINK_SIGN;
                            }
                        }
                        return LINK_SIGN;
                    },
                    events: {
                        'click .link': function (e, value, row, index) {
                            var url = cntapp.apiRoots.directories + that.parentId + '/documents/';
                            var data = {"documents": row.id};
                            $.ajax({
                                type: "POST",
                                traditional: true,
                                url: url,
                                data: data,
                                success: function () {
                                    that.$('#table').bootstrapTable('updateCell', {
                                        rowIndex: index,
                                        fieldName: 'action',
                                        fieldValue: UNLINK_SIGN
                                    });
                                    that.currentDocuments.trigger('render');
                                },
                                error: function (request, status, error) {
                                    alert(error);
                                }
                            });
                        },
                        'click .unlink': function (e, value, row, index) {
                            console.log("TODO: unlink the document");
                            var url = cntapp.apiRoots.directories + that.parentId + '/documents/';
                            var data = {"documents": row.id};
                            $.ajax({
                                type: "DELETE",
                                traditional: true,
                                url: url,
                                data: data,
                                success: function () {
                                    that.$('#table').bootstrapTable('updateCell', {
                                        rowIndex: index,
                                        fieldName: 'action',
                                        fieldValue: LINK_SIGN
                                    });
                                    that.currentDocuments.trigger('render');
                                },
                                error: function (request, status, error) {
                                    alert(error);
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

    LinkDocumentModalView = Backbone.View.extend({
        initialize: function (options) {
            options = options || {};
            this.parentId = options.parentId;
            this.currentDocuments = options.currentDocuments;
            this.documentsTableView = new DocumentsTableView({
                currentDocuments: this.currentDocuments,
                parentId: this.parentId
            });
        },
        render: function () {
            this.$el.html(TEMPLATE());
            this.$('.modal-body').html(this.documentsTableView.render().el);
            return this;
        },
        toggle: function () {
            this.$('#link-documents-modal').modal('toggle');
        }
    });

    return LinkDocumentModalView
});