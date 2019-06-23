<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>{{hostname or 'iocservicesmonitor'}} · iocservicesmonitor</title>

    <!-- Bootstrap -->
    <!-- <link href="/static/css/bootstrap.min.css" rel="stylesheet"> -->
    <link rel="stylesheet" href="{{url_for('main.static', filename='css/bootstrap.min.css')}}">

    <!-- Custom style -->
    <!-- <link href="/static/css/iocservicesmonitor.css" rel="stylesheet"> -->
    <link rel="stylesheet" href="{{url_for('main.static', filename='css/iocservicesmonitor.css')}}">

    <!-- Favicon -->
    <!-- <link rel="shortcut icon" href="/static/img/favicon.png"> -->
    <link rel="shortcut icon" href="{{url_for('main.static', filename='img/favicon.png')}}">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="container">
      <div class="page-header text-center">
        <h1>{{hostname or 'iocservicesmonitor'}}</h1>
      </div>
      <div>
        <table class="table table-hover" id="servers">
          <tr>
            <th>Server</th>
          </tr>
          {% for server in servers %}
          <tr>
            <td class="{{server['class']}}">
            {% if server['class'] != 'active' %}
              <a href="/api/iocs/{{server['server_ip']}}"
                data-toggle="tooltip" data-placement="right" title="Open services for this server">
            {% endif %}
                {{server['title']}}
            {% if server['class'] != 'active' %}
                </a>
            {% endif %}
            </td>
          </tr>
          {% endfor %}
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="warningModal" tabindex="-1" role="dialog"
      aria-labelledby="warningModal">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
              aria-label="Close"><span
              aria-hidden="true">&times;</span></button>
            <h4 class="modal-title" id="warningModal">Attention</h4>
          </div>
          <div class="modal-body">
            The performed action cannot be done. Maybe you have
            a permissions problem.
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default"
              data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <!-- <script src="/static/js/bootstrap.min.js"></script> -->
    <script src="{{url_for('main.static', filename='js/bootstrap.min.js')}}"></script>
    <!-- <script src="/static/js/iocservicesmonitor.js"></script> -->
    <script src="{{url_for('main.static', filename='js/iocservicesmonitor.js')}}"></script>
  </body>
</html>
