angular.module('start', ['ui.router', 'ngAnimate', 'ngMaterial']);

angular.module('start').config(
    function($stateProvider, $urlRouterProvider, $locationProvider) {
        //$locationProvider.html5Mode(true);
        $stateProvider.state('welcome', {
            url: '/:event_id',
            templateUrl: 'partial/payment.html'
        });
        /* Add New States Above */
        $urlRouterProvider.otherwise('/');
    });

angular.module('start').run(function($rootScope) {

    $rootScope.safeApply = function(fn) {
        var phase = $rootScope.$$phase;
        if (phase === '$apply' || phase === '$digest') {
            if (fn && (typeof(fn) === 'function')) {
                fn();
            }
        } else {
            this.$apply(fn);
        }
    };

});

angular.module('start').controller('MainCtrl', function($rootScope, $scope) {
});