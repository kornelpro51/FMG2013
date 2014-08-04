angular.module('ngCkeditor', []).directive('ckEditor', function () {
    return {
        require: '?ngModel',
        scope: {
            value: '=loaded'
        }
        link: function (scope, elm, attr, ngModel) {
            var ck = CKEDITOR.replace(elm[0]);

            //ck.config.fullPage = true;
            ck.config.startupFocus = true;
            //ck.config.height = '400px';
            //ck.config.extraAllowedContent = '*{*}';

            if (!ngModel) return;

            ck.on('instanceReady', function () {
                ck.setData(ngModel.$viewValue);
                ck.focus();
            });

            function updateModel() {
                scope.$apply(function () {
                    ngModel.$setViewValue(ck.getData());
                });
            }

            ck.on('change', updateModel);
            ck.on('key', updateModel);
            ck.on('dataReady', updateModel);

            console.log(ngModel);
            //console.log(ngModel.$viewValue);

            var setEditor = function () {
                //console.log(ngModel.$viewValue);
                if(ngModel.$viewValue) {
                    ck.setData(ngModel.$viewValue);
                    return
                } else {
                    console.log(ngModel);
                    setTimeout(setEditor(), 1000);
                }
            };

            /*ngModel.$render = function () {
                if(ngModel.$viewValue) {
                    ck.setData(ngModel.$viewValue);
                } else {
                    setTimeout(function() {
                        ck.setData(ngModel.$viewValue);
                    }, 500);
                }
            };*/

            ngModel.$render = setEditor();
        }
    };
});
