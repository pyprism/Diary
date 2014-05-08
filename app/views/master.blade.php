<!doctype html>
<html lang="en">
<head>
	<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Diary</title>
    {{ HTML::style('bower_components/bootstrap/dist/css/bootstrap.min.css'); }}
    {{ HTML::script('bower_components/tinymce-release/tinymce.min.js'); }}
    {{ HTML::script('js/tinymce-custom.js'); }}
</head>
<body>
	<div class="container">
        <nav class="navbar navbar-default" role="navigation">
            <a class="navbar-brand" href="#">Hiren</a>
            <ul class="nav navbar-nav">
                <li class="active"><a href="/new-post">Add Post</a></li>
                <li class="active"><a href="/">Posts</a></li>
            </ul>
        </nav>
	</div>
    <div class="container">
        @yield('content')
    </div>
</body>
</html>
