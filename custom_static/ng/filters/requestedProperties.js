app.filter('requestedProperties', function() {
	return function(properties) {
		var filtered = [];
		angular.forEach(properties, function(property, key){
			if (property.status == 'RQ' || property.status == 'NA') {
				filtered.push(property);
			}
		});
		return filtered;
	}
})