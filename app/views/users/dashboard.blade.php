<div class="container">
    <h1>Dashboard</h1>

    <p>Welcome to your Dashboard. You rock bitch :D !</p>
    @if(!$content)
    Ops you don't have any post !
    @else
    @foreach ($content as $user)
    <p>{{ $user}}</p>
    @endforeach
    @endif
</div>

