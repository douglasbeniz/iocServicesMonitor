<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>{{hostname or 'iocservicesmonitor'}} · iocservicesmonitor</title>
    <!-- Bootstrap -->
    <link rel="stylesheet" href="{{url_for('main.static', filename='css/bootstrap.min.css')}}">
    <!-- Custom style -->
    <link rel="stylesheet" href="{{url_for('main.static', filename='css/iocservicesmonitor.css')}}">
    <!-- Favicon -->
    <link rel="shortcut icon" href="{{url_for('main.static', filename='img/favicon.png')}}">
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
              <a href="http://{{server['server_ip']}}:5000/api/v1/iocs"
                data-toggle="tooltip" data-placement="right" title="Open services for this server ({{server['server_ip']}})">
                {{server['title']}}
              </a>
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
    <script src="{{url_for('main.static', filename='js/bootstrap.min.js')}}"></script>
    <script src="{{url_for('main.static', filename='js/iocservicesmonitor.js')}}"></script>
  </body>
</html>
