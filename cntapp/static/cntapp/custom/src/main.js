require.config({
    // for development purpose, ensure the newest version js at each time
    //urlArgs: "bust=" + (new Date()).getTime(),
    urlArgs: "bust=0.1.0",

    paths: {
        'jquery': '/static/jquery/dist/jquery',
        'underscore': '/static/underscore/underscore',
        'backbone': '/static/backbone/backbone',
        'bootstrap': '/static/bootstrap/dist/js/bootstrap',
        'bootstrap_editable': '/static/x-editable/dist/bootstrap3-editable/js/bootstrap-editable',
        'bootstrap_table': '/static/bootstrap-table/src/bootstrap-table',
        'bootstrap_table_editable': '/static/bootstrap-table/src/extensions/editable/bootstrap-table-editable',
        'text': '/static/requirejs-text/text',
        'dropzone': '/static/dropzone/dist/dropzone-amd-module',
    },
    shim: {
        'underscore': {
            exports: '_'
        },
        'backbone': {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        'bootstrap_table_editable': {
            deps: ['bootstrap_editable'],
            exports: 'bootstrap_table_editable'
        }
    }
});

require(['jquery', 'app'], function($, app) {
    $(document).ready(function () {
        cntapp = app;
    });
});