<div class="container">
    <h1>Dashboard</h1>

    <p>Welcome to your Dashboard. You rock bitch :D !</p>
    @if(!$content)
    <p class="alert alert-info" > Ops you don't have any post !</p>
    @else
    @foreach ($content as $user)
    <p>{{ $user }}</p>
    @endforeach
    @endif
</div>

