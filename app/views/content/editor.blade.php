
{{ Form::open(array('url' => 'users/editor')) }}
{{ Form::text('title', 'Enter a title for your post') }}
{{ Form::textarea('editor1', null, array(
'id'      => 'editor1',
'name'    => 'editor1') ) }}
{{ Form::submit('Click Me Asshole !') }}
{{ Form::close() }}

<div class="container">
    @if(Session::has('message'))
    <p class="alert">{{ Session::get('message') }}</p>
    @endif
</div>