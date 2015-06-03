define([
    'underscore',
    'backbone',

    'text!templates/pagination.html'
], function (_, Backbone,
             paginationTemplate) {
    var PAGINATION_TEMPLATE = _.template(paginationTemplate);
    var MAX_PRE_LINKS = 5;
    var MAX_NEXT_LINKS = 5;
    var MAX_LINKS = 10;

    var PaginationView = Backbone.View.extend({

        initialize: function (options) {
            options = options || {};
            if (typeof options.offset === 'undefined'
                || typeof options.limit === 'undefined'
                || typeof options.searchString === 'undefined'
                || typeof options.total === 'undefined') {
                throw new Error('pagination not initiated properly.')
            }

            this.offset = Number(options.offset);
            this.limit = Number(options.limit);
            this.total = Number(options.total);
            this.searchString = options.searchString;
        },

        render: function () {

            this.$el.html(PAGINATION_TEMPLATE(this.getContext()));
            return this;
        },

        // ATTENTION: it's a really dirty implementation !!! Need to rework someday !!
        getContext: function () {
            var pres = [],
                nexts = [],
                currentOffset,
                maxOffset,
                startPageNum,
                crtPageNum,
                context;
            var basicQS = [
                "#documents?search=", this.searchString,
                "&order=asc",
                "&limit=", this.limit,
                "&offset="
            ].join('');

            currentOffset = this.offset - this.limit * MAX_PRE_LINKS;
            currentOffset = currentOffset > 0 ? currentOffset : 0;
            startPageNum = currentOffset / this.limit + 1;
            for (; currentOffset < this.offset; currentOffset += this.limit) {
                pres.push(basicQS + currentOffset);
            }

            crtPageNum = currentOffset / this.limit;
            if (crtPageNum < MAX_PRE_LINKS) {
                maxOffset = this.offset + this.limit * (MAX_LINKS - crtPageNum);
            } else {
                maxOffset = this.offset + this.limit * MAX_NEXT_LINKS;
            }
            maxOffset = maxOffset < this.total ? maxOffset : this.total;
            for (currentOffset = this.offset + this.limit; currentOffset < maxOffset; currentOffset += this.limit) {
                nexts.push(basicQS + currentOffset);
            }

            context = {
                head: basicQS + 0,
                tail: basicQS + (this.total - (this.total % this.limit)),
                pres: pres,
                nexts: nexts,
                startPageNum: startPageNum
            };
            return context;
        }
    });

    return PaginationView;
});
