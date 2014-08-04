angular.module(
        'ysf.easyPieChart',
        []
    ).directive('easyPieChart', function () {
        return {
            restrict: 'C',
            scope: {
                options: '='
            },
            link: function (scope, elem, attrs) {
                //support._debug(elem[0], 'element value');
                //support._debug(scope.percent, 'scope value');
                //support._debug(this, 'this');
                $(elem[0]).easyPieChart();
            }
        }
    });
