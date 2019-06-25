/* 
 * iocservicesmonitor.js
 * -----------------------------------------------------------------------------
 * Utility to monitor systemd services running IOCs as micro-services
 * -----------------------------------------------------------------------------
 * ESS ERIC - ICS HWI group
 * -----------------------------------------------------------------------------
 * author: douglas.bezerra.beniz@esss.se
 * -----------------------------------------------------------------------------
 */
function unit(service, action) {
  var url = '/api/v1/' + service + '/' + action;
  $.getJSON( url, function( data ) {
    $.each( data, function( key, val ) {
      if (val == 'OK' || val == 200) {
        $('#services').load(document.URL + ' #services');
        var timerId = setInterval(function(){
          $('#services').load(document.URL + ' #services');
        }, 1000);
        setTimeout(function(){clearInterval(timerId);}, 10000);
      } else {
          $('#warningModal').modal('show')
      }
    });
  });
}

$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
  setInterval(function() {
    $('#services').load(document.URL + ' #services', function() {
      $('[data-toggle="tooltip"]').tooltip();
    });
  }, 20000);
});
