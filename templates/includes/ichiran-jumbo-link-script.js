var jumboLink = document.querySelector(".jumbo-link")
jumboLink.onclick = function(e) {
  if (/{{english_to_romaji[site_name] + "\/ichiran"}}/.test(document.referrer)) {
    history.back();
    return false;
  } else {
    return true;
  }
}