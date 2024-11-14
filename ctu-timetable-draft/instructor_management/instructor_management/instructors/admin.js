// Custom JS to handle the time picker
$(document).ready(function() {
  $('input[type="time"]').timepicker({
      timeFormat: 'hh:mm tt',  // 12-hour format with AM/PM
      interval: 30,            // 30-minute intervals
      minTime: '12:00am',
      maxTime: '11:59pm',
      defaultTime: '12',
      startTime: '12:00am',
      dynamic: false,
      dropdown: true,
      scrollbar: true
  });
});
