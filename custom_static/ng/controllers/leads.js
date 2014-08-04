app.controller(
  'AddLeadCtrl', ['$scope', '$filter', '$location', 'Customer', 'Lead', 'Property', 'LeadProperty', 'Note', 'toaster', '$rootScope',
    function($scope, $filter, $location, Customer, Lead, Property, LeadProperty, Note, toaster, $rootScope) {

      $scope.lead_properties = [{
        property: null,
        rate: null
      }];

      $scope.note = {};

      //if multiple properties are added, this variable is used.
      var order = 0;

      $scope.addPropertyToLead = function() {
        var single = {
          property: null,
          rate: null
        };
        $scope.lead_properties.push(single);
      };

      $scope.saveLead = function() {
        var customer = new Customer($scope.customer);

        if (customer.email === '' || !customer.email) {
          customer.email = '';
        }

        if (!customer.last_name) {
          customer.last_name = "";
        }

        customer.$save(function(success) {
          var lead = new Lead($scope.lead);
          //if lead.source is null .. add lead.source to other
          if (!lead.source) {
            lead.source = 'Other';
          }
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
              lead_property.order = order;
              lead_property.$save(function(success) {
                //$location.path('/');
                //the above line is wrong .. it would exit after the first item
              }, function(error) {});
              order += 1;
            });

            if (!$scope.note.content || $scope.note.content !== null) {
              var note = new Note($scope.note);
              note.lead = lead.id;
              //save the note and redirect
              note.$save(function(success) {
                $location.path('/lead/' + lead.id + '/response/first');
                toaster.pop('success', 'Success', 'New lead Saved Succesfully');
              });
            }
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
  'EditLeadPropertiesCtrl', ['$q', '$scope', '$location', '$http', '$routeParams', '$filter', 'toaster', 'Note', 'Lead', 'LeadProperty', 'Property', 'Customer', 'Message', 'socket',
    function($q, $scope, $location, $http, $routeParams, $filter, toaster, Note, Lead, LeadProperty, Property, Customer, Message, socket) {
      var promises = [];
      var order = 0;

      var lead = Lead.get({
        id: $routeParams.leadID
      }, function() {
        var leadProperties = lead.lead_properties;
        //console.log(leadProperties);
        leadProperties.forEach(function(key) {
          if (key.order >= order) {
            order = key.order + 1;
          }
          //console.log(order);
        });

        //console.log(leadProperties);
        $scope.requestedProperties = $filter('requestedProperties')(leadProperties);
        $scope.lead_properties = [{
          property: null,
          rate: 0,
          available_from: lead.arrival,
          available_to: lead.departure,
          order: order
        }];
        $scope.lead = lead;
        //console.log($scope.requestedProperties.length);
        Message.get({
          lead_id: lead.id
        }, function(data) {
          //console.log(data);
          $scope.lead.messages = data.results;
        });

        Note.get({
          lead_id: lead.id
        }, function(data) {
          //console.log(data.results);
          $scope.lead.notes = data.results;
        });
      });

      $scope.showCustomer = true;

      $scope.editCustomer = function() {
        $scope.showCustomer = !$scope.showCustomer;
      };

      $scope.saveCustomer = function() {
        var customer = Customer.update($scope.lead.customer_serial);
        $scope.showCustomer = !$scope.showCustomer;
      };

      $scope.note = null;
      $scope.propertyNotAvailable = false;


      $scope.addPropertyToLead = function() {
        order = order + 1;
        var single = {
          property: null,
          rate: 0,
          available_from: lead.arrival,
          available_to: lead.departure,
          order: order
        };
        $scope.lead_properties.push(single);
      };

      var updateLead = function() {
        if ($scope.propertyNotAvailable) {
          angular.forEach(lead.lead_properties, function(p) {
            if (p.status == 'RQ' || p.status == 'PR') {
              if (!p.keep) {
                p.status = 'NA';
              }
              promises.push($http.put(p.url, p));
            }
          });
          angular.forEach($scope.lead_properties, function(property) {
            var lead_property = new LeadProperty(property);
            lead_property.lead = lead.id;
            lead_property.available_from = $filter('date')(property.available_from, 'yyyy-MM-dd');
            lead_property.available_to = $filter('date')(property.available_to, 'yyyy-MM-dd');
            lead_property.status = 'PR';
            promises.push(lead_property.$save().$promise);
          });
        } else {
          angular.forEach($scope.lead.lead_properties, function(p) {
            p.available_from = $filter('date')(p.available_from, 'yyyy-MM-dd');
            p.available_to = $filter('date')(p.available_to, 'yyyy-MM-dd');
            promises.push($http.put(p.url, p));
          });
        }
        promises.push(Lead.update(lead).$promise);
        toaster.pop('info', 
          'Updating Lead Information', 
          'Saving updated property information and preparing the response template accordingly.'
          );
      };

      $scope.addNote = function(text, lead) {
        var note = new Note({
          lead: lead.id,
          content: text
        });
        note.$save(function() {
          $scope.note = '';
          $scope.lead.notes.push(note);
        });
      };

      $scope.formatMessage = function(message) {
        return message.replace(/\u000D/g, '<br>');
      };

      $scope.redirectToHome = function() {
        $location.path('/');
      };

      $scope.saveAndContinue = function() {
        updateLead();
        $q.all(promises).then(function() {
          $location.path('/lead/' + lead.id + '/response/first/');
        });
      };

      $scope.sendOffer = function(lead) {
        updateLead();
        $q.all(promises).then(function() {
          $location.path('/lead/' + lead.id + '/response/offer/');
        });
      };

      $scope.sendAutoResponse = function(lead) {
        updateLead();
        $q.all(promises).then(function() {
          $location.path('/lead/' + lead.id + '/response/second/');
        });
      };

      $scope.sendEmail = function(lead) {
        updateLead();
        $q.all(promises).then(function() {
          $location.path('/lead/' + lead.id + '/response/email/');
        });
      };

      $scope.toggleBooking = function(lead) {
        if (!lead.booked) {
          lead.booked = !lead.booked;
          Lead.update(lead);
        }
      };
    }
  ]);

app.controller(
  'EditLeadResponseCtrl', ['$scope', "$rootScope", '$location', '$http', '$routeParams', 'toaster', 'Customer', 'Lead', 'Property', 'LeadProperty', 'Template', 'Message', 'socket',
    function($scope, $rootScope, $location, $http, $routeParams, toaster, Customer, Lead, Property, LeadProperty, Template, Message, socket) {

      $scope.options = {
        leadID: $routeParams.leadID,
        responseType: $routeParams.responseType
      };

      $scope.lead = Lead.get({
        id: $routeParams.leadID
      }, function(success) {
        Message.get({
          lead_id: $scope.lead.id
        }, function(data) {
          $scope.lead.messages = data.results;
          if ($scope.lead.messages.length) {
            $scope.subject = $scope.lead.messages[0].subject;
          } else {
            $scope.subject = "";
          }
        });
      });

      $scope.showFwd = true;
      $scope.showCC = true;
      $scope.fwd = null;
      $scope.cc = null;

      $scope.templateLoaded = false;

      $scope.saveMessage = function() {
        $http.post($scope.lead.reply_message_url, {
          fwd: $scope.fwd,
          cc: $scope.cc,
          message: $scope.response,
          subject: $scope.subject
        }).success(function(data) {
          //set the green bone to always be true when the lead is replied
          $scope.lead.first_response = true;
          if ($routeParams.responseType == 'second') {
            $scope.lead.second_response = true;
          } else if ($routeParams.responseType == 'offer') {
            $scope.lead.offer = true;
          }
          //console.log($rootScope.alerts);
          angular.forEach($rootScope.alerts, function(alert, idx) {
            if (alert.object && alert.object.id) {
              if ($scope.lead.id === alert.object.id) {
                console.log(alert.id);
                socket.emit('viewed', alert.id);
              }
            }
          });
          //console.log(data);
          Lead.update($scope.lead);
          toaster.pop('success', 'Success', 'Updated information has been sent to the client!');
          $scope.redirectToHome();
        }).error(function() {
          toaster.pop('error',
            'Click Send Message Again',
            'There was an problem in communicating with the email server, Please try again');
        });
      };
      $scope.editLead = function(lead) {
        $location.path('/lead/' + lead.id + '/properties/edit/');
        destroyCKEditor();
      };

      $scope.redirectToHome = function() {
        $location.path('/');
        destroyCKEditor();
      };

      var destroyCKEditor = function() {
        for (var name in CKEDITOR.instances) {
          CKEDITOR.instances[name].destroy();
        }
      };
    }
  ]);