<div class="container">
{{ Form::open(array('url'=>'users/signin', 'class'=>'form-inline')) }}
<h2 class="form-signin-heading">Please Login</h2>
<div class="form-group">
{{ Form::text('email', null, array('class'=>'input-block-level', 'placeholder'=>'Email Address')) }}
</div>
<div class="form-group">
{{ Form::password('password', array('class'=>'input-block-level', 'placeholder'=>'Password')) }}
</div>
{{ Form::submit('Login', array('class'=>'btn btn-default'))}}
{{ Form::close() }}
</div>
