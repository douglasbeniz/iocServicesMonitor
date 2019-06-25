<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>{{service}} journal · {{hostname or 'iocservicesmonitor'}} · iocservicesmonitor</title>
    <!-- Bootstrap -->
    <link rel="stylesheet" href="{{url_for('api.static', filename='css/bootstrap.min.css')}}">
    <!-- Custom style -->
    <link rel="stylesheet" href="{{url_for('api.static', filename='css/iocservicesmonitor.css')}}">
    <!-- Favicon -->
    <link rel="shortcut icon" href="{{url_for('api.static', filename='img/favicon.png')}}">
  </head>
  <body>
    <div class="container-fluid">
      <div class="page-header text-center">
        <h1>{{service}} journal<br/>
        <small>{{hostname or 'iocservicesmonitor'}}</small></h1>
      </div>
      <div>
<pre id="journal">
{% for line in journal %}
{{line}}
{% endfor %}
</pre>
      </div>
    </div>
  </body>
</html>
