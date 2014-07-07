
@extends('layouts.main')
  @section('content')
    <h1>Dashboard</h1>

    <p>Welcome to your Dashboard. You rock bitch :D !</p>
    @if(!$content)
    <p class="alert alert-info" > Ops you don't have any post !</p>
    @else
    <table class="table table-bordered">
    <thead>
    <tr>
        <th>Title</th>
        <th>Date</th>
        <th>Tag</th>
        <th>Option</th>
    </tr>
    </thead>
    @foreach ($content as $user)
        <p>{{ $user }}</p>
        <tbody>
            <tr>
                <th></th>
                <th></th>
                <th></th>
            </tr>
        </tbody>
    </table>
    @endforeach
    @endif

@stop
