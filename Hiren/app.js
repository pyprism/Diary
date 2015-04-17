/**
 * Created by prism on 4/16/15.
 */
angular.module('Hiren', ['ngResource', 'ngRoute', 'satellizer'] )
    .config(function($authProvider, $routeProvider, $locationProvider) {
       $routeProvider
           .when('/', {
               templateUrl: 'partials/login.html',
               controller: 'LoginCtrl'
           })
           .when('/logout', {
               templateUrl: 'partials/logout.html',
               controller: 'LogoutCtrl'
           })
           .when('/posts', {
               templateUrl: 'partials/allPosts.html',
               controller: 'AllPostCtrl'
           })
           .when('/posts/:postId', {
               templateUrl: 'partials/post.html',
               controller: 'PostCtrl'
           })
           .when('/posts/new', {
               templateUrl: 'partials/new.html',
               controller: 'NewCtrl'
           });
        $locationProvider.html5Mode(true);
    });