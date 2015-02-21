angular.module('start').controller('AdminCtrl', function(
    $scope, $http, $stateParams, ngTableParams, $filter, $mdToast) {

    var NgTableParams = ngTableParams;

    $scope.tableParams = new NgTableParams({
        page: 1,
        count: 100,
        sorting: {
            name: 'asc'
        }
    }, {
        counts: [],
        total: 1,
        getData: function($defer, params) {
            $http.get('/api/events/' + $stateParams.event_id + '/statuss').success(function(data) {
                if (data.status === 'success') {
                    var orders = data.data;
                    var orderedData = params.sorting() ?
                                $filter('orderBy')(orders, params.orderBy()) : orders;
                    $defer.resolve(orderedData);
                }
            });
        }
    });

    $scope.bus = function(order_id) {
        $http.post('/api/orders/' + order_id + '/bus').success(function(data) {
            if (data.status === 'success') {
                $mdToast.show($mdToast.simple()
                    .content('Saved')
                    .hideDelay(1)
                    .position('top fit'));
            } else {
                $mdToast.show($mdToast.simple()
                    .content(data.error)
                    .position('top fit'));
            }
        });
    };

    $scope.ticket = function(order_id) {
        $http.post('/api/orders/' + order_id + '/ticket').success(function(data) {
            if (data.status === 'success') {
                $mdToast.show($mdToast.simple()
                    .content('Saved')
                    .hideDelay(1)
                    .position('top fit'));
            } else {
                $mdToast.show($mdToast.simple()
                    .content(data.error)
                    .position('top fit'));
            }
        });
    };
});