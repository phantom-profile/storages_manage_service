function click_alert(selector, msg){
  $(selector).click(function(){ alert(msg) })
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

$('#converter_link').click(function(e) {
  $.ajax({
    method: 'GET',
    url: '/users/convertor',
    success: function(data) {
      $('#convertor-form-display').html(data)
      $('#convertor_modal').modal('show');
      $('#id_currencies_form').on(
        'submit',
        function(event) {
          event.preventDefault()
          show_currencies()
        }
      )
    },
    error: function(error_data) {
      console.log("error")
      console.log(error_data)
    }
  })
})

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
     alert(response.error)
    }
  })
}

$('#id_storages_form').on('submit', function(event){
  event.preventDefault();
  refresh_table();
});

function delayTime(alertObject) {
  delayClass = alertObject.attr('class').split(' ').filter(option => option.startsWith('delay-'))[0]
  if (!delayClass) { return 5000 }

  return Number(delayClass.split('-')[1])
}

$(document).ready(function() {
  $('#alert-box .alert').each(function(_, value) {
    alertObject = $(value)
    delay = delayTime(alertObject)
    alertObject.delay(delay).fadeTo(2000, 500).slideUp(500, function(){
       alertObject.slideUp(500);
    });
  });
});
