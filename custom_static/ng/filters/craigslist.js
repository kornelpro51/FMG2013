app.filter('craigslist', function() {
  return function(key) {
    //var re = /^(\w+)@(?=craigslist)/;
    var re = /^(.+)(?=craigslist)/;
    return key.replace(re, 'guest@');
  };
})
