/**
 * Created by prism on 4/17/15.
 */
angular.module('Hiren')
    .controller('LoginCtrl', function($scope, $auth) {
        $scope.login = function() {
            $auth.login({ email: $scope.email, password: $scope.password})
                .then(function(response) {
                    console.log('login' + response.data);
                });
        };

        $scope.authenticate = function(provider) {
          $auth.authenticate(provider)
              .then(function(response) {
                  console.log('authenticated' + response.data);
              });
        };

    });