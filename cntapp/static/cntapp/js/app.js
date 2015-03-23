var app = (function($) {
    var config = $('#config'),
        app = JSON.parse(config.text());

    $(document).ready(function () {
        app.router = new app.Router();
    });

    return app;
})(jQuery);