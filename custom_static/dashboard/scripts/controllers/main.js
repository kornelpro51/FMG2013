app.controller(
    'MainCtrl', ["$scope", "$rootScope", 'LeadStorage', 'Lead',
        function ($scope, $rootScope, LeadStorage, Lead) {
            $scope.wizardSteps = [1,0,0,0,0];
            $scope.nextStep = function(step) {
                $scope.wizardSteps = [0,0,0,0,0];
                $scope.wizardStep[step+1] = 1;
            };
            $scope.previousStep = function(step) {
                $scope.wizardSteps = [0,0,0,0,0];
                $scope.wizardStep[step-1] = 1;
            };
            $scope.goToStep = function(step) {
                $scope.wizardSteps = [0,0,0,0,0];
                $scope.wizaardSteps[step];
            };
            var all = LeadStorage.getAll();
            console.log(all);
            var leads = Lead.get(function(success) {
                leads = leads.results;
                console.log(leads);
                LeadStorage.store(leads);
                console.log(LeadStorage.getAll());
            });
        }
    ]);
