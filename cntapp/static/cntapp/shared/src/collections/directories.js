define([
    'backbone',
    'models/directory'
], function (Backbone, Directory) {

    var DirectoriesCollection = Backbone.Collection.extend({
        url: '/api/directories/',
        model: Directory
    });

    return DirectoriesCollection;
});
