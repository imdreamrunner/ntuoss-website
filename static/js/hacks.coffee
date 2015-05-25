eventItemTemplate = _.template $("#event-item").html()

$(document).ready ->
  $.ajax
    url: "/tgifhacks/events"
    dataType: "json"
    success: (data) ->
      $events = $("#events")
      $events.html ""
      events = data['data']
      for event in events
        $events.append eventItemTemplate(event)