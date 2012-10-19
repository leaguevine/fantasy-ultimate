(function() {
    //usage: log('inside coolFunc', this, arguments);
    //paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
    window.log = function() {
        log.history = log.history || [];   // store logs to an array for reference
        log.history.push(arguments);
        //arguments.callee = arguments.callee.caller;
        if(this.console && this.console.log) { console.log( Array.prototype.slice.call(arguments) ); }
    };
    //make it safe to use console.log always
    (function(b) {function c(){}for(var d="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,markTimeline,profile,profileEnd,time,timeEnd,trace,warn".split(","),a;a;a=d.pop()){b[a]=b[a]||c;}})(window.console=window.console||{});

    var isAbsolute = function(url) {
        return (/^http:.*/).test(url) || (/^https:.*/).test(url);
    };

    var hasAccessToken = function(url) {
        return (/access_token=/).test(url);
    };

    var appendQueryParam = function(url, key, value) {
        if (url.indexOf('?') == -1) {
            url = url + '?';
        } else {
            url = url + '&';
        }
        return url + key + "=" + value;
    };

    var paramValue = function(v) {
        if (_.isArray(v)) {
            return "[" + v.join(",") + "]";
        }
        return v;
    };

    var GetListRequest = function(lv, url, params) {
        this.lv = lv;

        this.url = url;
        this.orderBy = params.orderBy;
        this.fields = params.fields;
        this.pageSize = params.pageSize ? Math.min(params.pageSize, 200) : 200;
        this.offset = params.offset;
        this.extraParams = params.extraParams;

        this.meta = null;
    };

    _.extend(GetListRequest.prototype, {
        hasMorePages: function() {
            return !this.meta || this.meta.next;
        },

        getNextPage: function(cb) {
            if (!this.hasMorePages()) {
                cb();
                return;
            }

            var _this = this;
            var success = function(result) {
                _this.meta = result.meta;
                cb(result.objects);
            };

            if (this.meta) {
                this.lv.get(this.meta.next, success);
            } else {
                var params = {};
                _.each(this.extraParams, function(v, k) {
                    params[k] = paramValue(v);
                });
                if (this.orderBy) {
                    params.order_by = paramValue(this.orderBy);
                }
                if (this.fields) {
                    params.fields = paramValue(this.fields);
                }
                if (this.pageSize) {
                    params.limit = this.pageSize;
                }
                if (this.offset) {
                    params.offset = this.offset;
                }
                this.lv.get(this.url, params, success);
            }
        },

        getAll: function(cb) {
            var objects = [];
            var _this = this;
            var success = function(objs) {
                Array.prototype.push.apply(objects, objs);
                if (_this.hasMorePages()) {
                    _this.getNextPage(success);
                } else {
                    cb(objects);
                }
            };

            this.getNextPage(success);
        }
    });

    var LV = function() {
        this.accessToken = window.app_data.lvat;
    };

    _.extend(LV.prototype, {
        makeApiUrl: function(url) {
            if (!isAbsolute(url)) {
                url = "https://api.leaguevine.com/v1" + url;
            }
            if (!hasAccessToken(url)) {
                url = appendQueryParam(url, "access_token", this.accessToken);
            }
            return url;
        },

        get: function(url, p1, p2, p3) {
            if (_.isFunction(p1)) {
                this.api({ url: url, cb: p1, error: p2 });
            } else {
                this.api({ url: url, params: p1, cb: p2, error: p3 });
            }
        },

        api: function(args) {
            args = args || {};
            var method = args.method || "GET";
            var cb = args.cb || function() {};
            var error = args.error || function() {};
            var url = this.makeApiUrl(args.url);
            var data = null;
            var dataType = null;
            if (args.params) {
                if (method == "GET") {
                    data = jQuery.param(args.params);
                } else {
                    data = JSON.stringify(args.params);
                    dataType = "json";
                }
            }

            $.ajax({
                url: url,
                data: data,
                type: method,
                contentType: "application/json",
                dataType: dataType,
                context: this,
                success: function(data) { cb(data); },
                error: function(e) { log("API error: " + e); error(); }
            });
        },

        getList: function(url, options) {
            return new GetListRequest(this, url, options);
        }
    });

    window.LV = new LV();
})();
