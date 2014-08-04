app.controller(
    'HomeCtrl', ['$scope', 'Global', 'Lead', 'Property', 'Note', '$dialog', '$location', '$log', '$anchorScroll',
        function($scope, Global, Lead, Property, Note, $dialog, $location, $log, $anchorScroll) {
            //$scope.text = 'I should display this when called';
            //support._debug($scope.text, 'initializing the view');

            //show hide lead information formation
            $scope.infoIsCollapsed = [];

            //notes input management against each lead
            $scope.notes = [];

            //managing pagination
            $scope.pages = [];
            $scope.activePage = null;

            $scope.searchCustomer = function(){
                $scope.leads = Lead.hot({
                    search: $scope.queryString
                });

            }

            $scope.getNext = function() {
                $scope.activePage += 1;
                $scope.leads = Lead.hot({
                    page: $scope.activePage
                });
                //$anchorScroll();
            };

            $scope.getPrevious = function() {
                $scope.activePage -= 1;
                $scope.leads = Lead.hot({
                    page: $scope.activePage
                });
                //$anchorScroll();
            }

            $scope.getPage = function(page) {
                $scope.activePage = page;
                $scope.leads = Lead.hot({
                    page: $scope.activePage
                });
                //$anchorScroll();
            };

            $scope.styleForNext = function() {
                if (!$scope.leads.next) {
                    return 'disabled';
                }
            }

            $scope.styleForPrevious = function() {
                if (!$scope.leads.previous) {
                    return 'disabled';
                }
            }

            $scope.styleForActive = function(page) {
                if ($scope.activePage === page) {
                    return 'active';
                }
            }
            //show/hide lead information function
            $scope.showHistory = function(key) {
                if ($scope.infoIsCollapsed[key]) {
                    $scope.infoIsCollapsed[key] = !$scope.infoIsCollapsed[key];
                } else {
                    for (var i = 0; i < $scope.infoIsCollapsed.length; i++) {
                        $scope.infoIsCollapsed[i] = false;
                    }
                    $scope.infoIsCollapsed[key] = !$scope.infoIsCollapsed[key];
                };
                //var lead = $scope.leads.results[key];
                //$log.log(lead.id);
                //$location.hash('lead' + lead.id);
                //$anchorScroll();
            };

            //query all the leads for display
            //$scope.user = Global.user;
            //$scope.leads = Lead.query();

            $scope.leads = Lead.get(function(success) {
                //$log.log($scope.leads);
                var pages = Math.ceil($scope.leads.count / $scope.leads.results.length);

                //setting the page array
                for (var i = 0; i < pages; i++) {
                    $scope.pages.push(i + 1);
                };
                //$log.log($scope.pages);

                $scope.activePage = 1;

                //setting the lead information collapse status
                for (var i = 0; i < $scope.leads.results.length; i++) {
                    $scope.infoIsCollapsed.push(false);
                    $scope.notes.push('');
                };
            });

            //add a note to a lead
            $scope.addNote = function(text, key, lead) {
                var note = new Note({
                    lead: lead.id,
                    content: text
                });
                note.$save(function() {
                    $scope.notes[key] = '';
                    lead.notes.push(note);
                })
            };

            $scope.formatMessage = function(message) {
                return message.replace(/\u000D/g, '<br>');
            }

            //get all the properties
            //$scope.properties = Property.query();
            //support._debug($scope.properties, 'properties');

            $scope.leadsLoaded = function() {
                return !$scope.leads.$resolved
            };

            //bone toggling functionality

            $scope.togglePhoneCall = function(lead) {
                lead.phone_call = !lead.phone_call;
                Lead.update(lead);
            };

            $scope.toggleFirst = function(lead) {
                lead.first_response = !lead.first_response;
                Lead.update(lead);
            };

            $scope.toggleSecond = function(lead) {
                lead.second_response = !lead.second_response;
                Lead.update(lead);
            };

            $scope.toggleOffer = function(lead) {
                lead.offer = !lead.offer;
                Lead.update(lead);
            };

            $scope.toggleHot = function(lead) {
                lead.hot = !lead.hot;
                Lead.update(lead);
            };

            $scope.toggleBooking = function(lead) {
                lead.booked = !lead.booked;
                Lead.update(lead);
            };

            //links feature
            $scope.addLead = function() {
                $location.path('/lead/add/')
            };

            $scope.editLead = function(lead) {
                $location.path('/lead/' + lead.id + '/properties/edit/');
            };

            $scope.sendOffer = function(lead) {
                $location.path('/lead/' + lead.id + '/response/offer/');
            };

            $scope.sendAutoResponse = function(lead) {
                $location.path('/lead/' + lead.id + '/response/second/');
            };

            $scope.sendEmail = function(lead) {
                $location.path('/lead/' + lead.id + '/response/email/');
            };
        }
    ]);

app.controller(
    'AddLeadCtrl', ['$scope', '$filter', '$location', 'Customer', 'Lead', 'Property', 'LeadProperty', 'Note',
        function($scope, $filter, $location, Customer, Lead, Property, LeadProperty, Note) {

            $scope.properties = Property.get();

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

            $scope.saveLead = function() {
                var customer = new Customer($scope.customer);
                customer.$save(function(success) {
                    var lead = new Lead($scope.lead);
                    lead.customer = customer.id;
                    //setting the correct date format on arrival and departure
                    lead.arrival = $filter('date')(lead.arrival, 'yyyy-MM-dd');
                    lead.departure = $filter('date')(lead.departure, 'yyyy-MM-dd');
                    // if lead is saved, push the lead properties
                    lead.$save(function(success) {
                        angular.forEach($scope.lead_properties, function(property) {
                            var lead_property = new LeadProperty(property);
                            lead_property.lead = lead.id;
                            lead_property.available_from = lead.arrival;
                            lead_property.available_to = lead.departure;
                            lead_property.status = 'RQ';
                            lead_property.$save(function(success) {
                                //$location.path('/');
                                //the above line is wrong .. it would exit after the first item
                            }, function(error) {});
                        });

                        var note = new Note($scope.note);
                        note.lead = lead.id;
                        //save the note and redirect
                        note.$save(function(success) {
                            $location.path('/');
                        });

                        //what if i want to update the scope results after the dialog is closed?
                        //ysf: research on it!
                    });
                });
            };

            $scope.dateOptions = {
                'starting-day': 1,
                'show-weeks': false
            };

            $scope.redirectToHome = function() {
                $location.path('/');
            };
        }
    ]);

