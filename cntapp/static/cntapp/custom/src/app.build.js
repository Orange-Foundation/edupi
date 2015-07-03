({
    baseUrl: "./",

    out: "../all.js",
    optimize: "uglify2",

    include: ['main'],

    wrap: true,

    paths: {
        'jquery': '../../../../../libs/bower_components/jquery/dist/jquery',
        'underscore': '../../../../../libs/bower_components/underscore/underscore',
        'backbone': '../../../../../libs/bower_components/backbone/backbone',
        'bootstrap': '../../../../../libs/bower_components/bootstrap/dist/js/bootstrap',
        'bootstrap_editable': '../../../../../libs/bower_components/x-editable/dist/bootstrap3-editable/js/bootstrap-editable',
        'bootstrap_table': '../../../../../libs/bower_components/bootstrap-table/src/bootstrap-table',
        'bootstrap_table_editable': '../../../../../libs/bower_components/bootstrap-table/src/extensions/editable/bootstrap-table-editable',
        'text': '../../../../../libs/bower_components/requirejs-text/text',
        'dropzone': '../../../../../libs/bower_components/dropzone/dist/dropzone-amd-module',
        'i18n': '../../../../../libs/bower_components/i18next/i18next',

        // shared modules
        'collections': '../../shared/src/collections',
        'models': '../../shared/src/models',
    }
})
