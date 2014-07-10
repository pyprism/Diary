@extends('layouts.main')
@section('content')
<div class="container">
    {{ Form::open() }}
    Title
    {{ Form::text('title', {{ $post->title }}) }} Tag @if($post->tag){{ Form::text('tag', {{ $post->tag }}) }}@else{{ Form::text('tag') }@endif
    {{ Form::textarea('content', {{ $post->text }}) }}
    {{ Form::submit('Save', array('class' => 'btn')) }}
    {{ Form::close() }}
</div>
@stop