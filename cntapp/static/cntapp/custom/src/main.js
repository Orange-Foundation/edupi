require.config({
    // for development purpose, ensure the newest version js at each time
    urlArgs: "bust=" + (new Date()).getTime(),

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
        'i18n': '/static/i18next/i18next',

        // shared modules
        'collections': '../../shared/src/collections',
        'models': '../../shared/src/models',
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
        },
        'i18n': {
            deps: ['jquery'],
            exports: 'i18n'
        }
    }
});

define('kickstart', function (require) {
    // import external js modules
    require('bootstrap');

    // define global variables here if needed
    // `cntapp` contains the current state of the application
    cntapp = require('app');
});

require(['jquery'], function($) {
    $(document).ready(function () {
        require(['kickstart']);
    });
});