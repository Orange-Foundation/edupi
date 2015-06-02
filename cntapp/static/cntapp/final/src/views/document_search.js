define([
    'underscore',
    'backbone',
    'views/document',
    'models/document',
    'collections/documents',
    'text!templates/document_list.html'
], function (_, Backbone,
             DocumentView, Document, Documents,
             documentListTemplate) {
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

            // {search: "ja", order: "asc", limit: "10", offset: "0"}
            //var params = parseQueryString(this.queryString);
        },

        render: function () {
            var that = this;
            var fetchUrl = '/api/documents/?' + this.queryString;
            $.get(fetchUrl)
                .done(function (data) {
                    //that.$el.append(_.template(paginationTemplate)());
                    that.$el.append('total:' + data['total']);
                    // TODO: show pagination
                    _(data['rows']).each(function (obj) {
                        var m = new Document(obj);
                        that.$el.append(
                            new DocumentView({model: m, id: "document-" + m.id}).render().el);
                        that.collection.add(m);
                    });
                });
            return this;
        }
    });

    return DocumentSearchView;
});
