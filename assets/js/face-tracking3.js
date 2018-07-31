/**
 * Created by Affan on 20/08/2017.
 */
(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['tracking', 'pca', 'jsfeat', 'jquery'], function (tracking, pca, jquery) {
            return (root.facerecognition = factory(tracking, pca, jquery));
        });
    } else if (typeof module === 'object' && module.exports) {
        var jQuery = (typeof window != 'undefined') ? window.jQuery : undefined;
        if (!jQuery) {
            jQuery = require('jquery');
            if (!jQuery.fn) jQuery.fn = {};
        }
        module.exports = factory(require('tracking'), require('pca'), require('jsfeat'), jQuery);
    } else {
        root.facerecognition = factory(root.tracking, root.pca, root.jsfeat, root.jQuery);
    }
}(this, function (tracking, pca, jsfeat, $) {
    var FaceRecognition = function (opts) {
        this.video = document.getElementById(opts.videoEl.replace('#', '')) || document.getElementById('video');
        this.videoEl = opts.videoEl || '#video';
        this.canvas = document.getElementById(opts.canvasEl.replace('#', '')) || document.getElementById('canvas');
        this.context = this.canvas.getContext('2d');
        this.tracker = new tracking.ObjectTracker('face');
        this.tracker.setInitialScale(4);
        this.tracker.setStepSize(2);
        this.tracker.setEdgesDensity(0.1);
        this.wasCaptured = false;
        this.dimen = {};
        this.c = 0;
        this.dimen.width = 50;
        this.dimen.height = 50;
        this.zeroRect = {
            x: 0,
            y: 0,
            width: 0,
            height: 0
        };
        this.rect = this.zeroRect;
        if (opts.dimen && typeof opts.dimen === 'object') {
            this.dimen.width = opts.dimen.width;
            this.dimen.height = opts.dimen.height;
        }
        this.captureCallback = function () {
        };
        if (typeof opts.captureCallback === 'function')
            this.captureCallback = opts.captureCallback;
        this.centerBoxWidth = opts.centerBoxWidth || 100;
        this.centerBoxHeight = opts.centerBoxHeight || 100;
        this.centerRect = {
            x: this.video.width / 2 - (this.centerBoxWidth / 2),
            y: this.video.height / 2 - (this.centerBoxHeight / 2),
            width: this.centerBoxWidth,
            height: this.centerBoxHeight
        };
        var _vidParElem = video.parentNode;
        var _cnvs = document.createElement('canvas');
        _cnvs.width = video.width;
        _cnvs.height = video.height;
        var _ctx = _cnvs.getContext('2d');
        _ctx.strokeStyle = '#eb1612';
        _ctx.strokeWidth = 2;
        _ctx.strokeRect(this.centerRect.x, this.centerRect.y, this.centerBoxWidth, this.centerBoxHeight);
        _vidParElem.appendChild(_cnvs);
        this.tracker.on('track', $.proxy(this.onTrack, this));
    };

    FaceRecognition.prototype = {
        constructor: FaceRecognition,
        isWithinCaptureBox: function (rect) {
            var isXInbound = rect.x >= this.centerRect.x && (rect.x + rect.width) <= (this.centerRect.x + this.centerRect.width);
            var isYInbound = rect.y >= this.centerRect.y && (rect.y + rect.height) <= (this.centerRect.y + this.centerRect.height);
            return isXInbound && isYInbound;
        },
        captureVideo: function (rect) {
            var canvas = document.createElement('canvas');
            var canvas2 = document.createElement('canvas');
            var context = canvas.getContext('2d');
            var context2 = canvas2.getContext('2d');
            canvas.width = this.video.offsetWidth;
            canvas.height = this.video.offsetHeight;
            canvas2.width = rect.width;
            canvas2.height = rect.height;
            context.drawImage(this.video, 0, 0, canvas.width, canvas.height);
            var imageData = context.getImageData(rect.x, rect.y, rect.width, rect.height);
            context2.putImageData(imageData, 0, 0);
            var normalized = pca.Image.normalize(canvas2, this.dimen.height, this.dimen.width);
            var equalized = tracking.Image.equalizeHist(normalized.getContext('2d').getImageData(0, 0, normalized.width, normalized.height).data, normalized.width, normalized.height);
            var grayscale = tracking.Image.grayscale(equalized, normalized.width, normalized.height, false);
            this.captureCallback(pca.Image.pixelsToCanvas(grayscale, normalized.width, normalized.height, false, false).toDataURL(), grayscale);
        },
        onTrack: function (event) {
            var $this = this;
            this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
            event.data.forEach(function (rect) {
                $this.context.strokeStyle = '#0110eb';
                $this.context.strokeRect(rect.x, rect.y, rect.width, rect.height);
                $this.context.font = '11px Helvetica';
                $this.context.fillStyle = "#fff";
                $this.context.fillText('Wajah terdeteksi', rect.x + (rect.width / 2) - 30, rect.y + 11);
                if ($this.isWithinCaptureBox(rect)) {
                    if (!$this.wasCaptured) {
                        $this.captureVideo(rect);
                        $this.wasCaptured = true;
                    }
                } else
                    $this.wasCaptured = false;
            });
        },
        startCamera: function () {
            this.trackerTask = tracking.track(this.videoEl, this.tracker, {camera: true});
        },
        stopCamera: function () {
            $(this.videoEl)[0].srcObject = null;
            this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        },
        startTracking: function () {
            if (typeof this.trackerTask === 'object' && typeof this.trackerTask.run() === 'function')
                this.trackerTask.run();
        },
        stopTracking: function () {
            if (typeof this.trackerTask === 'object' && typeof this.trackerTask.stop() === 'function')
                this.trackerTask.stop();
        }
    };
    $.fn.facetrack = function (opts) {
        var dt;
        this.each(function () {
            var el = $(this);
            dt = new FaceRecognition(opts);
            el.data('facerecognition', dt);
        });
        return dt;
    };
    return FaceRecognition;
}));