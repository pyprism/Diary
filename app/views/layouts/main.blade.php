<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hiren</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ HTML::style('bower/bootstrap/dist/css/bootstrap.css') }}
    {{ HTML::style('main.css') }}
    <link rel="shortcut icon" href="{{{ asset('favicon.ico') }}}">
</head>
<body>
<nav class="navbar navbar-default navbar-fixed-tops" role="navigation">
    <a class="navbar-brand" href="/">Hiren</a>
    <div class="collapse navbar-collapse">
        <ul class="nav navbar-nav">
            @if(!Auth::check())
            <li>{{ HTML::link('users/register', 'Register') }}</li>
            <li>{{ HTML::link('users/login', 'Login') }}</li>
            @else
            <li>{{ HTML::link('users/dashboard', 'Dashboard') }}</li>
            <li>{{ HTML::link('users/editor', 'Create New Post') }}</li>
            <li>{{ HTML::link('users/logout', 'Logout') }}</li>
            @endif
        </ul>
    </div>
</nav>
{{-- <div class="container"> --}}
    @if(Session::has('message'))
    <p class="alert alert-info">{{ Session::get('message') }}</p>
    @endif
{{-- </div> --}}
<div class="container" >
    {{-- {{ $content }} --}}
    @yield('content')
</div>



{{ HTML::script('bower/jquery/dist/jquery.js') }}
{{ HTML::script('bower/bootstrap/dist/js/bootstrap.js') }}
{{ HTML::script('bower/ckeditor/ckeditor.js') }}
{{ HTML::script('editor.js') }}
</body>
</html>