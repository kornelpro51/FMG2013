app.factory('GlobalLeadsArray', function($http) {
	var data = [1, 2, 3];

	return {
		init: function () {
			data = $http.get('/api/leads/');
			return data;
		},
		push: function(lead) {
			data.push(lead);
			return false;
		},
		getData: function() {
			return data;
		}
	}
});

