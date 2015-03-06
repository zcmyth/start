angular.module('start').controller('ConsentCtrl', function($scope, $mdDialog) {
    $scope.closeDialog = function() {
        $mdDialog.hide();
    };
});

angular.module('start').controller('PaymentCtrl', function(
    $scope, $mdToast, $http, $stateParams, $window, $mdDialog, $analytics) {

    $analytics.pageTrack('/startnewyork/payment/' + $stateParams.event_id);
    var items = [
        'bus', 'lift', 'rental', 'beginner', 'helmet'
    ];
    $scope.loading = false;
    $scope.data = {};
    $scope.form = {
        event_id: $stateParams.event_id,
        bus: 1,
        location: ''
    };
    var haveOwnTicket = false;

    var getTotal = function() {
        var data = $scope.data;
        var form = $scope.form;
        var total = 0;
        angular.forEach(items, function(value) {
            if (form[value]) {
                total += data[value] * form[value];
            }
        });
        return total;
    };

    $http.get('/api/events/' + $stateParams.event_id).success(function(data) {
        if (data.status === 'success') {
            $scope.data = data.data;
            $scope.data.total = getTotal();
        }
    });

    $scope.$watch('form.lift', function() {
        $scope.data.total = getTotal();
    });

    $scope.$watch('form.rental', function() {
        $scope.form.rental_type = undefined;
        $scope.data.total = getTotal();
    });
    
    $scope.$watch('form.helmet', function() {
        $scope.data.total = getTotal();
    });

    $scope.$watch('form.beginner', function() {
        if (parseInt($scope.form.beginner) > 0) {
            $scope.form.lift = undefined;
            $scope.form.rental = undefined;
        }
        $scope.data.total = getTotal();
    });
    $scope.$watch('form.bus', function() {
        if (parseInt($scope.form.bus) > 0) {
            $scope.form.location = undefined;
        }
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
        if (parseInt($scope.form.bus) === 1 && !$scope.form.location) {
            $mdToast.show($mdToast.simple()
                    .content('Please select pickup location')
                    .position('top fit'));
                return;
        }
        if (!(parseInt($scope.form.beginner) === 1 || parseInt($scope.form.lift) === 1) && !haveOwnTicket) {
            $mdToast.show($mdToast.simple()
                    .content('You need a beginner package or a lift ticket to enjoy your ride. Click checkout again if you have your own lift ticket')
                    .hideDelay(5000)
                    .position('top fit'));
            haveOwnTicket = true;
            return;
        }
        if ((parseInt($scope.form.beginner) === 1 || parseInt($scope.form.rental) === 1) && !$scope.form.rental_type) {
            $mdToast.show($mdToast.simple()
                    .content('Please choose rental type')
                    .position('top fit'));
                return;
        }
         if (!$scope.form.consent) {
            $mdToast.show($mdToast.simple()
                    .content('Please read the liability waiver')
                    .position('top fit'));
                return;
        }
        $scope.loading = true;
        $http.post('/api/orders', $scope.form).success(function(data) {
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

    $scope.showConsent = function() {
        $mdDialog.show({
            templateUrl: 'partial/consent.html',
            controller: 'ConsentCtrl'
        });
    };
});