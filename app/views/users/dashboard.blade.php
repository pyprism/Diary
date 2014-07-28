
@extends('layouts.main')
@section('content')
<h1>Dashboard</h1>

<p>Welcome to your Dashboard. You rock bitch :D !</p>
@if(!$contents)
<div class="row">
<p class="alert alert-warning col-md-4 col-md-offset-4" > Ops you don't have any post !</p>
</div>
@else
<table class="table table-bordered table-hover">
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
        @if(!$content->tag)
        <th>None</th>
        @else
        <th>{{ $content->tag }}</th>
        @endif
    </tr>
    @endforeach
    </tbody>
</table>

@endif

@stop
