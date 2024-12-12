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

      if ($('body').hasClass('mobile-nav-active')) {
        $('body').removeClass('mobile-nav-active');
        $('.mobile-nav-overlay').fadeOut();
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

      // Scroll to top
      window.scrollTo(0, 0);

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
  $('body').prepend('<button type="button" class="mobile-nav-toggle d-lg-none"><svg class="icon"><use xlink:href="assets/icons/icons.svg#icon-mobile-menu"></use></svg></button>');
  $('body').append('<div class="mobile-nav-overlay"></div>');

  $(document).on('click', '.mobile-nav-toggle', function (e) {
    $('body').toggleClass('mobile-nav-active');
    $('.mobile-nav-overlay').toggle();
  });

  $(document).click(function (e) {
    var container = $(".mobile-nav, .mobile-nav-toggle");
    if (!container.is(e.target) && container.has(e.target).length === 0) {
      if ($('body').hasClass('mobile-nav-active')) {
        $('body').removeClass('mobile-nav-active');
        $('.mobile-nav-overlay').fadeOut();
      }
    }
  });
} else if ($(".mobile-nav, .mobile-nav-toggle").length) {
  $(".mobile-nav, .mobile-nav-toggle").hide();
}

// Venobox (lightbox feature used in project details)
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

$('.rupee-button').click(function () {
  $('#rupee-audio')[0].play();
});


// --- || JavaScript || ---
window.onload = (event) => {
  //Instantly displays "about" page, simulating a nav click.
  document.getElementsByClassName('about-link')[0].click();
  document.getElementsByClassName('about-link')[1].parentElement.classList.add("active");

  //Handles logic regarding the two profile-pics.
  switchToggleBehaviour();

  footerDateManagement();

  // Sets up the various project categories filters
  setupIsotopes(2)
};

function switchToggleBehaviour() {
  const darkModeToggle = document.getElementById("darkmode-toggle");
  const profilePic = document.getElementById("profile-pic");
  const profilePicSrc = document.getElementById("profile-pic").currentSrc;
  const altProfilePicSrc = document.getElementById("alt-profile-pic").currentSrc;
  const hiddenProfilePicSrc = document.getElementById("hidden-profile-pic").currentSrc;
  const hover = document.getElementById("hovereffect");

  let toggleCounter = 0;
  let toggleCounterLimit = 10;

  darkModeToggle.addEventListener("click", function (event) {
    toggleCounter++;

    if (event.target.checked) {
      if (toggleCounter >= toggleCounterLimit) {
        toggleCounter = 0;
        profilePic.src = hiddenProfilePicSrc;
      } else {
        profilePic.src = altProfilePicSrc;
        hover.classList.add("alt");
      }
    } else {
      profilePic.src = profilePicSrc;
      hover.classList.remove("alt");
    }
  });
}

function footerDateManagement() {
  const updateYear = 2024;
  const dif = new Date().getFullYear() - updateYear;
  const footerString = "Last online " + dif + " years ago | " + updateYear;
  let footers = document.querySelectorAll('.year-dif');

  for (let i = 0; i < footers.length; ++i) {
    footers[i].innerHTML = footerString;
  }
}

function setupIsotopes(ammount) {

  for (let i = 0; i < ammount; ++i) {
    let stringIndex = (i + 1).toString()

    let isotopeRef = new Isotope('.projects-isotope' + stringIndex, {
      itemSelector: '.proj-item' + stringIndex,
      layoutMode: 'fitRows',
      getSortData: { custom: '.custom parseInt', chronological: '.chronological parseInt' }
    });

    let filtersElem = document.querySelectorAll('#filters' + stringIndex + ' li');

    for (let i = 0; i < filtersElem.length; ++i) {
      let filter = filtersElem[i];

      filter.addEventListener('click', function (event) {
        document.querySelector('#filters' + stringIndex + ' .filter-active').classList.remove('filter-active');
        event.target.classList.add('filter-active');

        let sortValue = event.target.getAttribute('data-sort-value');
        let filterValue = event.target.getAttribute('data-filter');

        if (sortValue != undefined) { // Chronological: sort by year and show all 
          isotopeRef.arrange({ sortBy: sortValue });
          isotopeRef.arrange({ filter: "*" });
        } else { // Default: custom sort and show according to filter 
          isotopeRef.arrange({ sortBy: "custom" });
          isotopeRef.arrange({ filter: filterValue });
        }
      });
    }

  }
}
