/**
 * Created by prism on 4/17/15.
 */
angular.module('Hiren')
    .controller('LoginCtrl', function($scope, $auth) {
        $scope.login = function() {
            $auth.login({ email: $scope.email, password: $scope.password})
                .then(function(response) {
                    console.log(response.status);
                })
                .catch(function(response) {
                    sweetAlert("Oops...", "Email/Password is not correct", "error");
                });
        };

      //  $scope.authenticate = function(provider) {
     //     $auth.authenticate(provider)
     //         .then(function(response) {
     //             console.log(response.data);
     //         });
     //   };

    });