<!doctype html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Welcome</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ HTML::style('bower/bootstrap/dist/css/bootstrap.min.css') }}
    {{ HTML::style('bower/Font-Awesome/css/font-awesome.min.css') }}
    {{ HTML::style('main.css') }}

</head>
<body>
	<div class="welcome">
            <a href="{{ $login }}" class="btn btn-default btn-lg">
                <i class="fa fa-sign-in fa-lg"></i> Login
            </a>

            <a href="{{ $register }}" class="btn btn-default btn-lg">
                <i class="fa fa-heart fa-lg"></i> Register
            </a>
		<h1>Hiren Blog</h1>
	</div>
</body>
</html>
