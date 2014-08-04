/**
 * Created with PyCharm.
 * User: paolo
 * Date: 12/09/13
 * Time: 19:25
 * To change this template use File | Settings | File Templates.
 */
function HeaderCtrl($scope, $rootScope, socket, $timeout, $log, $location) {
    $scope.messages = [];
    $scope.alerts = []
    $scope.nicknames = [];
    $scope.nickname = '';
    $scope.login = false;
    $scope.connected = false;
    $scope.room = '';
    var setClock = function () {
                $scope.date = new Date();
                $timeout(setClock, 1000);
            };
            setClock();

    socket.on('connect', function (result) {
        if (!$scope.connected){
            socket.emit('subscribe', $rootScope.init_val.room, function(result, pkg){
            if (result){
                $log.debug('connected to ' + pkg);
                return;
            }
            $log.debug('Not connected!');
        });
        }
        $scope.connected = true;
        return false;
    });


    socket.on('msg_to_room', message);

    function message(from, msg) {
        $scope.messages.push({
            user: from,
            text: msg
        });
        $log.debug(msg)
    }

    socket.on('alert', pop_msg);

    function pop_msg(data){
        $log.debug(data)
        if(data.alert){
            $scope.alerts.push(data)
        }

        $log.debug($scope.alerts.length)
    }

    socket.on('joined', joined);

    function joined(room){
        $scope.room = room;
        $log.debug('Joined room: ');
    }

     $scope.editLead = function (alert) {
         $location.path('/lead/' + alert.object.id + '/properties/edit/');
         socket.emit('viewed', alert.id)
     };


    $scope.sendMessage = function () {
        $log.debug($scope.message);
        socket.emit('user_message', $scope.message);

        // add the message to our model locally
        $scope.messages.push({
            user: 'Me',
            text: $scope.message
        });

        // clear message box
        $scope.message = '';
        return false;
    };

}

