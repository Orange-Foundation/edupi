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
        'text': '../../../../../libs/bower_components/requirejs-text/text',

        // shared modules
        'collections': '../../shared/src/collections',
        'models': '../../shared/src/models',
    }
})
