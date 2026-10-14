// Mobile menu + contact page "text James" composer. No tracking, no dependencies.
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    });
  }

  var form = document.getElementById("msg");
  if (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var name = form.name.value.trim();
      var err = document.getElementById("m-err");
      if (!name) { err.hidden = false; form.name.focus(); return; }
      err.hidden = true;
      var area = form.area.value === "Not sure yet" ? "the Columbia area" : form.area.value;
      var body = "Hi James, this is " + name + ". I'm looking to " + form.goal.value + " in " + area + ".";
      if (form.note.value.trim()) body += " " + form.note.value.trim();
      var phone = form.querySelector("button[type=submit]").getAttribute("data-phone");
      // "?&body=" works on both iOS and Android messaging apps
      window.location.href = "sms:" + phone + "?&body=" + encodeURIComponent(body);
    });
  }
})();
