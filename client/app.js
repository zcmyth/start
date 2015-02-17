angular.module('start', ['ui.router', 'ngAnimate', 'ngMaterial', 'monospaced.qrcode']);

angular.module('start').config(
    function($stateProvider, $urlRouterProvider, $locationProvider, $mdThemingProvider) {
        //$locationProvider.html5Mode(true);
        $stateProvider.state('main', {
            url: '/:event_id',
            templateUrl: 'partial/payment.html'
        });
        $stateProvider.state('trip', {
            url: '/trip/:event_id',
            templateUrl: 'partial/payment.html'
        });
        $stateProvider.state('ticket', {
            url: '/ticket/:ticket_id',
            templateUrl: 'partial/ticket.html'
        });
        $stateProvider.state('order_confirm', {
            url: '/order_confirm/:order_id',
            templateUrl: 'partial/order_confirm.html'
        });
        /* Add New States Above */
        $urlRouterProvider.otherwise('/');

        $mdThemingProvider.theme('default')
            .primaryPalette('blue')
            .accentPalette('indigo');
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