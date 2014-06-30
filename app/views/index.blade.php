<!doctype html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Welcome</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ HTML::style('bower/bootstrap/dist/css/bootstrap.css') }}
    {{ HTML::style('main.css') }}
	<style>
		@import url(//fonts.googleapis.com/css?family=Lato:700);

		body {
			margin:0;
			font-family:'Lato', sans-serif;
			text-align:center;
			color: #999;
		}

		.welcome {
			width: 300px;
			height: 200px;
			position: absolute;
			left: 50%;
			top: 50%;
			margin-left: -150px;
			margin-top: -100px;
		}

		a, a:visited {
			text-decoration:none;
		}

		h1 {
			font-size: 32px;
			margin: 16px 0 0 0;
		}
	</style>
</head>
<body>
	<div class="welcome">
        <button type="button" class="btn btn-default btn-l">
            <span class="glyphicon glyphicon-user"> {{ HTML::link('users/login', 'Login') }}</span>
        </button>
        OR
        <button type="button" class="btn btn-default btn-l">
            <span class="glyphicon glyphicon-registration-mark"> {{ HTML::link('users/register', 'Register') }}</span>
            </a>
        </button>
		<h1>Hiren Blog</h1>
	</div>
</body>
</html>
