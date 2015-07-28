define([
    'underscore',
    'backbone',
    'models/directory',
    'collections/directories',
    'text!templates/statebar.html'
], function (_, Backbone,
             Directory,
             DirectoriesCollection,
             navbarTemplate) {

    var STATEBAR_TEMPLATE = _.template(navbarTemplate);

    var StateBarView = Backbone.View.extend({

        initialize: function (options) {
            options = options || {};
            if (typeof options.path === 'undefined') {
                throw new Error('path not defined');
            }
            this.path = options.path;

            this.pathCollection = new Backbone.Collection({model: Directory});
            this.pathCollection.on('reset', this.render, this);
            this.pathCollection.on('render', this.render, this);
        },

        render: function () {
            this.$el.html(STATEBAR_TEMPLATE({
                path: this.pathCollection.models
            }));
            this.$el.i18n();
            return this;
        },

        refreshAndRender: function () {
            this._refreshCurrentPath(this.pathCollection, this.path);
            return this;
        },

        _refreshCurrentPath: function (pathCollection, path) {
            var pathDirectories = [], pathArray,
                d, i, pathLength, dirs;

            dirs = finalApp.collections.directories;
            pathArray = path.split('/');
            for (i = 0, pathLength = pathArray.length; i < pathLength; i++) {
                d = dirs.get(pathArray[i]);
                if (typeof d === 'undefined') {
                    d = new Directory({id: pathArray[i]});
                    d.fetch({
                        success: function (directory) {
                            pathCollection.trigger('render');  // re-render at each fetch, case for refreshing page
                        }
                    });
                }
                pathDirectories.push(d);
            }
            pathCollection.reset(pathDirectories);
        }
    });

    return StateBarView;
});
