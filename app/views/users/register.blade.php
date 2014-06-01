
{{ Form::open(array('url'=>'users/create', 'class'=>'form-horizontal')) }}
<h2 class="form-signup-heading">Please Register</h2>

<ul>
    @foreach($errors->all() as $error)
    <li>{{ $error }}</li>
    @endforeach
</ul>
<div class="form-group">
{{ Form::text('firstname', null, array('class'=>'input-block-level', 'placeholder'=>'First Name')) }}
</div>
<div class="form-group">
{{ Form::text('lastname', null, array('class'=>'input-block-level', 'placeholder'=>'Last Name')) }}
</div>
<div class="form-group">
{{ Form::text('email', null, array('class'=>'input-block-level', 'placeholder'=>'Email Address')) }}
</div>
<div class="form-group">
{{ Form::password('password', array('class'=>'input-block-level', 'placeholder'=>'Password')) }}
</div>
<div class="form-group">
{{ Form::password('password_confirmation', array('class'=>'input-block-level', 'placeholder'=>'Confirm Password')) }}
</div>

{{ Form::submit('Register', array('class'=>'btn btn-default'))}}
{{ Form::close() }}
