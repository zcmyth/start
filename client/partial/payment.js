angular.module('start').controller('PaymentCtrl', function($scope, $mdToast, $http, $stateParams) {

    $scope.data = {};
    $scope.form = {
        event_id: $stateParams.event_id,
        lift: 0,
        rental: 0,
        lesson: 0
    };

    var getTotal = function() {
        var data = $scope.data;
        var form = $scope.form;
        return data.bus + data.lift * form.lift + data.rental * form.rental + data.lesson * form.lesson;
    };

    $http.get('/api/events/' + $stateParams.event_id).success(function(data) {
        if (data.status) {
            $scope.data = data.data;
            $scope.data.total = getTotal();
        }
    });

    $scope.$watch('form.lift', function() {
        $scope.data.total = getTotal();
    });

    $scope.$watch('form.rental', function() {
        $scope.data.total = getTotal();
    });

    $scope.$watch('form.lesson', function() {
        $scope.data.total = getTotal();
    });

    $scope.submit = function() {
        var fieldsToCheck = [{
            value: $scope.form.first_name,
            name: 'First Name'
        }, {
            value: $scope.form.last_name,
            name: 'Last Name'
        }, {
            value: $scope.form.email,
            name: 'Email'
        }, {
            value: $scope.form.phone,
            name: 'Phone'
        }];

        for (var index in fieldsToCheck) {
            var field = fieldsToCheck[index];
            if (!field.value) {
                $mdToast.show($mdToast.simple()
                    .content('Please enter "' + field.name + '"')
                    .position('top fit'));
                return;
            }
        }
        $http.post('/api/orders', $scope.form).success(function() {
            console.log('lalal');
        });
    };
});
