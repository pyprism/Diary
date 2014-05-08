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
	return View::make('master');
});

Route::get('new-post', function(){
    return View::make('new-post');
});

Route::post('new-post',function(){
    //return Input::all();
    return Input::get('content');
    //return Redirect::to('/');
});