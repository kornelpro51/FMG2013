app.filter('fromNow', function ($rootScope) {
  return function (dateString) {
    return moment(new Date(dateString)).from($rootScope.date)
  };
});