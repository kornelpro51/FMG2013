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
        var cachebuster = parseInt(Math.random() * 100000);
        $scope.getTemplate = function(lead, responseType) {
          if (responseType == 'first') {
            $scope.template = Template.first_response({
              lead: lead,
              cachebuster: cachebuster
            }, function() {
              $scope.resolvedResponse = $scope.template.first_response;
              //console.log($scope.resolvedResponse);
            });
          } else if (responseType == 'second') {
            $scope.template = Template.second_response({
              lead: lead,
              r: r
            }, function() {
              $scope.resolvedResponse = $scope.template.second_response;
            });
          } else if (responseType == 'offer') {
            $scope.template = Template.offer_response({
              lead: lead,
              cachebuster: cachebuster
            }, function() {
              $scope.resolvedResponse = $scope.template.offer_response;
            });
          } else {
            $scope.template = Template.default_response({
              lead: lead,
              cachebuster: cachebuster
            }, function() {
              $scope.resolvedResponse = $scope.template.default_response;
            });
          }
        };
      }
    ],
    link: function(scope, elm, attr, ngModel) {

      var ck = CKEDITOR.replace(elm[0]);
      ck.config.startupFocus = true;
      ck.config.fullPage = true;

      if (!ngModel) return;

      //update model on key press
      function updateModel() {
        scope.$apply(function() {
          setTimeout(function() {
            console.log(ck.getData());
            ngModel.$setViewValue(ck.getData());
          }, 200);
        });
      }

      ck.on('key', updateModel);

      scope.$watch('options', function(o) {
        if (o) {
          scope.getTemplate(o.leadID, o.responseType);
        }
      });

      scope.$watch('resolvedResponse', function(r) {
        ngModel.$setViewValue(r);
        ck.setData(r, function() {
          ck.focus();
        });
      });
    }
  };
});