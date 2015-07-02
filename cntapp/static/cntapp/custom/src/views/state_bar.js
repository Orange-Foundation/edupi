define([
    'underscore',
    'backbone',
    'models/directory',
    'text!templates/state_bar.html'
], function (_, Backbone, Directory, stateBarTemplate) {

    var StateBarView = Backbone.View.extend({

        initialize: function (options) {
            this.path = options.path;

            this.template = _.template(stateBarTemplate);
            this.collection = new Backbone.Collection({model: Directory});
            this.collection.on('reset', this.render, this);
            this.collection.on('render', this.render, this);
        },

        _refreshCurrentPath: function (pathCollection, path) {
            var pathDirectories = [], pathArray,
                d, i, pathLength, dirs;

            dirs = cntapp.collections.directories;
            pathArray = path.split('/');
            for (i = 0, pathLength = pathArray.length; i < pathLength; i++) {
                d = dirs.get(pathArray[i]);
                if (typeof d === 'undefined') {
                    d = new Directory({id: pathArray[i]});
                    d.fetch({
                        success: function (directory) {
                            console.log('get dir:' + directory.get('name'));
                            pathCollection.trigger('render');  // re-render at each fetch, case for refreshing page
                        }
                    });
                }
                pathDirectories.push(d);
            }
            pathCollection.reset(pathDirectories);
        },

        render: function () {
            this.$el.html(this.template({
                path: this.collection.models
            }));
            this.$el.i18n();
            return this;
        },

        refreshAndRender: function () {
            this._refreshCurrentPath(this.collection, this.path);
            return this;
        }

    });
    return StateBarView;
});