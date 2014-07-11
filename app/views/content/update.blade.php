@extends('layouts.main')
@section('content')
<div class="container">
    {{ Form::open() }}
    Title
    {{ Form::text('title', $post[0]->title) }} Tag {{ Form::text('tag', $post[0]->tag) }}
    {{ Form::textarea('content', $post[0]->text) }}
    {{ Form::submit('Update', array('class' => 'btn')) }}
    {{ Form::close() }}
</div>
@stop