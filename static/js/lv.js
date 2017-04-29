((() => {
    //usage: log('inside coolFunc', this, arguments);
    //paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
    window.log = function(...args) {
        log.history = log.history || [];   // store logs to an array for reference
        log.history.push(args);
        //arguments.callee = arguments.callee.caller;
        if(this.console && this.console.log) { console.log( Array.prototype.slice.call(args) ); }
    };
    //make it safe to use console.log always
    ((b => {function c(){}for(var d="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,markTimeline,profile,profileEnd,time,timeEnd,trace,warn".split(","),a;a;a=d.pop()){b[a]=b[a]||c;}}))(window.console=window.console||{});

    var isAbsolute = url => (/^http:.*/).test(url) || (/^https:.*/).test(url);

    var hasAccessToken = url => (/access_token=/).test(url);

    var appendQueryParam = (url, key, value) => {
        if (url.indexOf('?') == -1) {
            url = url + '?';
        } else {
            url = url + '&';
        }
        return url + key + "=" + value;
    };

    var paramValue = v => {
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
        hasMorePages() {
            return !this.meta || this.meta.next;
        },

        getNextPage(cb) {
            if (!this.hasMorePages()) {
                cb();
                return;
            }

            var _this = this;
            var success = result => {
                _this.meta = result.meta;
                cb(result.objects);
            };

            if (this.meta) {
                this.lv.get(this.meta.next, success);
            } else {
                var params = {};
                _.each(this.extraParams, (v, k) => {
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

        getAll(cb) {
            var objects = [];
            var _this = this;
            var success = objs => {
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

    var REGEXP_ISODATE = new RegExp("^([0-9]{4})-?([0-9]{2})-?([0-9]{2})" +
            //4 5:Hour      6:Min       7:Sec
             "(T([0-9]{2}):?([0-9]{2}):?([0-9]{2})" +
            //8  9:frac
             "(.([0-9]+))?" +
            //10 1112+/-13 tzhr  14:Min
             "(Z|(([-+])([0-9]{2}):([0-9]{2}))?)?)?$");

    var isoDate = str => {
        var d = str.match(REGEXP_ISODATE);

        var offset = 0;
        var date = new Date(d[1], 0, 1);

        if (d[2]) { date.setMonth(d[2] - 1); }
        if (d[3]) { date.setDate(d[3]); }
        if (d[5]) { date.setHours(d[5]); }
        if (d[6]) { date.setMinutes(d[6]); }
        if (d[7]) { date.setSeconds(d[7]); }
        if (d[10]) {
            if (d[10] != 'Z') {
                offset = (Number(d[13]) * 60) + Number(d[14]);
                offset *= ((d[12] == '-') ? 1 : -1);
            }
            // Only offset the timezone by our own if there is a timezone
            // specified. Otherwise we assume the time is "naive" and is intended
            // to be displayed in the user's default timezone.
            offset -= date.getTimezoneOffset();
        }

        time = (Number(date) + (offset * 60 * 1000));
        var result = new Date();
        result.setTime(Number(time));
        return result;
    };

    var LV = function() {
        this.accessToken = window.app_data.lvat;
    };

    _.extend(LV.prototype, {
        makeApiUrl(url) {
            if (!isAbsolute(url)) {
                url = "https://api.leaguevine.com/v1" + url;
            }
            if (!hasAccessToken(url)) {
                url = appendQueryParam(url, "access_token", this.accessToken);
            }
            return url;
        },

        get(url, p1, p2, p3) {
            if (_.isFunction(p1)) {
                this.api({ url, cb: p1, error: p2 });
            } else {
                this.api({ url, params: p1, cb: p2, error: p3 });
            }
        },

        api(args) {
            args = args || {};
            var method = args.method || "GET";
            var cb = args.cb || (() => {});
            var error = args.error || (() => {});
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
                url,
                data,
                type: method,
                contentType: "application/json",
                dataType,
                context: this,
                success(data) { cb(data); },
                error(e) { log("API error: " + e); error(); }
            });
        },

        getList(url, options) {
            return new GetListRequest(this, url, options);
        }
    });

    window.LV = new LV();
    window.LV.Utils = {
        isoDate
    };
}))();
