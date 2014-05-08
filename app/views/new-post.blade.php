@extends('master')

@section('content')
<p>Now Enter Text,File etc</p>
{{ Form::open(array('url' => 'new-post')) }}
    <textarea name="content" style="width:100%"></textarea>
{{ Form::submit('Save'); }}
{{ Form::close() }}
@stop