<?php namespace App\Http\Controllers;

use Illuminate\Foundation\Bus\DispatchesCommands;
use Illuminate\Routing\Controller as BaseController;
use Illuminate\Foundation\Validation\ValidatesRequests;
use JWT;
use Config;

abstract class Controller extends BaseController {

	use DispatchesCommands, ValidatesRequests;

    /*
     * Method for JWT token generation
     */

    protected function createToken($user) {
        $payload = array(
            'sub' => $user->id,
            'iat' => time(),
            'exp' => time() + (2 * 7 * 24 * 60 * 60) //14 days
        );
        return JWT::encode($payload, Config::get('secrets.TOKEN_SECRET'));
    }

}
