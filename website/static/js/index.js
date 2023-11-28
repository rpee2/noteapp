// alert banners
function deleteBanner() {
  x = document.getElementById("close-banner");
  x.parentElement.remove();
}

setTimeout(bannerTimeout, 5000);

function bannerTimeout() {
  var banner = document.getElementById("banner");
  if (banner) {
    banner.remove();
  }
}

//dark mode

const darkMode = document.getElementById("js-darkmode");

document.addEventListener("DOMContentLoaded", () => {
  const existingTheme = localStorage.getItem("theme");
  const root = document.documentElement;
  if (existingTheme === "dark") {
    root.setAttribute("data-theme", "dark");
    darkMode.checked = true;
  } else {
    root.setAttribute("data-theme", "light");
    darkMode.checked = false;
  }
});

darkMode.addEventListener("change", () => {
  const existingTheme = localStorage.getItem("theme");
  var newTheme =
    existingTheme === "light" ? (newTheme = "dark") : (newTheme = "light");
  document.documentElement.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme); // key value
});

// sidebar

function removeFilters() {
  const sidebarFilter = document.getElementById("sidebar-form");
  const inputs = sidebarFilter.querySelectorAll("input");
  inputs.forEach((input) => {
    input.checked = false;
  });
}

// for Firefox and unsupported browsers which don't support popover https://developer.mozilla.org/en-US/docs/Web/API/Popover_API/Using
document.addEventListener("DOMContentLoaded", () => {
  const popover = document.getElementById("js-sidebar-popover");
  const popoverButton = document.getElementById("js-popover-button");
  popoverSupported = HTMLElement.prototype.hasOwnProperty("popover");
  if (popoverSupported) {
    if (popoverButton) {
      popover.popover = "auto";
      popoverButton.popoverTargetElement = popover;
      popoverButton.popoverTargetAction = "toggle"; // hide, show are the other actions
      console.log("Popover API supported.");
    } else {
      popover.popover = "auto";
      console.log("Popover not in use.");
      return;
    }
  } else {

    popover.hidden = true;
    const dialog = document.getElementById("js-sidebar-dialog");
    popoverButton.addEventListener("click", () => {
      dialog.showModal();
      // dialog.show(); also works but have to change z-index of dialog for it to show
    });

    // close the dialog when you click outside https://stackoverflow.com/questions/25864259/how-to-close-the-new-html-dialog-tag-by-clicking-on-its-backdrop
    dialog.addEventListener("click", function (event) {
      var rect = dialog.getBoundingClientRect();
      var isInDialog =
        rect.top <= event.clientY &&
        event.clientY <= rect.top + rect.height &&
        rect.left <= event.clientX &&
        event.clientX <= rect.left + rect.width;
      if (!isInDialog) {
        dialog.close();
      }
    });
    console.log("Popover API not supported. We use dialog instead!");
  }
});

// home.html

function deleteNote(event, note_id) {
  // stop the onclick event of the parent card div
  event.stopPropagation();
  
  var csrf_token = document.head.querySelector("meta[name='csrf-token']").getAttribute("content");

  fetch("/delete-note", {
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token,
    },
    method: "POST",
    credentials: "same-origin",
    body: JSON.stringify({ note_id: note_id }),
  }).then((response) => {
    if (response.status === 200) {
      window.location.href = "/";
    } 
  });
}
