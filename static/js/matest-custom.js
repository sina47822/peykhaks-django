/* AVOID USE RIGHT CLICK MOUSE */
//document.addEventListener('contextmenu', event => event.preventDefault());



// Carousel
$("#home-carousel").carousel('pause');
setTimeout(function(){
  $("#home-carousel").carousel({
    interval: 5000
  });
  $("#home-carousel").carousel('cycle');
},500);


// Bootstrap carousel interval 1 min
$('#home-carousel-video.carousel').carousel({
  interval: 58000,
  pause: null
});

// Boostrap carousel on slide, pause video
$('#home-carousel-video.carousel').on('slide.bs.carousel', function () {
  $('#home-carousel-video video').get(0).pause();
});

// Boostrap carousel if slide is video, resume video
$('#home-carousel-video.carousel').on('slid.bs.carousel', function () {
  if ($('#home-carousel-video .item.active video').length > 0) {
    $('#home-carousel-video .item.active video').get(0).play();
  }
});



// Cookie
// document.addEventListener('DOMContentLoaded', function (event) {
//   if (window.location.href.match(/(\/en\/)|(\/es\/)|(\/fr\/)|(\/de\/)/g)) {
//     cookieChoices.showCookieConsentBar('We use cookies to improve your experience on our website. Click on "Read" below to learn more about our cookie policy. By using our services, you agree to our use of cookies in accordance with art. 122 of Legislative Decree 196/2003 as amended by Legislative Decree 69/2012.',
//       'I Accept', 'Read More', '/en/cookie/');
//   } else cookieChoices.showCookieConsentBar('Utilizziamo i cookie per assicurarti una migliore esperienza sul nostro sito. Per maggiori informazioni consulta la nostra cookie policy cliccando su "leggi". Continuando la navigazione sul nostro sito, accetti l\'utilizzo dei cookie ai sensi dell\'art. 122 D.lgs 196/2003 cosÃ¬ come modificato dal D.lgs 69/2012.',
//     'Accetto', 'Leggi', '/en/cookie/');
// });

$(document).ready(function () {
  var videohome = document.getElementById("js-video");
  $("#js-videoAudio").on("click", function (e) {
    videohome.muted = !videohome.muted;
    $(this).toggleClass("is--muted");
  });
  // Video toggle pause
  $("#js-videoPlay").on("click", function (e) {
    if (videohome.paused) {
      videohome.play();
    } else {
      videohome.pause();
    }
  });
});

