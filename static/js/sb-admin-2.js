(function ($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function (e) {
    $('#accordionSidebar').show()
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");

    document.getElementById('accordionSidebar').classList.remove('sidebar-hide')
    document.getElementById('accordionSidebar').classList.add('sidebar-show')

    if ($(".sidebar").hasClass("toggled")) {
      document.getElementById('accordionSidebar').classList.add('sidebar-hide')
      document.getElementById('accordionSidebar').classList.remove('sidebar-show')
      setTimeout(() => { $('#accordionSidebar').hide() }, 200)
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function () {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };

    // Toggle the side navigation when window is resized below 480px
    if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $(".sidebar").addClass("toggled");
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function (e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function () {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function (e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

})(jQuery); // End of use strict

const convertDay = ['Пн.', 'Вт.', 'Ср.', 'Чт.', 'Пт.', 'Сб.', 'Вс.',]
const convertMonth = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Сентября', 'Октября', 'Ноября', 'Декабря',]

let dateToday = new Date()
const date = document.getElementById('dateToDay')
date.innerHTML = dateToday.getDate() + ' ' + convertMonth[dateToday.getMonth()] + ', ' + convertDay[dateToday.getDay()]

$("#datepicker").hide();
$("#datepicker").datepicker({  
  showButtonPanel: true,  
       beforeShow: function( input ) {  
  setTimeout(function() {  
    var buttonPane = $( input )  
      .datepicker( "widget" )  
      .find( ".ui-datepicker-buttonpane" );  
   
    var btn = $('<button type="button" class="ui-datepicker-current ui-state-default ui-priority-secondary ui-corner-all">Clear</button>');  
    btn  
     .unbind("click")  
     .bind("click", function () {  
     $.datepicker._clearDate( input );  
   });  
   
    btn.appendTo( buttonPane );  
   
  }, 1 );  
       }  
 });  

$("#buttonHere").click(function () {
  $("#datepicker").toggle();
});

$("#datepicker").datepicker({
  onSelect: function (value, date) {
    $("#datepicker").hide();
  }
});