app.service('LeadStorage', ['Lead', function(Lead) {
    var store = [];
    var pages = [];
    var currentPage = null;
    this.init = function(leads) {
        store = leads;
    };
    this.getAll = function() {
        return store;
    };
    this.store = function(lead) {
        store.unshift(lead);
    };
}]);