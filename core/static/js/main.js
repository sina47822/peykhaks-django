var $ = jQuery.noConflict();

// Carousel
// $(document).ready(function () {
// 	var owl = $("#owl-demo-2");
// 	owl.owlCarousel({
// 		autoplay: true,
// 		autoplayTimeout: 1000,
// 		autoplayHoverPause: true,
// 		items: 3,
// 		loop: true,
// 		center: false,
// 		rewind: false,
// 		mouseDrag: true,
// 		touchDrag: true,
// 		pullDrag: true,
// 		freeDrag: false,
// 		margin: 0,
// 		stagePadding: 0,
// 		merge: false,
// 		mergeFit: true,
// 		autoWidth: false,
// 		startPosition: 0,
// 		rtl: true,
// 		smartSpeed: 250,
// 		fluidSpeed: false,
// 		dragEndSpeed: false,
// 		responsive: {
// 			0: {
// 				items: 1
// 				// nav: true
// 			},
// 			480: {
// 				items: 2,
// 				nav: false
// 			},
// 			768: {
// 				items: 3,
// 				// nav: true,
// 				loop: false
// 			},
// 			992: {
// 				items: 4,
// 				// nav: true,
// 				loop: false
// 			}
// 		},
// 		responsiveRefreshRate: 200,
// 		responsiveBaseElement: window,
// 		fallbackEasing: "swing",
// 		info: false,
// 		nestedItemSelector: false,
// 		itemElement: "div",
// 		stageElement: "div",
// 		refreshClass: "owl-refresh",
// 		loadedClass: "owl-loaded",
// 		loadingClass: "owl-loading",
// 		rtlClass: "owl-rtl",
// 		responsiveClass: "owl-responsive",
// 		dragClass: "owl-drag",
// 		itemClass: "owl-item",
// 		stageClass: "owl-stage",
// 		stageOuterClass: "owl-stage-outer",
// 		grabClass: "owl-grab",
// 		autoHeight: false,
// 		lazyLoad: false
// 	});
//   var owl = $("#owl-demo-3");
// 	owl.owlCarousel({
// 		autoplay: true,
// 		autoplayTimeout: 1000,
// 		autoplayHoverPause: true,
// 		items: 3,
// 		loop: true,
// 		center: false,
// 		rewind: false,
// 		mouseDrag: true,
// 		touchDrag: true,
// 		pullDrag: true,
// 		freeDrag: false,
// 		margin: 0,
// 		stagePadding: 0,
// 		merge: false,
// 		mergeFit: true,
// 		autoWidth: false,
// 		startPosition: 0,
// 		rtl: true,
// 		smartSpeed: 250,
// 		fluidSpeed: false,
// 		dragEndSpeed: false,
// 		responsive: {
// 			0: {
// 				items: 1
// 				// nav: true
// 			},
// 			480: {
// 				items: 2,
// 				nav: false
// 			},
// 			768: {
// 				items: 3,
// 				// nav: true,
// 				loop: false
// 			},
// 			992: {
// 				items: 4,
// 				// nav: true,
// 				loop: false
// 			}
// 		},
// 		responsiveRefreshRate: 200,
// 		responsiveBaseElement: window,
// 		fallbackEasing: "swing",
// 		info: false,
// 		nestedItemSelector: false,
// 		itemElement: "div",
// 		stageElement: "div",
// 		refreshClass: "owl-refresh",
// 		loadedClass: "owl-loaded",
// 		loadingClass: "owl-loading",
// 		rtlClass: "owl-rtl",
// 		responsiveClass: "owl-responsive",
// 		dragClass: "owl-drag",
// 		itemClass: "owl-item",
// 		stageClass: "owl-stage",
// 		stageOuterClass: "owl-stage-outer",
// 		grabClass: "owl-grab",
// 		autoHeight: false,
// 		lazyLoad: false
// 	});
// $(".next").click(function () {
//   owl.trigger("owl.next");
// });
// $(".prev").click(function () {
//   owl.trigger("owl.prev");
// });
// });

$(document).ready(function() {
  $("#news-slider").owlCarousel({
      items : 6,
      itemsDesktop:[1199,6],
      itemsDesktopSmall:[980,3],
      itemsMobile : [600,1],
      navigation:true,
      navigationText:["",""],
      pagination:true,
      autoPlay:true,
      rtl: true,
      autoplay:true, 
      autoplayTimeout:6000,
      autoplayHoverPause:true, 
      animateOut: 'fadeOut',

  });
});
$(document).ready(function() {
  $("#news-slider-2").owlCarousel({
      items : 6,
      itemsDesktop:[1199,6],
      itemsDesktopSmall:[980,3],
      itemsMobile : [600,1],
      navigation:true,
      navigationText:["",""],
      pagination:true,
      autoPlay:true,
      rtl: true,
      autoplay:true, 
      autoplayTimeout:4000,    
      autoplayHoverPause:true, 
      animateOut: 'fadeOut',

  });
});

$(document).ready(function(){

   $('.pks_slider').owlCarousel({
    margin:0,
    autoplay:true, 
    autoplayTimeout:1500,    
    autoplayHoverPause:false, 
    animateOut: 'fadeOut',
    // animateIn: 'fadeIn',
    loop:true,   
    nav:false,   
    items: 1,  
    rtl: true,  
     
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