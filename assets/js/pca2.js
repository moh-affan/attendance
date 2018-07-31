/**
 * Created by Affan on 20/08/2017.
 */

(function (window, undefined) {
    window.pca = window.pca || {};

}(window));

(function () {

    pca.Matrix = {};
    pca.Matrix.pixelToMatrix = function (pixels, width, height) {
        var temp = new Array(height);
        var i = height;
        var c = 0;
        while (i--) {
            temp[i] = new Array(width);
            var j = width;
            while (j--) temp[i][j] = pixels[c++];
        }
        return temp;
    };
    pca.Matrix.matrixToPixel = function (matrix, width, height) {
        var temp = new Uint8ClampedArray(width * height);
        var i = height;
        var c = 0;
        while (i--) {
            var j = width;
            while (j--) temp[c++] = matrix[i][j];
        }
        return temp;
    };
    pca.Matrix.mean = function (trainingSet) {
        var Mt = trainingSet.length;
        var N = trainingSet[0].length;
        var mean = new Uint8Array(N);
        for (var i = 0; i < Mt; i++) {
            for (var j = 0; j < N; j++) {
                if (mean[j] == undefined)
                    mean[j] = 0;
                else
                    mean[j] += trainingSet[i][j] / Mt;
            }
        }
        return mean;
    };

    pca.Matrix.calcCovarMatrix = function (trainingSet) {
        var mean = this.mean(trainingSet);
        var Mt = trainingSet.length;
        var N = mean.length;
        var diff = new Array(Mt);
        for (var i = 0; i < Mt; i++) {
            diff[i] = new Uint8Array(N);
            for (var j = 0; j < N; j++) {
                diff[i][j] = trainingSet[i][j] - mean[j];
            }
        }

        for (var i = 0; i < Mt; i++) {
            var eigenvector = new jsfeat.matrix_t(100, 100, jsfeat.U8_t | jsfeat.C1_t);
            jsfeat.linalg.eigenVV(diff[i], eigenvector);
            console.log(eigenvector)
        }
    };

    pca.Matrix.eigenValue = function () {

    };
    pca.Matrix.eigenVector = function () {
        var mean = this.mean(trainingSet);
        var Mt = trainingSet.length;
        var N = mean.length;

    };
    pca.Matrix.calculateEigenFace = function () {

    };

}());

(function () {

    pca.Vector = {};
    pca.Vector.pixelToVector = function (pixels, width, height) {
        var i = height * width;
        var temp = new Array(i);
        var c = 0;
        while (i--) {
            var j = 1;
            temp[i] = new Array(j);
            while (j--) temp[i][j] = pixels[c++];
        }
        return temp;
    };
    pca.Matrix.vectorToPixel = function (matrix, width, height) {
        var temp = new Uint8ClampedArray(width * height);
        var i = height * width;
        var c = 0;
        while (i--) {
            var j = 1;
            while (j--) temp[c++] = matrix[i][j];
        }
        return temp;
    };

}());

(function () {
    pca.Image = {};

    pca.Image.pixelsToCanvas = function (pixels, width, height, fillRGB, isTransparent) {
        var c = document.createElement('canvas');
        var ctx = c.getContext('2d');
        c.height = height;
        c.width = width;
        var p = 0;
        var imgData = ctx.createImageData(c.width, c.height);
        for (var i = 0; i < imgData.data.length; i += 4) {
            imgData.data[i] = pixels[p];
            imgData.data[i + 1] = fillRGB ? pixels[p + 1] : pixels[p];
            imgData.data[i + 2] = fillRGB ? pixels[p + 2] : pixels[p];
            imgData.data[i + 3] = isTransparent ? pixels[p + 3] : 255;
            if (fillRGB)
                p = i;
            else
                p++;
        }
        ctx.putImageData(imgData, 0, 0);
        return c;
    };

    pca.Image.normalize = function (canvas, height, width) {
        var c = document.createElement('canvas');
        var ctx = c.getContext('2d');
        c.height = height;
        c.width = width;
        ctx.drawImage(canvas, 0, 0, width, height);
        return c;
    };
}());