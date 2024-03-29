angular.module('start', ['ui.router', 'ngAnimate', 'ngMaterial', 'monospaced.qrcode', 'ngTable', 'angulartics', 'angulartics.google.analytics']);

angular.module('start').config(
    function($stateProvider, $urlRouterProvider, $locationProvider, $mdThemingProvider, $analyticsProvider) {
        //$locationProvider.html5Mode(true);
        $analyticsProvider.virtualPageviews(false);
        $stateProvider.state('main', {
            url: '/:event_id',
            templateUrl: 'partial/payment.html',
            resolve: {
                event:  function($http, $stateParams) {
                    return $http.get('/api/events/' + $stateParams.event_id).then(function (data) {
                        if (data.status === 200 && data.data.status === 'success') {
                            return data.data.data;
                        }
                    });
                }
            },
            controller: 'PaymentCtrl'
        });
        $stateProvider.state('order_confirm', {
            url: '/order_confirm/:order_id',
            templateUrl: 'partial/order_confirm.html'
        });
        $stateProvider.state('bus', {
            url: '/bus/:event_id',
            templateUrl: 'partial/bus.html'
        });
        $stateProvider.state('ticket', {
            url: '/ticket/:event_id',
            templateUrl: 'partial/ticket.html'
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

angular.module('start').filter('capitalize', function() {
    return function(input, all) {
        return (!!input) ? input.replace(/([^\W_]+[^\s-]*) */g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();}) : '';
    };
});