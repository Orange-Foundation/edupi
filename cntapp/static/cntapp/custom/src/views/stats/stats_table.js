define([
    'underscore',
    'backbone',
    'text!templates/stats/stats_table.html'
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
                    console.log(results);
                    var i;
                    _.each(results, function (data) {
                        that.$('.stats-list').append(data['name'] + ":" + data['clicks'] + "<br>");
                        console.log(data);
                    });
                }
            });

            return this;
        },

        events: {
            'click .refresh-stats': function () {
                var now = (new Date()).getTime();
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
                        //if (result['status'] === 'running') {
                            Backbone.history.loadUrl(Backbone.history.fragment);
                        //}
                        cntapp.router.navigate('stats', {trigger: true})
                    }
                })
            }
        }


    });
    return StatsTableView;
});