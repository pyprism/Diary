<?php namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Contracts\Auth\Guard;
use Illuminate\Contracts\Auth\Registrar;
use Illuminate\Foundation\Auth\AuthenticatesAndRegistersUsers;
use Illuminate\Http\Response;
//use Illuminate\Http\Request;
use App\User;
use Hash;
use Request;


class AuthController extends Controller {

	/*
	|--------------------------------------------------------------------------
	| Registration & Login Controller
	|--------------------------------------------------------------------------
	|
	| This controller handles the registration of new users, as well as the
	| authentication of existing users. By default, this controller uses
	| a simple trait to add these behaviors. Why don't you explore it?
	|
	*/

	use AuthenticatesAndRegistersUsers;

	/**
	 * Create a new authentication controller instance.
	 *
	 * @param  \Illuminate\Contracts\Auth\Guard  $auth
	 * @param  \Illuminate\Contracts\Auth\Registrar  $registrar
	 *
	 */
	public function __construct(Guard $auth, Registrar $registrar)
	{
		$this->auth = $auth;
		$this->registrar = $registrar;

		$this->middleware('guest', ['except' => 'getLogout']);
	}

    /*
     * Login method
     */
    public function login() {
        $email = Request::input('email');
        $password = Request::input('password');

        $user = User::where('email', $email)->first();

        if(!$user)
            return response()->json(['message' => 'Wrong email and/or password'], 401);

        if (Hash::check($password, $user->password)) {
            unset($user->password);
            return response()->json(['token' => $this->createToken($user)]);
        }

        else
            return response()->json(['message' => 'Wrong email and/or password'], 401);
    }

    /*
     * Sign up method
     */

    public function signup() {
        $user = User::all()->first();
        if($user)  // check if already 1 user already registered
            return response()->json(['message' => 'Luke I am your father, Your father already exits'], 401);
        $user = new User;
        $user->name = Request::input('name');
        $user->email = Request::input('email');
        $user->password = Hash::make(Request::input('password'));
        $user->save();

        return response()->json(['token' => $this->createToken($user)]);
    }

}
