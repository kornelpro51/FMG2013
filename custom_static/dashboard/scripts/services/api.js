app.factory('Lead', ['$resource',
    function($resource) {
        return $resource(
            '/api/leads/:id', {
                id: '@id'
            }, {
                update: {
                    method: 'PUT'
                },
                hot: {
                    method: 'GET',
                    params: {
                        ordering: '-hot'
                    },
                    isArray: false
                },
                search: {
                    method: 'GET',
                    isArray: false
                }
            }
        );
    }
]);

app.factory('LeadProperty', ['$resource',
    function($resource) {
        return $resource(
            '/api/leads/:leadID/properties/:id', {
                id: '@id',
                leadID: '@lead'
            }, {
                update: {
                    method: 'PUT'
                }
            }
        );
    }
]);


app.factory('Customer', ['$resource',
    function($resource) {
        return $resource(
            '/api/customers/:id', {
                id: '@id'
            }, {
                update: {
                    method: 'PUT',
                }
            }
        );
    }
]);

app.factory('Property', ['$resource',
    function($resource) {
        return $resource(
            '/api/properties/:id', {
                id: '@id'
            }, {
                update: {
                    method: 'PUT'
                }
            }
        );
    }
]);

app.factory('Message', ['$resource',
    function($resource) {
        return $resource(
            '/api/messages/:id', {
                id: '@id'
            }, {
                update: {
                    method: 'PUT'
                }
            }
        );
    }
]);


app.factory('Notification', ['$resource',
    function($resource) {
        return $resource(
            '/api/notifications/', {
                id: '@id'
            }, {
                update: {
                    method: 'PUT'
                }
            }
        );
    }
]);

app.factory('Template', ['$resource',
    function($resource) {
        return $resource(
            '/api/template/:listCtrl/:lead', {
                listCtrl: '@listCtrl',
                lead: '@lead'
            }, {
                first_response: {
                    method: 'GET',
                    params: {
                        listCtrl: 'first_response'
                    }
                },
                second_response: {
                    method: 'GET',
                    params: {
                        listCtrl: 'second_response'
                    }
                },
                offer_response: {
                    method: 'GET',
                    params: {
                        listCtrl: 'offer_response'
                    }
                },
                concierge_response: {
                    method: 'GET',
                    params: {
                        listCtrl: 'concierge_response'
                    }
                },
                default_response: {
                    method: 'GET',
                    params: {
                        listCtrl: 'default_response'
                    }
                }
            }
        );
    }
]);

app.factory('Note', ['$resource',
    function($resource) {
        return $resource(
            '/api/notes/:id/', {
                id: '@id'
            }, {
                update: {
                    method: 'PUT'
                }
            }
        );
    }
]);
