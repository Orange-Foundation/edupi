require.config({
    // for development purpose, ensure the newest version js at each time
    //urlArgs: "bust=" + (new Date()).getTime(),
    urlArgs: "bust=v1.4.0",

    paths: {
        'jquery': '/static/jquery/dist/jquery',
        'underscore': '/static/underscore/underscore',
        'backbone': '/static/backbone/backbone',
        'bootstrap': '/static/bootstrap/dist/js/bootstrap',
        'text': '/static/requirejs-text/text',
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
        }
    }
});

require(['jquery', 'app'], function($, app) {
    $(document).ready(function () {
        finalApp = app;
    });
});
