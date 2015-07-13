define([
    'underscore',
    'backbone',
    'views/stats/stats_table',
    'text!templates/stats/stats_page.html',
    'text!templates/stats/no_stats.html',
], function (_, Backbone,
             StatsTableView,
             statsPageTemplate,
             noStatsTemplate
) {

    var TEMPLATE = _.template(statsPageTemplate);
    var NO_STATS_TEMPLATE = _.template(noStatsTemplate);

    var StatsPageView = Backbone.View.extend({
        initialize: function () {
            this.stats_date = (new Date()).getTime();
        },

        showLatestStats: function () {
            var that = this;
            $.ajax({
                type: "GET",
                url: '/custom/stats/',
                success: function (statsList) {
                    console.log(statsList);
                    if (statsList.length < 1) {
                        that.$('.info-zone').html(NO_STATS_TEMPLATE());
                    } else {
                        var latestJsonStats = statsList[0];
                        var i;
                        for (i = 1; i < statsList.length; i++) {
                            if (that._compare_json_file_name(statsList[i], latestJsonStats)) {
                                latestJsonStats = statsList[i];
                            }
                        }
                        that.$('.info-zone').html(
                            new StatsTableView({
                                'stats_date': latestJsonStats.slice(0, -5)
                            }).render().el
                        );
                    }
                }
            });
        },

        _compare_json_file_name: function (a, b) {
            // param: DATE_1.json, DATE_2.json
            var date_1 = Number(a.slice(0, -5));
            var date_2 = Number(b.slice(0, -5));
            return date_1 > date_2;
        },

        heartBeatCheck: function () {
            var that = this;
            setTimeout(function () {
                $.ajax({
                    type: "GET",
                    url: '/custom/stats/status/',
                    success: function (result) {
                        if (result['status'] === 'running') {
                            that.$('.info-zone').append('.');
                            that.heartBeatCheck();
                        } else {
                            Backbone.history.loadUrl(Backbone.history.fragment);
                        }
                    }
                });
            }, 1000);
        },

        render: function () {
            this.$el.html(TEMPLATE());
            var that = this;

            $.ajax({
                type: "GET",
                url: '/custom/stats/status/',
                success: function (result) {
                    console.log(result);
                    if (result['status'] === 'running') {
                        that.$('.info-zone').html('Please wait, the server is crunching data for you ...');
                        that.heartBeatCheck();
                    } else {
                        that.$('.info-zone').html('The server is available');
                        that.showLatestStats();
                    }
                }
            });
            return this;
        },

        events: {
            'click .refresh-stats': function () {
                var now = (new Date()).getTime();
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
                        //if (result['status'] === 'running') {
                        Backbone.history.loadUrl(Backbone.history.fragment);
                        //}
                        cntapp.router.navigate('stats', {trigger: true})
                    }
                })
            }
        }

        //events: {
           /* 'click .generate-stats': function () {
                var that = this;
                console.log('run');
                $.ajax({
                    type: 'GET',
                    url: '/custom/stats/start/',
                    contentType: "application/json",
                    data: {
                        stats_date: that.stats_date
                    },
                    success: function (result) {
                        console.log(result);
                        that.$('.status').html('status: ' + result['status'])
                    }
                })
            },

            'click .get-status': function () {
                console.log('get status');
                var that = this;
                $.ajax({
                    type: "GET",
                    url: '/custom/stats/status/',
                    contentType: "application/json",
                    data: {
                        stats_date: that.stats_date
                    },
                    success: function (result) {
                        console.log(result);
                        that.$('.status').html('status: ' + result['status'])
                    }
                });
            },

            'click .get-stats': function () {
                console.log('get-stats');
                var that = this;
                $.ajax({
                    type: "GET",
                    url: '/custom/documents_stats/',
                    contentType: "application/json",
                    data: {
                        stats_date: that.stats_date
                    },
                    success: function (results) {
                        console.log(results);
                        that.$('.stats').html('stats');
                        var i;
                        _.each(results, function (data) {
                            that.$('.stats').html(data['name'] + ":" + data['clicks'] + "<br>");
                        });
                    }
                });
            }
            */
        //}
    });
    return StatsPageView;
});