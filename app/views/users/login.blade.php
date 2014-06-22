<div class="container">
    <div class="center">
        {{ Form::open(array('url'=>'users/signin', 'class'=>'clearfix')) }}
        <h2 class="form-signin-heading">Please Login</h2>
        <div class="form-group">
            {{ Form::email('email', null, array('class'=>'form-control', 'placeholder'=>'Email Address')) }}
        </div>
        <div class="form-group">
            {{ Form::password('password', array('class'=>'form-control', 'placeholder'=>'Password')) }}
        </div>
        {{ Form::submit('Login', array('class'=>'btn btn-default '))}}
        {{ Form::close() }}
    </div>
</div>
