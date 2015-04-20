/**
 * Created by prism on 4/20/15.
 */
angular.module('Hiren')
    .controller('LogOutCtrl', function($auth) {
        if (!$auth.isAuthenticated()) {
            return;
        }
        $auth.logout();
    })