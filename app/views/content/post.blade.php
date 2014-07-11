@extends('layouts.main')
@section('content')
{{ $post[0] }}
<a href="{{ url('users/update'). '/' . $id }}"><button type="button" class="btn btn-primary">Edit</button></a>
@stop