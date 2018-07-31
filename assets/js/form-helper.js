/**
 * Created by Affan on 17/08/2017.
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
    var FormHelper = function (form, url, options) {
        this._form = $(form);
        this._url = url;
        if (typeof options !== 'object' || options === null)
            options = {};
        if (typeof options.button === 'string')
            this.button = $(options.button);
        if (typeof options.modal === 'string')
            this.modal = $(options.modal);
        if (typeof options.dataTable === 'object')
            this.dataTable = options.dataTable;
        if (typeof options.msgSuccess === 'string')
            this.msgSuccess = options.msgSuccess;
        if (typeof options.msgFail === 'string')
            this.msgFail = options.msgFail;
        if (typeof options.alertClass === 'string')
            this.alertClass = options.alertClass;
        if (typeof options.done === 'function') {
            this.done = $.fn.extend(this.done, options.done);
        }
        if (typeof options.fail === 'function') {
            this.fail = $.fn.extend(this.fail, options.fail);
        }
        this.button.on({
            'click': $.proxy(this.submit, this)
        });
        this._form.on({
            'submit': $.proxy(this.submit, this)
        });
    };
    FormHelper.prototype = {
        constructor: FormHelper,
        submit: function () {
            var $this = this;
            $.post(this._url, this._form.serialize())
                .done(function () {
                    $.proxy($this.done(), $this)
                })
                .fail(function (r) {
                    $.proxy($this.fail(r.responseJSON), $this)
                });
            return false;
        },
        done: function () {
            this._form.trigger("reset");
            this.dataTable.ajax.reload();
            $(this.modal).modal('hide');
            var div = $('<div></div>');
            div.addClass('alert alert-success alert-dismissable fade in');
            var icheck = $('<i></i>');
            icheck.addClass('fa fa-check');
            var btn = $('<button></button>');
            btn.addClass('close');
            btn.attr({
                'type': "button",
                'data-dismiss': "alert",
                'aria-hidden': true
            });
            div.append(icheck);
            div.append(btn);
            div.append('<b>Sukses!</b> ' + this.msgSuccess);
            $(this.alertClass).html(div);
            setTimeout(function () {
                $('body').find('button[data-dismiss="alert"]').trigger("click");
            }, 4000);
        },
        fail: function (rJSON) {
            var $this = this;
            $.map(rJSON, function (a, b) {
                var el = $this._form.find('#' + b);
                var par = el.parents('.form-group');
                par.addClass('has-error');
                var spn = $('<span></span>');
                spn.addClass('help-block');
                $.map(a, function (c) {
                    spn.html('<i>' + c + '</i>');
                });
                par.find('span').remove();
                if ($.contains(par, spn))
                    par.remove(spn);
                par.append(spn);
            });
        }
    };

    $.fn.formhelper = function (url, options) {
        this.each(function () {
            var el = $(this);
            var dt = new FormHelper(el, url, options);
            el.data('formhelper', dt);
        });
        return this;
    };
    return FormHelper;
});