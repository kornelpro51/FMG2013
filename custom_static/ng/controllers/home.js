app.controller(
  'HomeCtrl', ['$scope', 'Lead', 'Property', 'Message', 'Note', 'socket', '$location', '$log',
    function($scope, Lead, Property, Message, Note, socket, $location, $log) {
      //$scope.text = 'I should display this when called';
      //support._debug($scope.text, 'initializing the view');

      socket.on('alert', function(alert) {
        if ($scope.leads.$resolved && !alert.alert) {
          $scope.leads.results.unshift(alert.object);
        }
      });

      //show hide lead information formation
      $scope.infoIsCollapsed = [];

      //notes input management against each lead
      $scope.notes = [];

      //set searchString to empty
      $scope.queryString = null;

      //managing pagination
      $scope.pages = [];
      $scope.activePage = null;

      $scope.searchLeads = function() {
        if ($scope.queryString.length > 1) {
          $scope.leads = Lead.search({
            search: $scope.queryString
          });
        } else if ($scope.queryString == null || $scope.queryString == '') {
          $scope.leads = Lead.get();
        }
      };

      $scope.searchCustomer = function() {
        $scope.leads = Lead.hot({
          search: $scope.queryString
        });

      };

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
      };

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
      };

      $scope.styleForPrevious = function() {
        if (!$scope.leads.previous) {
          return 'disabled';
        }
      };

      $scope.styleForActive = function(page) {
        if ($scope.activePage === page) {
          return 'active';
        }
      };
      //show/hide lead information function
      $scope.showHistory = function(key) {
        if ($scope.infoIsCollapsed[key]) {
          $scope.infoIsCollapsed[key] = !$scope.infoIsCollapsed[key];
        } else {
          for (var i = 0; i < $scope.infoIsCollapsed.length; i++) {
            $scope.infoIsCollapsed[i] = false;
          }
          //console.log($scope.leads.results[key]);
          $scope.infoIsCollapsed[key] = !$scope.infoIsCollapsed[key];
          if (!$scope.leads.results[key].messages) {
            var lead_id = $scope.leads.results[key].id;
            Message.get({
              lead_id: lead_id
            }, function(data) {
              //console.log(data.results);
              if (data.results.length) {
                $scope.leads.results[key].messages = data.results;
              } else {
                $scope.leads.results[key].messages = true;
              }
            });
            Note.get({
              lead_id: lead_id
            }, function(data) {
              $scope.leads.results[key].notes = data.results;
            });
          }
        }
        //var lead = $scope.leads.results[key];
        //$log.log(lead.id);
        //$location.hash('lead' + lead.id);
        //$anchorScroll();
      };

      //get percentage

      $scope.getPercent = function(a, b) {
        return (a / b) * 100;
      }

      //query all the leads for display
      //$scope.user = Global.user;
      //$scope.leads = Lead.query();

      $scope.leads = Lead.get(function(success) {
        //$log.log($scope.leads);
        var pages = Math.ceil($scope.leads.count / $scope.leads.results.length);

        //setting the page array
        for (var i = 0; i < pages; i++) {
          $scope.pages.push(i + 1);
        }
        //$log.log($scope.pages);
        //console.log($scope.leads);
        $scope.activePage = 1;

        //setting the lead information collapse status
        for (var i = 0; i < $scope.leads.results.length; i++) {
          $scope.infoIsCollapsed.push(false);
          $scope.notes.push('');
        }
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
      };

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
        if (!lead.booked) {
          lead.booked = !lead.booked;
          Lead.update(lead);
        }
      };

      $scope.toggleLongTerm = function(lead) {
        lead.long_term = !lead.long_term;
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

      //return class
      $scope.noFlags = function(lead) {
        if (!lead.first_response && !lead.second_response && !lead.offer && !lead.hot && !lead.booked) {
          ////console.log(lead.id + ' no flags');
          return 'no-flags';
        } else {
          return;
        }
      }
    }
  ]);