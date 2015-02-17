angular.module('start').controller('OrderStatusCtrl', function(
    $scope, $http, $stateParams) {

    $http.get('/api/orders/' + $stateParams.order_id).success(function(data) {
        if (data.status === 'success') {
            $scope.data = data.data;
        }
    });
});
