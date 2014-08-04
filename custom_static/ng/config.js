var app = angular.module(
  'app', [
    'ngRoute',
    'ngResource',
    'ngSanitize',
    'ui.bootstrap',
    'ui.select2',
    'ngCkeditor',
    'truncate',
    'toaster'
  ]
);

//ysf: configuring the app to set csrf tokens in the headers

app.config(function($httpProvider) {
  //ysf: in the backend, make sure the view forces csrf cookie in the token
  //ysf: now getting the csrftoken value from the cookie and adding it to the
  //ysf: $http request headers, so that the post data does not get rejected

  $httpProvider.defaults.headers.common['X-CSRFToken'] = window.document.cookie.match(/csrftoken=([^;]+)/)[1];
  $httpProvider.defaults.cache = false;
  //console.log(window.document.cookie.match(/csrftoken=([^;]+)/)[1]);
});


// ysf: adding the route parameters to the angular app
// so that it can decide which controller to call in the view

app.config(function($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: '/partials/home.html',
      controller: 'HomeCtrl'
    })
    .when('/lead/add/', {
      templateUrl: '/partials/lead/add.html',
      controller: 'AddLeadCtrl'
    })
    .when('/lead/:leadID/properties/edit/', {
      templateUrl: '/partials/lead/editProperties.html',
      controller: 'EditLeadPropertiesCtrl'
    })
    .when('/lead/:leadID/response/:responseType', {
      templateUrl: '/partials/lead/editResponse.html',
      controller: 'EditLeadResponseCtrl'
    })
    .otherwise({
      redirectTo: '/'
    });
});

//adding all properties to save one request on each page

app.run(function($rootScope, Property) {
  $rootScope.properties = Property.get({
    page_size: 9999
  });
});