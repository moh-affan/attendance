/**
 * Created by Affan on 16/08/2017.
 */
(function (root, factory) {
    if (typeof define === "function" && define.amd) {
        define(["jquery"], factory);
    } else if (typeof exports === 'object') {
        factory(require('jquery'));
    } else {
        factory(jQuery);
    }
})(this, function ($, undefined) {
    var DropDown = function (elem, data, cb) {
        this.elem = $(elem);
        this.callback = function () {
        };
        if (typeof data !== 'object' || data === null)
            data = [{name: '--Pilih--', value: ''}];
        this.data = $.merge([{name: '--Pilih--', value: ''}], data);
        if (typeof cb === 'function') {
            this.callback = cb;
        }
        this.elem.on({
            'change': $.proxy(this.change, this)
        });
    };
    DropDown.prototype = {
        constructor: DropDown,
        render: function () {
            var html = '';
            $.each(this.data, function (i, item) {
                html += '<option value="' + item.value + '">';
                html += item.name;
                html += '</option>';
            });
            this.elem.html(html);
        },
        change: function (a) {
            this.callback(this.elem.find('option:selected').text(), this.elem.val());
        }
    };

    $.fn.dropdown = function (data, cb) {
        this.each(function () {
            var el = $(this);
            var dt = new DropDown(el, data, cb);
            el.data('dropdown', dt);
            dt.render();
        });
        return this;
    };
    return DropDown;
});