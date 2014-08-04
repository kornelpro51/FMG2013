app.controller(
  'HeaderCtrl', ["$scope", "$rootScope", "$http", "$timeout", "$log", "$location", "socket",
    function($scope, $rootScope, $http, $timeout, $log, $location, socket) {
      $scope.messages = [];
      $scope.login = false;
      $scope.connected = false;
      $scope.room = null;

      //setting the clock (a continuous loop)
      var setClock = function() {
        $rootScope.date = new Date();
        $timeout(setClock, 60000);
      };

      //function to add alert to the alert array
      var addAlert = function(alert) {
        //$rootScope.alerts.push(alert);
        if (alert.alert) {
          $rootScope.alerts.push(alert);
        }
      };

      //function to delete viewed alert
      var delAlert = function(alert_id) {
        if (!isNaN(alert_id)) {
          alert_id = parseInt(alert_id);
        };
        angular.forEach($rootScope.alerts, function(alert, idx) {
          //console.log(alert.id);
          if (alert_id === alert.id) {
            $rootScope.alerts.splice(idx, 1);
          }
        });
      };

      //function to connect to socket.io
      var connectSocket = function(data) {
        if (!$scope.connected) {
          socket.emit('subscribe', $rootScope.init_val.room, function(data, pkg) {
            if (data) {
              //$log.debug('connected to ' + pkg);
              return false;
            } else {
              //$log.debug('Not connected!');
              return false;
            }
          });
        }
        $scope.connected = true;
        return false;
      };


      //join the room
      var joinRoom = function(room) {
        $scope.room = room;
        //$log.debug('Joined room: ' + room);
      };

      //function to view alert
      $scope.viewAlert = function(alert) {
        $location.path('/lead/' + alert.object.id + '/properties/edit/');
        //delAlert(alert.id);
        //socket.emit('viewed', alert.id);
      };

      $scope.muteAlert = function(alert) {
        socket.emit('viewed', alert.id);
      };


      //execute the script

      //set initial alerts
      $http.get('/api/leadnotifications/').success(function(data) {
        $rootScope.alerts = [];
        angular.forEach(data.results, function(val, key) {
          //$log.debug(val);
          if (val.alert) {
            $rootScope.alerts.push(val);
          }
        });
      });

      //set the clock
      setClock();

      //listen to the socket
      //when the socket broadcasts 'connect', send the signal 'subscribe'
      socket.on('connect', connectSocket);

      //when the socket broadcasts 'alert', push the broadcast data in the alert array
      socket.on('alert', addAlert);

      //when the socket emits 'joined', set the global room
      //this is done if the socket is not connected
      socket.on('joined', joinRoom);

      //when the socket broadcasts 'viewed', delete the viewed alert from alerts[]
      socket.on('deleted', delAlert);
    }
  ]);