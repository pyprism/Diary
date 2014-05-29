<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hiren</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ HTML::style('bower/bootstrap/dist/css/bootstrap.css') }}
    {{ HTML::style('main.css') }}
    {{ HTML::style('bower/jquery/dist/jquery.js') }}
    {{ HTML::style('bower/bootstrap/dist/js/bootstrap.js') }}
</head>
<body>
<div class="navbar navbar-fixed-top">
    <div class="navbar-inner">
        <div class="container">
            <ul class="nav">
                @if(!Auth::check())
                <li>{{ HTML::link('users/register', 'Register') }}</li>
                <li>{{ HTML::link('users/login', 'Login') }}</li>
                @else
                <li>{{ HTML::link('users/logout', 'logout') }}</li>
                @endif
            </ul>
        </div>
    </div>
</div>
<div class="container">
    @if(Session::has('message'))
    <p class="alert">{{ Session::get('message') }}</p>
    @endif
</div>
{{ $content }}
</body>
</html>