(function ($, Backbone, _, app) {

    app.models.Directory = Backbone.Model.extend({
        urlRoot: app.apiRoot + 'directories',
        defaults: {
            id: -1
        }
    });

})(jQuery, Backbone, _, app);