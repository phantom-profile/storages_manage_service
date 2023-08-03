function click_alert(selector, msg){
  $(selector).click(function(){ alert(msg) })
}

function show_weather(location) {
  $.ajax({
    url: '/storages/current_weather',
    data: {
      "location": location
    },
    dataType: 'json',
    success: function(data) {
      $('#storage-weather-info').html(build_response(data))
    },
    error : function(response){
     alert(response.responseJSON.error.message)
    }
  })
}

function build_response(data) {
  const w = {
    country: data.location.country,
    city: data.location.name,
    upd: data.current.last_updated,
    cond: data.current.condition.icon,
    temp: data.current.temp_c,
    wind: data.current.wind_kph
  }

  let img = `<img src="${w.cond}" width = "20" height = "20">`
  let msg = `Weather in ${w.country} ${w.city} at ${w.upd}: ${img} t: ${w.temp} C°, w: ${w.wind} km/h`

  return msg
}

function show_currencies() {
  $.ajax({
    url: '/users/convert_currency',
    data: {
      "convert_from": $('#id_convert_from').val(),
      "convert_to": $('#id_convert_to').val(),
      "amount_from": $('#id_amount_from').val()
    },
    dataType: 'json',
    success: function(data) {
      $('#id_amount_to').val(data.to_value)
    },
    error : function(response){
     alert(response.responseJSON.error)
    }
  })
}

function refresh_table() {
  $.ajax({
    url: '/storages/index',
    data: {
      "table_only": true,
      "name__contains": $('#id_name__contains').val(),
      "location__contains": $('#id_location__contains').val(),
      "capacity__gte": $('#id_capacity__gte').val(),
      "sort_by": $('#id_sort_by').val(),
      "reverse_order": $('#id_reverse_order').is(":checked"),
    },
    dataType: 'html',
    success: function(data) {
      $('#storages_table').html(data)
    },
    error : function(response){
     alert(response.responseJSON.error)
    }
  })
}

$('#id_currencies_form').on('submit', function(event){
  event.preventDefault();
  show_currencies();
});

$('#id_storages_form').on('submit', function(event){
  event.preventDefault();
  refresh_table();
});
