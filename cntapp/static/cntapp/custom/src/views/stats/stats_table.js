define([
    'underscore',
    'backbone',
    'text!templates/stats/stats_table.html',

    'bootstrap_table'
], function (_, Backbone,
             statsTableTemplate
) {

    var TEMPLATE = _.template(statsTableTemplate);
    var StatsTableView = Backbone.View.extend({
        initialize: function (options) {
            options = options || {};
            if (options['stats_date'] === 'undefined') {
                throw Error('stats_date is not defined.')
            }
            this.statsDate = options.stats_date;
        },

        showTable: function (data) {
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
                    title: 'Name',
                    sortable: true
                }, {
                    field: 'clicks',
                    title: 'Clicks',
                    sortable: true
                }]
            });
            this.$('#table').bootstrapTable('resetView');
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

            return this;
        },

        events: {
            'click .refresh-stats': function () {
                var now = (new Date()).getTime();  // Time in milliseconds
                var that = this;
                console.log('run');
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