app.controller(
    'EditLeadPropertiesCtrl', ['$scope', '$location', '$http', '$routeParams', '$filter', 'Note', 'Lead', 'LeadProperty', 'Property',
        function($scope, $location, $http, $routeParams, $filter, Note, Lead, LeadProperty, Property) {
            var lead = Lead.get({
                id: $routeParams.leadID
            });

            $scope.lead = lead;

            $scope.note = null
            $scope.propertyNotAvailable = false;
            $scope.properties = Property.get();

            $scope.lead_properties = [{
                property: null,
                rate: null
            }];

            $scope.addPropertyToLead = function() {
                var single = {
                    property: null,
                    rate: null
                };
                $scope.lead_properties.push(single);
            };

            var updateLead = function() {
                if ($scope.propertyNotAvailable) {
                    angular.forEach(lead.lead_properties, function(p) {
                        p.status = 'NA';
                        //console.log(p.url);
                        $http.put(p.url, p);
                        //LeadProperty.update(p);
                    });
                    angular.forEach($scope.lead_properties, function(property) {
                        var lead_property = new LeadProperty(property);
                        lead_property.lead = lead.id;
                        lead_property.available_from = $filter('date')(property.available_from, 'yyyy-MM-dd');
                        lead_property.available_to = $filter('date')(property.available_to, 'yyyy-MM-dd');
                        lead_property.status = 'PR';
                        lead_property.$save();
                    });
                } else {
                    angular.forEach($scope.lead.lead_properties, function(p) {
                        console.log(p);
                        p.available_from = $filter('date')(p.available_from, 'yyyy-MM-dd');
                        p.available_to = $filter('date')(p.available_to, 'yyyy-MM-dd');
                        $http.put(p.url, p);
                    });
                };

                Lead.update(lead);
            };

            $scope.addNote = function(text, lead) {
                var note = new Note({
                    lead: lead.id,
                    content: text
                });
                note.$save(function() {
                    $scope.note = '';
                    $scope.lead.notes.push(note);
                })
            };

            $scope.formatMessage = function(message) {
                return message.replace(/\u000D/g, '<br>');
            };

            $scope.redirectToHome = function() {
                $location.path('/');
            };

            $scope.saveAndContinue = function () {
                updateLead();
                $location.path('/lead/' + lead.id + '/response/first/');
            }

            $scope.sendOffer = function(lead) {
                updateLead();
                $location.path('/lead/' + lead.id + '/response/offer/');
            };

            $scope.sendAutoResponse = function(lead) {
                updateLead();
                $location.path('/lead/' + lead.id + '/response/second/');
            };

            $scope.sendEmail = function(lead) {
                updateLead();
                $location.path('/lead/' + lead.id + '/response/email/');
            };
        }
    ]);

app.controller(
    'EditLeadResponseCtrl', ['$scope', '$location', '$http', '$routeParams', 'Customer', 'Lead', 'Property', 'LeadProperty', 'Template',
        function($scope, $location, $http, $routeParams, Customer, Lead, Property, LeadProperty, Template) {
            /*var lead = Lead.get({
                id: $routeParams.leadID
            }, function () {
                if (!lead.first_response) {
                    var template = Template.first_response({
                        lead: lead.id
                    }, function (success) {
                        $scope.response = template.first_response;
                    });
                } else if (!lead.second_response) {
                    var template = Template.second_response({
                        lead: lead.id
                    });
                    $scope.response = template.second_response;
                }
            });*/

            $scope.tinyMCEoptions = {
                doctype : "<!DOCTYPE html>",
                menubar: false,
                inline_styles: true,
                verify_html : false
            }

            $scope.lead = Lead.get({
                id: $routeParams.leadID
            });

            $scope.response = null;
            var template = null;

            if ($routeParams.responseType == 'first') {
                template = Template.first_response({
                    lead: $routeParams.leadID
                }, function() {
                    $scope.response = template.first_response;
                });
            } else if ($routeParams.responseType == 'second') {
                template = Template.second_response({
                    lead: $routeParams.leadID
                }, function() {
                    $scope.response = template.second_response;
                });
            } else if ($routeParams.responseType == 'offer') {
                template = Template.offer_response({
                    lead: $routeParams.leadID
                }, function() {
                    $scope.response = template.offer_response;
                });
            }

            $scope.saveMessage = function() {
                $http.post($scope.lead.reply_message_url, {
                    message: $scope.response,
                    subject: $scope.subject
                }, function() {
                    if (!$routeParams.responseType == 'first') {
                        $scope.lead.first_response = true;
                    } else if ($routeParams.responseType == 'second') {
                        $scope.lead.second_response = true;
                    } else if ($routeParams.responseType == 'offer') {
                        $scope.lead.offer = true;
                    }

                    Lead.update($scope.lead);
                    $scope.redirectToHome();
                });
            };

            $scope.editLead = function(lead) {
                $location.path('/lead/' + lead.id + '/properties/edit/');
            };

            $scope.redirectToHome = function() {
                $location.path('/');
            };
        }
    ]);