// Form control
$(document).ready(function ($) {

  window.rec = false;

  setRecaptcha = function() {
      $('.g-recaptcha')
          .each(function(index, el) {
          grecaptcha.render(el, { 
              'sitekey': '6LdMGXMUAAAAALU_EWz-6gXgTtBuynY4r2YH5VIL',
              'callback': verifyCallback,
          });
      });
  };

  function verifyCallback() {;
      window.rec = true;
  }

  $("#form_contact").validate({
    rules: {
      txtContactName: {
        required: true
      },
      txtContactSurname: {
        required: true
      },
      txtContactEmail: {
        required: true
      },
      txtContactPhone: {
        required: true
      },
      txtContactCompany: {
        required: true
      },
      txtContactJob: {
        required: true
      },
      txtContactMessage: {
        required: true
      },
      txtPrivacyform: {
        required: true
      },
      txtPrivacyform2: {
        required: true
      },
      txtAddress: {
        required: true
      },
      txtNation: {
        required: true
      }
    },
    highlight: function (element) {
      $(element).addClass("classe_errore");
    },
    unhighlight: function (element) {
      $(element).removeClass("classe_errore");
    },
    submitHandler: function (form) {
      
      if(window.rec == false) {
        alert("Check reCAPTCHA");
        window.rec = false;
        return false;
      } else {
        
        var glang = $("#form_contact").attr("gdata-lang");
        ga('send', 'event', 'Form info prodotti', 'Pagina contatti' , glang ,1),
        this.submit();
  
      }     
    }
  });


  $("#form_contatti").validate({
    rules: {
      name: {
        required: true
      },
	  surname: {
        required: true
      },
      company: {
        required: true
      },
      email: {
        required: true
      },
      phone: {
        required: true
      },
      address: {
        required: true
      },
      job: {
        required: true
      },
	  nation: {
        required: true
      },
      message: {
        required: true
      },
      privacy: {
        required: true
      }
    },
    highlight: function (element) {
      $(element).addClass("classe_errore");
    },
    unhighlight: function (element) {
      $(element).removeClass("classe_errore");
    },
    submitHandler: function (form) {

      if(window.rec == false) {
        alert("Check reCAPTCHA");
        window.rec = false;
        return false;
      } else {
        
        var gprod = $("#form_contatti_btn").attr("gdata-prod");
        var glang = $("#form_contatti_btn").attr("gdata-lang");

        ga('send', 'event', 'Form info prodotti', gprod , glang ,1),
        form.submit();
  
      }     
      
    }
  });

  $("#main-search").validate({
    rules: {
      addons: {
        required: true,
        minlength: 3
      }
    },
    highlight: function (element) {
      $(element).addClass("classe_errore");
    },
    unhighlight: function (element) {
      $(element).removeClass("classe_errore");
    },
    submitHandler: function (form) {
      var search = $("#main-search");
      var action = search.attr("action");
      var text = $("#txtSearch").val();
      search.attr("action",action + text);
      form.submit();
    }
  });

  $("#mobile-search").validate({
    rules: {
      txtSearch: {
        required: true
      }
    },
    highlight: function (element) {
      $(element).addClass("classe_errore");
    },
    unhighlight: function (element) {
      $(element).removeClass("classe_errore");
    },
    submitHandler: function (form) {
      form.submit();
    }
  });

  

});

// Slider
$(document).ready(function () {
  $('.owl-products').owlCarousel({
    loop: true,
    margin: 30,
    responsiveClass: true,
    autoplay:true,
    autoplayTimeout:3000,
    autoplayHoverPause:true,
    navigation: true,
    dots: false,
    navText: [
      '<img src="/frontend/assets/img/ic-bottom-arrow-sx.svg">',
      '<img src="/frontend/assets/img/ic-bottom-arrow-dx.svg">'
    ],
    stagePadding: 20,
    responsive: {
      0: {
        items: 1,
        nav: true
      },
      600: {
        items: 3,
        nav: true
      },
      1200: {
        items: 3,
        nav: true
      },
      1400: {
        items: 3,
        nav: true
      }
    }
  })
});

// Goto Top
$(document).ready(function () {

  $(window).scroll(function () {
    if ($(this).scrollTop() > 200) {
      $('.go-top').fadeIn(200);
    } else {
      $('.go-top').fadeOut(200);
    }
  });

  $('.go-top').click(function (event) {
    event.preventDefault();

    $('html, body').animate({
      scrollTop: 0
    }, 300);
  })
});


// Sidebar Collapse
$(document).ready(function () {
  var mql = window.matchMedia("screen and (max-width: 1024px)")
  mediaqueryresponse(mql)
  mql.addListener(mediaqueryresponse)

  function mediaqueryresponse(mql) {
    if (mql.matches) {
      $(".sidebar .taber").attr("data-toggle", "collapse");
      $('.sidebar .collapse').collapse("hide");
      $(".footer-toggle .taber").attr("data-toggle", "collapse");
      $('.footer-toggle .collapse').collapse("hide");
    } else {
      $('.sidebar .collapse').collapse("show");
      $(".sidebar [data-toggle='collapse']").removeAttr("data-toggle");
      $('.footer-toggle .collapse').collapse("show");
      $(".footer-toggle [data-toggle='collapse']").removeAttr("data-toggle");
    }
  }
});

