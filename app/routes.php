<?php

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It's a breeze. Simply tell Laravel the URIs it should respond to
| and give it the Closure to execute when that URI is requested.
|
*/

Route::get('/', function()
{
    $register = action('UsersController@getRegister');
    $login = action('UsersController@getLogin');
    $data = array( 'register'=>$register, 'login'=>$login);
	return View::make('index', $data);
});

Route::controller('users', 'UsersController');