var app = angular.module(
    'app', [
        'ngResource',
        'ngSanitize',
        'ngRoute',
        'ui.bootstrap'
    ]
);

//ysf: configuring the app to set csrf tokens in the headers

app.config(function($httpProvider) {
    //ysf: in the backend, make sure the view forces csrf cookie in the token
    //ysf: now getting the csrftoken value from the cookie and adding it to the
    //ysf: $http request headers, so that the post data does not get rejected

    $httpProvider.defaults.headers.common['X-CSRFToken'] = window.document.cookie.match(/csrftoken=([^;]+)/)[1];
    console.log(window.document.cookie.match(/csrftoken=([^;]+)/)[1]);
});


// ysf: adding the route parameters to the angular app
// so that it can decide which controller to call in the view

app.config(function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: '/partials/v2/main.html',
            controller: 'MainCtrl'
        })
        .otherwise({
            redirectTo: '/'
        })
});


