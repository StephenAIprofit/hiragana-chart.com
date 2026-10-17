document.querySelectorAll(".dropdown").forEach((box) => {
  const btn = box.querySelector(".nav-btn");
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    box.classList.toggle("open");
  });
});
document.addEventListener("click", () => {
  document.querySelectorAll(".dropdown.open").forEach((el) => el.classList.remove("open"));
});
const hamburger = document.querySelector(".hamburger");
const nav = document.querySelector(".nav-links");
if (hamburger && nav) {
  hamburger.addEventListener("click", () => nav.classList.toggle("open"));
}
const path = location.pathname;
document.querySelectorAll(".nav-links a").forEach((a) => {
  const href = a.getAttribute("href");
  if (href === path || (path === "/" && href.startsWith("/#"))) {
    if (href === path) a.classList.add("active");
  }
});
