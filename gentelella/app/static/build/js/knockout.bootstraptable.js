
ko.bindingHandlers.myBootstrapTable = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
        var oViewModel = valueAccessor();
        var $ele = $(element).bootstrapTable(oViewModel.params);
        oViewModel.bootstrapTable = function () {
            return $ele.bootstrapTable.apply($ele, arguments);
        }
    },
    update: function (element, valueAccessor, allBindingsAccessor, viewModel) {}
};

(function ($) {
    ko.bootstrapTableViewModel = function (options) {
        var that = this;

        this.default = {
            search: true,
            strictSearch: true,
            showColumns: true,
            cache:false,
            showRefresh: true,
            minimumCountColumns: 2,
            clickToSelect: true,
            showToggle: true,
        };
        this.params = $.extend({}, this.default, options || {});

        this.getSelections = function () {
            var arrRes = that.bootstrapTable("getSelections")
            return arrRes;
        };

        this.refresh = function () {
            that.bootstrapTable("refresh");
        };
    };
})(jQuery);