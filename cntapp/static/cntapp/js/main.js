require.config({
    // for development purpose, ensure the newest version js at each time
    //urlArgs: "bust=" + (new Date()).getTime(),

    paths: {
        jquery: '/static/jquery/dist/jquery',
        underscore: '/static/underscore/underscore',
        backbone: '/static/backbone/backbone',
        bootstrap_table: '/static/bootstrap-table/src/bootstrap-table',
        text: '/static/requirejs-text/text'
    }
});

require([
    'app'
], function(app) {
    $(document).ready(function () {
        app.initialize();
    });
});