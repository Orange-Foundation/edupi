(function ($, Backbone, _, app) {

    app.models.Directory = Backbone.Model.extend({
        urlRoot: app.apiRoot + 'directories',
        defaults: {
            id: -1
        }
    });

    app.models.Document = Backbone.Model.extend({
        urlRoot: app.apiRoot + 'documents'
    });


})(jQuery, Backbone, _, app);