$(document).ready(function () {

  var mql = window.matchMedia("screen and (max-width: 767px)")
  mediaqueryresponse(mql)
  mql.addListener(mediaqueryresponse)

  function mediaqueryresponse(mql) {
    if (mql.matches) {
      $('#menu-top').removeClass('in');
    } else {
      $('#menu-top').addClass('in');
    }
  }

  $('.owl-newshome').owlCarousel({
    loop: false,
    margin: 0,
    responsiveClass: true,
    autoplay:true,
    autoplayTimeout:5000,
    autoplayHoverPause:true,
    navigation: false,
    dots: false,
    navText: [
      '<img src="/frontend/assets/img/ic-bottom-arrow-sx.svg">',
      '<img src="/frontend/assets/img/ic-bottom-arrow-dx.svg">'
    ],
    stagePadding: 0,
      responsive: {
          0: {
              items: 1,
              nav: true
          },
          600: {
              items: 1,
              nav: true
          },
          1000: {
              items: 1,
              nav: true
          }
      }
  });


});

/* Line */
$(window).scroll(function() {
  if ($(document).scrollTop() > ($("header").height() + $(".breadcrumb").height())) {
  $('.line.top').addClass('line-fix');
  } else {
  $('.line.top').removeClass('line-fix');
  }
});

/* CHANGE LANGUAGE */
$(window).load(function () {

  var currentLanguage = $("body").attr("lang");

  $(".js-change-lang").click(function(e){
    e.preventDefault(),
    e.stopPropagation();
    var jsLang = $(this).attr("ref");
    var Url = window.location.pathname;

    $.ajax({ 
      type: 'POST', 
      url: "/wservice/reload-different-lang", 
      data: { "method": "reloadDifferentLang", "ChooseLanguage": jsLang, "Url": Url, "CurrentLanguage" : currentLanguage },
    }).done(function(data,status) { 
  
      if (data.status == 'SUCCESS') {
        window.location.replace(data.results);
      }
    });

  });

  $("button.btn-test").click(function(){
    var table = $("#TestTbody");

    if(table.attr("empty") == "1") {
      $("#table-test").slideDown(500),
      $("button.btn-test").hide(),
      $('html, body').animate({
        scrollTop: 0
      }, 300);

      $.ajax({ 
        type: 'POST', 
        url: "/wservice/getTestTable", 
        data: { "method": "getTestTable", "CurrentLanguage" : currentLanguage },
      }).done(function(data,status) { 
        table.html(data),
        table.attr("empty","0");
      });
    } else {

      $("#table-test").slideDown(500),
      $("button.btn-test").hide(),
      $('html, body').animate({
          scrollTop: 0
        }, 300);
    } 
  });

  $(".close-title-test").click(function(){
    $("#table-test").slideUp(500);
    $("button.btn-test").show();
  });

});

/* Collapse History */
$(window).load(function () {

  //open what is selcted in sidebar
  $('.panel-collapse').on('show.bs.collapse', function () {
    $(this).siblings('.panel-heading').addClass('active');
  });
  $('.panel-collapse').on('hide.bs.collapse', function () {
    $(this).siblings('.panel-heading').removeClass('active');
  });

  //bind link in the sidebar
  $('.sidebar-link').click(function (event) {
    var LinkWebNode = $(this).attr("webnode");
    var toast = $(this).attr("href");
    event.preventDefault();
    var call = {};
    call.url = "api_addNewToast";
    call.data = { "method": "api_addNewToast", "Toast" : toast, "IdWebNode" : LinkWebNode };
    if(PHPCall(call)) {
      window.location.href = toast;
    }
  });

  //search in the testTable
  /* $("#searchTestField").on("keyup", function() {

    $("#TestTbody tr").show();
    $("#TestTbody tr.showTest").removeClass('showTest');

    var value = $(this).val();

    $("#TestTbody tr").each(function(index) {
      $row = $(this);
      var id = $row.find("td").text();
      current = $row.attr("jq");
      if (id.toLowerCase().indexOf(value.toLowerCase()) === 0) {
        $("#TestTbody tr[jq='"+ current + "']").addClass("showTest");
      }
    });

    $("#TestTbody tr").hide();
    if($("#TestTbody tr.showTest").length > 0){
      $("#TestTbody tr.showTest").show();
    }

    if(value == "") { $("#TestTbody tr").show(); }


  });*/

  $("#searchTestField").on("keyup", function() {

    $("#TestTbody tr").show();
    $("#TestTbody tr.showTest").removeClass('showTest');

    var value = $(this).val();

    $("#TestTbody tr").each(function(index) {
      $row = $(this);
      current = $row.attr("jq");
      
      $row.find("td").each(function(){
        var id = $(this).text();
        id = id.toLowerCase().split(" ");
        $(id).each(function(a,b){
          if (b.toLowerCase().indexOf(value.toLowerCase()) === 0) {
            $("#TestTbody tr[jq='"+ current + "']").addClass("showTest");
          }
        });
      })
      
      
    });

    $("#TestTbody tr").hide();
    if($("#TestTbody tr.showTest").length > 0){
      $("#TestTbody tr.showTest").show();
    }

    if(value == "") { $("#TestTbody tr").show(); }


  });

});


