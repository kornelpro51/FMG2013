app.directive('notification', function ($timeout) {
    return {
        restrict: 'E',
        replace: true,
        scope: {
            ngModel: '='
        },
        template: '<div class="note note-success" bs-alert="ngModel"><button type="button" class="close">×</button>text</div>',
        link: function (scope, element, attrs) {
            $timeout(function () {
                element.empty();
                element.hide();
            }, 5000);
        }
    }
});