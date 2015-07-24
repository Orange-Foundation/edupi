define([
    'underscore', 'backbone',
    'views/document', 'views/pagination',
    'models/document', 'collections/documents'
], function (_, Backbone,
             DocumentView, PaginationView,
             Document, Documents) {
    var parseQueryString;

    parseQueryString = function (queryString) {
        var params = {};
        if (queryString) {
            _.each(
                _.map(decodeURI(queryString).split(/&/g), function (el, i) {
                    var aux = el.split('='), o = {};
                    if (aux.length >= 1) {
                        var val = undefined;
                        if (aux.length == 2)
                            val = aux[1];
                        o[aux[0]] = val;
                    }
                    return o;
                }),
                function (o) {
                    _.extend(params, o);
                }
            );
        }
        return params;
    };

    var DocumentSearchView = Backbone.View.extend({
        tagName: "ul",
        className: "col-sm-offset-2 col-sm-8",
        id: "document-list",

        initialize: function (options) {
            options = options || {};
            // TODO: CHECK fetch url
            if (typeof options.queryString === 'undefined') {
                throw new Error('no query string defined');
            }
            this.queryString = options.queryString;
            this.collection = new Documents();
        },

        render: function () {
            var that = this;
            var fetchUrl = '/api/documents/?' + this.queryString;
            var start = Date.now();
            $.get(fetchUrl)
                .done(function (data) {
                    var params;
                    var end =   Date.now();
                    var diff = (end - start) / 1000;
                    that.$el.append(data['total'] + ' results (' + diff.toFixed(3) + ' seconds)');
                    _(data['rows']).each(function (obj) {
                        var m = new Document(obj);
                        that.$el.append(
                            new DocumentView({model: m, id: "document-" + m.id}).render().el);
                        that.collection.add(m);
                    });

                    params = parseQueryString(that.queryString);
                    if (data['total'] > params['limit']) {
                        that.$el.append(new PaginationView({
                            total: data['total'],
                            offset: params['offset'],
                            limit: params['limit'],
                            searchString: params['search']
                        }).render().el);
                    }
                });
            return this;
        }
    });

    return DocumentSearchView;
});
