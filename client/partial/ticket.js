angular.module('start').controller('TicketCtrl', function(
    $scope, $mdToast, $http, $stateParams, $window) {

    $scope.loading = false;
    $scope.data = {};
    $scope.form = {
        ticket_id: $stateParams.ticket_id,
        lift: 6,
        snowboard: 0,
        ski: 0,
    };

    var getTotal = function() {
        var data = $scope.data;
        var form = $scope.form;
        return data.lift * form.lift + data.snowboard * form.snowboard + data.ski * form.ski;
    };

    $http.get('/api/tickets/' + $stateParams.ticket_id).success(function(data) {
        if (data.status === 'success') {
            $scope.data = data.data;
            $scope.data.total = getTotal();
        }
    });

    $scope.$watch('form.lift', function() {
        $scope.data.total = getTotal();
    });

    $scope.$watch('form.snowboard', function() {
        $scope.data.total = getTotal();
    });

    $scope.$watch('form.ski', function() {
       $scope.data.total = getTotal();
    });

    $scope.range = function(min, max, step) {
        step = step || 1;
        var input = [];
        for (var i = min; i <= max; i += step) {
            input.push(i);
        }
        return input;
    };

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
        $scope.loading = true;
        $http.post('/api/tickets', $scope.form).success(function(data) {
            if (data.status === 'success') {
                $window.location.href = data.data;
            } else {
                $scope.loading = false;
                $mdToast.show($mdToast.simple()
                    .content(data.message)
                    .position('top fit'));
            }
        }).error(function(data) {
            $mdToast.show($mdToast.simple()
                    .content('Something wrong...')
                    .position('top fit'));
            $scope.loading = false;
        });
    };
});
