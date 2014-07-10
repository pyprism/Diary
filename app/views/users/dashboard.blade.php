
@extends('layouts.main')
@section('content')
<h1>Dashboard</h1>

<p>Welcome to your Dashboard. You rock bitch :D !</p>
@if(!$contents)
<p class="alert alert-info" > Ops you don't have any post !</p>
@else
<table class="table table-bordered">
    <thead>
    <tr>
        <th>Title</th>
        <th>Created At</th>
        <th>Updated At</th>
        <th>Tag</th>
    </tr>
    </thead>

    <tbody>
    @foreach ($contents as $content)
    <tr>
        <th><a href='{{ url("users/post") . '/' . $content->id }}'>{{ $content->title }}</a></th>
        <th>{{ $content->created_at }}</th>
        <th>{{ $content->updated_at }}</th>
        @if($content->tag)
        <th>{{ $content->tag }}</th>
        @endif
        <th>None</th>
    </tr>
    @endforeach
    </tbody>
</table>

@endif

@stop