/* Sidebar Product*/
$('.tree-toggle > .click-toggle').click(function () {
  $(this).parent().toggleClass("label-over").parent().children('ul.tree').toggle(200);
});

$(function(){
  $('.opened').parent().children('ul.tree').toggle();
  $('label.opened').toggleClass("label-over");
});


// BASIC FUNCTIONS -------------------------------------------------
function PHPCall(xx,mode){
  
  var lang = xx.data.Toast.split("/")[1];
  
	var what = { 
		type: 'POST',
		async: false,
		url: '/wservice/' + lang + '/' + xx.url,
		data: xx.data
	};
	
	if (mode){
		what.processData = false;
		what.contentType = false;	
	}

	if(mode == "json"){
		what.contentType = "application/json; charset=utf-8";
		what.dataType = 'json';
	}

	if(mode == "html"){
		what.contentType = "text/plain";
		what.dataType = 'html';
	} 

	$.ajax(what).done(function(data,status) {
		res = false;
		if (data.status == 'SUCCESS') {
			res = data.results;
		}
	});
	//console.log(res);
	return res;
}

function setValidatorUI(obj, type, message) {

  $(obj).parent().removeClass('has-error');
  $(obj).parent().removeClass('has-success');
  $(obj).parent().removeClass('has-warning');
  $(obj).parent().parent().find('.help-block li').removeClass('has-error-message');
  $(obj).parent().parent().find('.help-block li').removeClass('has-success-message');
  $(obj).parent().parent().find('.help-block li').removeClass('has-warning-message');

  switch (type) {
      case 'GENERIC_ERROR':
          $(obj).parent().parent().find('.help-block li').addClass('has-error-message');
          break;
      case 'ERROR':
          $(obj).parent().addClass('has-error');
          $(obj).parent().find('.help-block li').addClass('has-error-message');
          break;
      case 'WARNING':
          $(obj).parent().addClass('has-warning');
          break;
      case 'SUCCESS':
          $(obj).parent().addClass('has-success');
          $(obj).parent().find('.help-block li').addClass('has-success-message');
          break;
  }

  if (message == '') {
      $(obj).parent().parent().find('.help-block').hide();
      $(obj).parent().parent().find('.help-block li').html('');
  }
  else  {
      $(obj).parent().parent().find('.help-block').show();
      $(obj).parent().find('.help-block li').html(message);
  }
}



$("#form_workwithus").validate({
  rules: {
    txtContactName: {
      required: true
    },
    txtContactSurname: {
      required: true
    },
    txtContactEmail: {
      required: true
    },
    txtContactPhone: {
      required: true
    },
    txtContactMessage: {
      required: true
    },
    txtPrivacyform: {
      required: true
    },
    txtContactDomicile: {
      required: true
    },
    WorkwithusCv: {
      required: true
    },
  },
  highlight: function (element) {
    $(element).addClass("classe_errore");
  },
  unhighlight: function (element) {
    $(element).removeClass("classe_errore");
  },
  submitHandler: function (form) {
    
    if(window.rec == false) {
      alert("Check reCAPTCHA");
      window.rec = false;
      return false;
    } else {
      
      //var glang = $("#form_workwithus").attr("gdata-lang");
      //ga('send', 'event', 'Form info prodotti', 'Pagina contatti' , glang ,1),
      
      this.submit();

    }     
  }
});