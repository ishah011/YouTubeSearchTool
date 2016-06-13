/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown1").classList.toggle("show");
}

function myFunction1() {
    document.getElementById("myDropdown2").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }

  else if(!event.target.matches('#drop1') && event.target.matches('#drop2')){
    if (document.getElementById("myDropdown1").classList.contains('show')) {
      document.getElementById("myDropdown1").classList.toggle("hide");
    }
    if (document.getElementById("myDropdown2").classList.contains('show'))
    {
      document.getElementById("myDropdown2").classList.toggle("hide");
    }
    else{
      myFunction2();
    }
  }

  else if(!event.target.matches('#drop2') && event.target.matches('#drop1')){
    if (document.getElementById("myDropdown2").classList.contains('show')) {
      document.getElementById("myDropdown2").classList.toggle("hide");
    }
    if (document.getElementById("myDropdown1").classList.contains('show'))
    {
      document.getElementById("myDropdown1").classList.toggle("hide");
    }
    else{
      myFunction1();
    }

  }
}