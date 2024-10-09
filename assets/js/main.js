// --- || jQuery || ---

// Nav Menu
$(document).on('click', '.nav-menu a, .mobile-nav a', function (e) {
  if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
    var hash = this.hash;
    var target = $(hash);
    if (target.length) {
      e.preventDefault();

      if ($(this).parents('.nav-menu, .mobile-nav').length) {
        $('.nav-menu .active, .mobile-nav .active').removeClass('active');
        $(this).closest('li').addClass('active');
      }

      if (hash == '#header') {
        $('#header').removeClass('header-top');
        $("section").removeClass('section-show');
        return;
      }

      if (!$('#header').hasClass('header-top')) {
        $('#header').addClass('header-top');
        setTimeout(function () {
          $("section").removeClass('section-show');
          $(hash).addClass('section-show');
        }, 350);
      } else {
        $("section").removeClass('section-show');
        $(hash).addClass('section-show');
      }

      if ($('body').hasClass('mobile-nav-active')) {
        $('body').removeClass('mobile-nav-active');
        $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
        $('.mobile-nav-overly').fadeOut();
      }

      return false;
    }
  }
});

// Mobile Navigation
if ($('.nav-menu').length) {
  var mobile_nav = $('.nav-menu').clone().prop({
    class: 'mobile-nav d-lg-none'
  });
  $('body').append(mobile_nav);
  $('body').prepend('<button type="button" class="mobile-nav-toggle d-lg-none"><svg class="icofont-navigation-menu"><use xlink:href="assets/icons/icons.svg#icon-github"></use></svg></i></button>');
  $('body').append('<div class="mobile-nav-overly"></div>');

  $(document).on('click', '.mobile-nav-toggle', function (e) {
    $('body').toggleClass('mobile-nav-active');
    $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
    $('.mobile-nav-overly').toggle();
  });

  $(document).click(function (e) {
    var container = $(".mobile-nav, .mobile-nav-toggle");
    if (!container.is(e.target) && container.has(e.target).length === 0) {
      if ($('body').hasClass('mobile-nav-active')) {
        $('body').removeClass('mobile-nav-active');
        $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
        $('.mobile-nav-overly').fadeOut();
      }
    }
  });
} else if ($(".mobile-nav, .mobile-nav-toggle").length) {
  $(".mobile-nav, .mobile-nav-toggle").hide();
}

// Isotope and filter (tag function on projects section)
$(window).on('load', function () {
  var isotopeRef = $('.projects-isotope').isotope({
    itemSelector: '.projects-item',
    layoutMode: 'fitRows'
  });

  $('#projects-filters li').on('click', function () {
    $("#projects-filters li").removeClass('filter-active');
    $(this).addClass('filter-active');

    isotopeRef.isotope({
      filter: $(this).data('filter')
    });
  });

});

// Initiate venobox when page ready (lightbox feature used in projects)
$(document).ready(function () {
  $('.venobox').venobox();
});

// TLDR Skip button on project details lightbox
$('.tldr-button').click(function () {
  const scrollingElement = (document.scrollingElement || document.body);
  $(scrollingElement).animate({
    scrollTop: document.body.scrollHeight,
  }, 500);
});


// --- || JavaScript || ---

// Custom func that runs on startup.
function loadFunc() {
  //Instantly displays "about" page.
  document.getElementById('proj-link').click();

  //Handles logic regarding the two profile-pics.
  switchToggleBehaviour();

  footerDateManagement();
}

function footerDateManagement() {
  const updateYear = 2024;
  const dif = new Date().getFullYear() - updateYear;
  const footerString = "Last online " + dif + " years ago | " + updateYear;
  document.getElementById("year-dif").innerHTML = footerString;
}

function switchToggleBehaviour() {
  const darkModeToggle = document.getElementById("darkmode-toggle");
  const profilePic = document.getElementById("profile-pic");
  const profilePicSrc = document.getElementById("profile-pic").currentSrc;
  const altProfilePicSrc = document.getElementById("alt-profile-pic").currentSrc;
  const hover = document.getElementById("hovereffect");

  darkModeToggle.addEventListener("click", function (event) {
    if (event.target.checked) {
      hover.classList.add("alt");
      profilePic.src = altProfilePicSrc;
    } else {
      hover.classList.remove("alt");
      profilePic.src = profilePicSrc;
    }
  });
}
