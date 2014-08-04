//ysf: support functions to debug and inspect code

var support = {
    _debug: function(value, msg) {
        console.log({
            message: msg,
            value: value
        });
    }
};

//ysf: refactored for closure compiler
app.controller(
    'HeaderCtrl', ['$scope', '$timeout',
        function($scope, $timeout) {
            var setClock = function() {
                $scope.date = new Date();
                //support._debug($scope.date, 'current date');
                $timeout(setClock, 1000);
            };

            $scope.name = 'Yousuf Jawwad';
            setClock();
        }
    ]);


app.controller(
    'AddLeadDialogCtrl', ['$scope', 'dialog', 'dialogsModel', 'Customer', 'Lead', 'LeadProperty', '$filter',
        function($scope, dialog, dialogsModel, Customer, Lead, LeadProperty, $filter) {
            $scope.properties = dialogsModel.properties;
            /*$scope.properties = Property.get(function (success) {
             support._debug($scope.properties.results);
             $scope.properties = $scope.properties.results;
             support._debug($scope.properties);
             });*/

            //$scope.properties = Property.query();

            $scope.lead_properties = [{
                property: null,
                cost: null
            }];

            $scope.addPropertyToLead = function() {
                var single = {
                    property: null,
                    cost: null
                };
                $scope.lead_properties.push(single);
            };

            //adding select2 options for property list
            $scope.propertyListOptions = {};

            //adding date options
            $scope.dateOptions = {
                'starting-day': 1
            };

            //close the dialog without saving
            $scope.close = function() {
                dialog.close();
            };

            $scope.save = function() {
                var customer = new Customer($scope.customer);
                support._debug(customer, 'customer after initialization');
                customer.$save(function(success) {
                    //support._debug(customer, 'saved successfully');
                    support._debug($scope.lead, 'the complete lead before saving');
                    support._debug($scope.lead.properties, 'selected properties');
                    //the problem: i am getting an empty string aswell .. also the width problem

                    //ysf: new lead to save and instanciating it with form data
                    var lead = new Lead($scope.lead);
                    support._debug(customer.id, 'the customer id');
                    lead.customer = customer.id;
                    //setting the correct date format on arrival and departure
                    lead.arrival = $filter('date')(lead.arrival, 'yyyy-MM-dd');
                    lead.departure = $filter('date')(lead.departure, 'yyyy-MM-dd');
                    // if lead is saved, push the lead
                    lead.$save(function(success) {
                        //dialog.close();
                        support._debug(lead, 'Stored Lead');
                        angular.forEach($scope.lead_properties, function(property) {
                            support._debug(property, 'the associated property ');
                            lead_property = new LeadProperty(property);
                            lead_property.lead = lead.id;
                            lead_property.available_from = lead.arrival;
                            lead_property.available_to = lead.departure;
                            lead_property.status = 'RQ';
                            lead_property.$save(function(success) {

                            }, function(error) {
                                support._debug(error, 'the error while saving lead property');
                            })
                        });
                        //what if i want to update the scope results after the dialog is closed?
                        //ysf: resarch on it!
                    }, function(error) {
                        support._debug(error, 'error when saving lead');
                    });
                }, function(error) {
                    support._debug(error, 'customer not saved')
                })
            }
        }
    ]);

app.controller(
    'EditLeadDialogCtrl', ['$scope', 'dialog', 'dialogsModel', 'Lead', 'Template', '$http',
        function($scope, dialog, dialogsModel, Lead, Template, $http) {
            lead = dialogsModel.lead;
            support._debug(lead, 'The inherited lead');
            if (!lead.first_response) {
                var template = Template.first_response({
                    lead: lead.id
                }, function(success) {
                    $scope.response = template.first_response;
                });
            } else if (!lead.second_response) {
                support._debug('2nd', '2nd');
                var template = Template.second_response({
                    lead: lead.id
                });
                $scope.response = template.second_response;
            };
            $scope.saveMessage = function() {
                support._debug('save message', 'save message');
                $http.post(lead.reply_message_url, {
                    message: $scope.response
                }).success(function(data) {
                    support._debug(data, 'data')
                }).error(function(data) {
                    support._debug(data, 'error')
                });
            }
        }
    ]);


app.controller(
    'HomeCtrl', ['$scope', 'Lead', 'Property', '$dialog',
        function($scope, Lead, Property, $dialog) {
            //$scope.text = 'I should display this when called';
            //support._debug($scope.text, 'initializing the view');

            //query all the leads for display
            $scope.leads = Lead.query();
            support._debug($scope.leads, 'testing lead format');

            //get all the properties
            $scope.properties = Property.query();
            support._debug($scope.properties, 'properties');
            /*$scope.properties = Property.get(function (success) {
                //support._debug($scope.properties.results);
                $scope.properties = $scope.properties.results;
                //support._debug($scope.properties);
            });*/
            //ysf: setting the Lead dialog box properties
            //ysf: fetching the properties in the main window,
            //     to optimize the performance.
            var addLeadDialogOptions = {
                backdrop: true,
                keyboard: true,
                dialogFade: true,
                backdropClick: false,
                templateUrl: '/partials/dialogs/add_lead.html',
                controller: 'AddLeadDialogCtrl',
                resolve: {
                    dialogsModel: function() {
                        return {
                            properties: $scope.properties
                        }
                    }
                }
            };

            //ysf: dialog box to perform actions on leads
            var EditLeadDialogOptions = {
                backdrop: true,
                keyboard: true,
                dialogFade: true,
                backdropClick: false,
                templateUrl: '/partials/dialogs/edit_lead.html',
                controller: 'EditLeadDialogCtrl'
            };

            //open the add lead dialog box on click
            $scope.openAddLeadDialog = function() {
                var d = $dialog.dialog(addLeadDialogOptions);
                d.open();
            };

            $scope.openEditLeadDialog = function(options) {
                EditLeadDialogOptions.resolve = {
                    dialogsModel: function() {
                        return {
                            lead: options
                        }
                    }
                };
                var d = $dialog.dialog(EditLeadDialogOptions);
                d.open();
            }
        }
    ]);