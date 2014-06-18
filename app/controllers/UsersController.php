<?php
/**
 * Created by PhpStorm.
 * User: prism
 * Date: 5/29/14
 * Time: 1:48 PM
 */

class UsersController extends BaseController {
    protected $layout = "layouts.main";

    public function __construct() {
        $this->beforeFilter('csrf', array('on'=>'post'));
        $this->beforeFilter('auth', array('only'=>array('getDashboard' , 'getEditr')));
    }

    public function getRegister(){
        if (Auth::check()){
            return Redirect::to('users/dashboard')->with('message', 'You are already logged in !');
        }else
            $this->layout->content = View::Make('users.register');
    }

    public function postCreate() {

        $validator = Validator::make(Input::all(), User::$rules);

        if ($validator->passes()) {
            // validation has passed, save user in DB
            $user = new User;
            $user->firstname = Input::get('firstname');
            $user->lastname = Input::get('lastname');
            $user->email = Input::get('email');
            $user->password = Hash::make(Input::get('password'));
            $user->save();

            return Redirect::to('users/login')->with('message', 'Thanks for registering!');
        } else {
            // validation has failed, display error messages
            return Redirect::to('users/register')->with('message', 'The following errors occurred')->withErrors($validator)->withInput();
        }
    }

    public function getLogin() {
        if (Auth::check())
        {
            return Redirect::to('users/dashboard')->with('message', 'You are already logged in !');
        }else
            $this->layout->content = View::make('users.login');
    }

    public function postSignin() {
        if (Auth::attempt(array('email'=>Input::get('email'), 'password'=>Input::get('password')))) {
            return Redirect::to('users/dashboard')->with('message', 'You are now logged in!');
        } else {
            return Redirect::to('users/login')
                ->with('message', 'Your username/password combination was incorrect')
                ->withInput();
        }
    }

    public function getDashboard() {
        if (!Auth::check()){
            return Redirect::to('users/login')->with('message', 'You motherf@)ker are not logged in !');
        }else{
            $contents = DB::table('content')->where('author_id', Auth::User()->id )->first();
            $this->layout->content = View::make('users.dashboard')-> with('content' , $contents);
            //print_r($contents);
            //return Content::All();
        }
    }

    public function getLogout() {
        Auth::logout();
        return Redirect::to('users/login')->with('message', 'Your are now logged out!');
    }

    public function getEditor(){
        if (!Auth::check()){
            return Redirect::to('users/login')->with('message', 'You motherf@)ker are not logged in !');
        }else
            $this->layout->content = View::make('content.editor');
    }

    public function postEditor(){
        if (Auth::check()){
            if (Input::has('title') && Input::has('editor1'))
            {
                $content = new Content;
                $content->title = Input::get('title');
                $content->text = Input::get('editor1');
                $content->author_id = Auth::user()->id;
                $content->save();
                return Redirect::to('users/dashboard')->with('message','Post Saved');

            }else{
                return Redirect::to('users/editor')->with('message','Maybe Title or Content is missing ! ');
            }
        }
    }
}