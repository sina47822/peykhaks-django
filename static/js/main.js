var $ = jQuery.noConflict();

// Carousel
$(document).ready(function() {

$('.owl-carousel').owlCarousel({
  loop:true,
  margin:10,
  nav:true,
  responsive:{
      0:{
          items:1
      },
      600:{
          items:3
      },
      1000:{
          items:5
      }
    }
  })
});

// switch price list checked box
$(document).ready(function(){

  $("#flexSwitchCheckChecked").on('change', function() {
    if ($(this).is(':checked')) {
        $('.price-list-beton').attr('style', 'display : block');
        $('.price-list-khak').attr('style', 'display : none');
        $('#flexSwitchCheckCheckedLable').text('برای تغییر لیست از بتن به خاک روی سوییچ کلیک کنید')

    }
    else {
       $('.price-list-beton').attr('style', 'display : none');
       $('.price-list-khak').attr('style', 'display : block');
       $('#flexSwitchCheckCheckedLable').text('برای تغییر لیست از خاک به بتن روی سوییچ کلیک کنید')


    }});
});