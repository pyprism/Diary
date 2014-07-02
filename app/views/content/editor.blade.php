<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hiren</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ HTML::style('bower/bootstrap/dist/css/bootstrap.min.css') }}
    {{ HTML::style('bower/Font-Awesome/css/font-awesome.min.css') }}
    {{ HTML::style('main.css') }}
    <link rel="shortcut icon" href="{{{ asset('favicon.ico') }}}">
</head>
<body>
<div class="container">
    <header class="navbar navbar-default navbar-fixed-to" >
        <a class="navbar-brand" href="/">Hiren</a>
        <div class="collapse navbar-collapse">
            <ul class="nav navbar-nav">
                @if(!Auth::check())
                <li><a href="{{ url('users/register')}}" class="fa fa-sign-in"> Register</a></li>
                <li><a href="{{ url('users/login') }}" class="fa fa-heart"> Login</a></li>
                @else
                <li><a href="{{ url('users/dashboard')}}" class="fa fa-square-o"> Dashboard</a></li>
                <li><a href="{{ url('users/editor') }}" class="fa fa-book"> Create New Post</a></li>
                <li ><a href="https://github.com/pyprism/Diary" class="fa fa-github"> Source Code</a></li>
                <li><a href="{{ url('users/logout') }}" class="fa fa-sign-out"> Logout</a></li>
                @endif
            </ul>
        </div>
    </header>
</div>

    @if(Session::has('message'))
    <p class="alert alert-info">{{ Session::get('message') }}</p>
    @endif
<div class="container">

    <div class="raptor-editable" data-id="main-content">
        <input type='hidden' id='csrf'  value='{{ $csrf }}' />
        <p>
            Raptor may be integrated into a site many ways.
            This article aims to cover the simplest integration possible.
            asdasdasd
            asd asd ad asd
             ads asd

        </p>
    </div>
</div>



{{ HTML::script('bower/jquery/dist/jquery.min.js') }}
{{ HTML::script('bower/bootstrap/dist/js/bootstrap.min.js') }}
{{ HTML::script('raptor/example/libraries/jquery-ui.js') }}
{{ HTML::script('raptor/raptor.min.js') }}
{{ HTML::style('raptor/raptor-front-end.min.css') }}
{{ HTML::script('editor.js') }}
</body>
</html>