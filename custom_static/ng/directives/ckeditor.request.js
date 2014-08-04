angular.module('ngCkeditor', []).directive('ckEditor', function() {
    return {
        require: '^ngModel',
        scope: {
            ngModel: "=",
            options: "="
        },
        controller: ['$scope', 'Template',
            function($scope, Template) {
                $scope.template = null;
                $scope.resolvedResponse = null;
                $scope.getTemplate = function(lead, responseType) {
                    //console.log(lead);
                    //console.log(responseType);
                    if (responseType == 'first') {
                        $scope.template = Template.first_response({
                            lead: lead
                        }, function() {
                            $scope.resolvedResponse = $scope.template.first_response;
                        });
                    } else if (responseType == 'second') {
                        $scope.template = Template.second_response({
                            lead: lead
                        }, function() {
                            $scope.resolvedResponse = $scope.template.second_response;
                        });
                    } else if (responseType == 'offer') {
                        $scope.template = Template.offer_response({
                            lead: lead
                        }, function() {
                            $scope.resolvedResponse = $scope.template.offer_response;
                        });
                    } else {
                        $scope.template = Template.default_response({
                            lead: lead
                        }, function() {
                            $scope.resolvedResponse = $scope.template.default_response;
                        });
                    }
                }
            }
        ],
        link: function(scope, elm, attr, ngModel) {
            var ck = CKEDITOR.replace(elm[0]);
            ck.config.startupFocus = true;
            ck.config.fullPage = true;

            if (!ngModel) return;

            ck.on('instanceReady', function() {
                ck.setData(ngModel.$viewValue);
                ck.focus();
            });

            function updateModel() {
                scope.$apply(function() {
                    setTimeout(function() {
                        console.log(ck.getData());
                        ngModel.$setViewValue(ck.getData());
                    }, 200)
                });
            }

            //ck.on('change', updateModel);
            ck.on('key', updateModel);
            //ck.on('dataReady', updateModel);

            //console.log(attr);

            var leadId = null;
            var responseType = null;

            scope.$watch('options', function(o) {
                if (o) {
                    scope.getTemplate(o.leadID, o.responseType);
                }
            });

            scope.$watch('resolvedResponse', function(r) {
                //console.log(r);
                ngModel.$setViewValue(r);
                ck.setData(ngModel.$viewValue);
                ck.focus();
                //console.log(ngModel);
            });

            /*scope.$watch('$scope.resolvedResponse', function(r) {
                if (r) {
                    //console.log(r);
                    //ngModel.$viewValue = r;
                    console.log(r);
                    ngModel.$setViewValue(r);
                    //ngModel.$setModelValue(r);
                    console.log(ngModel);
                    ck.setData(ngModel.$viewValue);
                }
            })*/

            //ngModel.$render = setEditor();
        }
    };
});