define([
    'underscore',
    'backbone',
    'models/document',
    'text!templates/stats/stats_table.html',
    'text!templates/file_play_modal.html',

    'bootstrap_table'
], function (_, Backbone,
             Document,
             statsTableTemplate,
             filePlayModalTemplate
) {

    var TEMPLATE = _.template(statsTableTemplate);
    var FILE_PLAY_MODAL_TEMPLATE = _.template(filePlayModalTemplate);

    var StatsTableView = Backbone.View.extend({
        initialize: function (options) {
            options = options || {};
            if (options['stats_date'] === 'undefined') {
                throw Error('stats_date is not defined.')
            }
            this.statsDate = options.stats_date;
        },

        showDocumentInModal: function (model) {
            var that = this;
            var fileId = '#file-' + model.get('id');
            this.$('.modal-area').html(FILE_PLAY_MODAL_TEMPLATE({model: model}));

            // auto-play video and audio
            if (['v', 'a'].indexOf(model.get('type')) > -1) {
                this.$(".modal").on('hidden.bs.modal', function () {
                    that.$(fileId).get(0).pause();
                });
                this.$(".modal").on('shown.bs.modal', function () {
                    that.$(fileId).get(0).play();
                });
            }

            this.$('.modal').modal('show');
        },

        showTable: function (data) {
            var that = this;

            this.$('#table').bootstrapTable({
                data: data,
                showColumns: 'true',
                showToggle: 'true',
                search: 'true',
                pagination: 'true',

                columns: [{
                    field: 'id',
                    title: 'ID',
                    sortable: true
                }, {
                    field: 'name',
                    title: i18n.t('Name'),
                    sortable: true,
                    formatter: function (value, row, index) {
                        return '<a type="button" class="btn-play">' + value + '</a>';
                    },
                    events: {
                        'click .btn-play': function (e, value, row, index) {
                            if (['v', 'i', 'a', 'p'].indexOf(row['type']) > -1) {
                                that.showDocumentInModal(new Document(row));
                            } else {
                                var win = window.open(row['file'], '_blank');
                                win.focus();
                            }
                        }
                    }
                }, {
                    field: 'description',
                    title: i18n.t('Description'),
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
                    field: 'clicks',
                    title: i18n.t('Clicks'),
                    sortable: true
                }]
            });
        },

        render: function () {
            var that = this;
            var date = new Date(Number(this.statsDate)).toLocaleString();
            this.$el.html(TEMPLATE({
                statsDate: date
            }));
            $.ajax({
                type: "GET",
                url: '/custom/documents_stats/',
                contentType: "application/json",
                data: {
                    stats_date: that.statsDate
                },
                success: function (results) {
                    that.showTable(results);
                }
            });

            this.$el.i18n();

            return this;
        },

        events: {
            'click .refresh-stats': function () {
                var now = (new Date()).getTime();  // Time in milliseconds
                var that = this;
                $.ajax({
                    type: 'GET',
                    url: '/custom/stats/start/',
                    contentType: "application/json",
                    data: {
                        stats_date: now
                    },
                    success: function (result) {
                        console.debug(result);
                        if (result['status'] === 'started') {
                            Backbone.history.loadUrl(Backbone.history.fragment);
                        } else {
                            console.error('cannot start running stats, status:' + result['status']);
                        }
                    }
                })
            }
        }
    });
    return StatsTableView;
});
