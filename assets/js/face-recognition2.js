/**
 * Created by Affan on 20/08/2017.
 */
(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['tracking', 'jquery'], function (tracking, jquery) {
            return (root.facerecognition = factory(tracking, jquery));
        });
    } else if (typeof module === 'object' && module.exports) {
        var jQuery = (typeof window != 'undefined') ? window.jQuery : undefined;
        if (!jQuery) {
            jQuery = require('jquery');
            if (!jQuery.fn) jQuery.fn = {};
        }
        module.exports = factory(require('tracking'), jQuery);
    } else {
        root.facerecognition = factory(root.tracking, root.jQuery);
    }
}(this, function (tracking, $) {
    var FaceRecognition = function (opts) {
        this.dataTraining = new Array(5);
        this.video = document.getElementById(opts.videoEl.replace('#', '')) || document.getElementById('video');
        this.videoEl = opts.videoEl || '#video';
        this.canvas = document.getElementById(opts.canvasEl.replace('#', '')) || document.getElementById('canvas');
        this.context = this.canvas.getContext('2d');
        this.tracker = new tracking.ObjectTracker('face');
        this.tracker.setInitialScale(4);
        this.tracker.setStepSize(2);
        this.tracker.setEdgesDensity(0.1);
        this.counter = 0;
        this.capture = false;
        this.dimen = {};
        this.dimen.width = 50;
        this.dimen.height = 50;
        this.i = 0;
        this.curRect = {
            x: 0,
            y: 0,
            width: 0,
            height: 0
        }
        if (opts.dimen && typeof opts.dimen === 'object') {
            this.dimen.width = opts.dimen.width;
            this.dimen.height = opts.dimen.height;
        }
        this.captureCallback = function () {
        };
        if (typeof opts.captureCallback === 'function')
            this.captureCallback = opts.captureCallback;
        this.tracker.on('track', $.proxy(this.onTrack, this));
    };

    FaceRecognition.prototype = {
        constructor: FaceRecognition,
        normalize: function (canvas) {
            var c = document.createElement('canvas');
            var ctx = c.getContext('2d');
            c.height = this.dimen.height;
            c.width = this.dimen.width;
            ctx.drawImage(canvas, 0, 0, this.dimen.width, this.dimen.height);
            return c;
        },
        isMoved: function (rect1, rect2, threshold) {
            console.log('rect1');
            console.log(rect1);
            console.log('rect2');
            console.log(rect2);
            var deltaX = Math.abs(rect1.x - rect2.x);
            var deltaY = Math.abs(rect1.y - rect2.y);
            var deltaWidth = Math.abs(rect1.width - rect2.width);
            var deltaHeight = Math.abs(rect1.height - rect2.height);
            console.log('deltaX :' + deltaX);
            console.log('deltaY :' + deltaY);
            if (deltaX > threshold || deltaY > threshold || deltaHeight > threshold || deltaWidth > threshold)
                return true;
            return false;
        },
        grayscale: function (canvas) {
            var c = document.createElement('canvas');
            var ctx = c.getContext('2d');
            c.height = canvas.height;
            c.width = canvas.width;
            ctx.drawImage(canvas, 0, 0, c.width, c.height);
            var data = ctx.getImageData(0, 0, c.width, c.height);
            var gray1 = tracking.Image.grayscale(data.data, c.width, c.height);
            var imgData = ctx.createImageData(c.width, c.height);
            var ctr = 0;
            for (var i = 0; i < data.data.length; i += 4) {
                imgData.data[i] = gray1[ctr];
                imgData.data[i + 1] = gray1[ctr];
                imgData.data[i + 2] = gray1[ctr];
                imgData.data[i + 3] = 255;
                ctr++;
            }
            ctx.putImageData(imgData, 0, 0);
            return c;
        },
        captureVideo: function (rect) {
            console.log('capture');
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
            this.captureCallback(this.counter, this.grayscale(this.normalize(canvas2)).toDataURL());
            this.dataTraining[this.counter] = this.grayscale(this.normalize(canvas2)).getContext('2d').getImageData(0, 0, this.dimen.width, this.dimen.height).data;
            this.counter = (++this.counter % 5);
        },
        onTrack: function (event) {
            var $this = this;
            this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
            event.data.forEach(function (rect) {
                $this.context.strokeStyle = '#a64ceb';
                $this.context.strokeRect(rect.x, rect.y, rect.width, rect.height);
                $this.context.font = '11px Helvetica';
                $this.context.fillStyle = "#fff";
                $this.context.fillText('Wajah terdeteksi', rect.x + (rect.width / 2) - 30, rect.y + 11);
                var isMoved = $this.isMoved($this.curRect, rect, 5);
                console.log(isMoved);
                if (!isMoved)
                    $this.captureVideo(rect);
                $this.curRect = rect;
            });
        },
        startTracking: function () {
            tracking.track(this.videoEl, this.tracker, {camera: true});
        },
        stopTracking: function () {
            $(this.videoEl)[0].srcObject = null;
            this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
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