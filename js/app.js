var locations = ["fmi-bistro", "ipp-bistro", "mensa-arcisstr", "mensa-garching", "mensa-leopoldstr", "mensa-lothstr", 
                 "mensa-martinsried", "mensa-pasing", "mensa-weihenstephan", "stubistro-arcisstr", "stubistro-goethestr", 
                 "stubistro-großhadern", "stubistro-grosshadern", "stubistro-rosenheim", "stubistro-schellingstr", 
                 "stucafe-adalbertstr", "stucafe-akademie-weihenstephan", "stucafe-boltzmannstr", "stucafe-garching", 
                 "stucafe-karlstr", "stucafe-pasing"];

var root = document.getElementById("app");
var currentLocation = locations[0];

var locationsDropdown = m("div", {class: "dropdown"}, [
                            m("div", {class: "dropdown-trigger"},
                            m("button", {class: "button"},[
                                m("span", "Select Location"),
                                m("span", {class: "icon icon-small"},
                                    m("i", {class: "fa fa-angle-down"}))
                            ])),
                            m("div", {class: "dropdown-menu", role: "menu"},
                                m("div", {class: "dropdown-content"},
                                    locations.map(function(loc) {return m("a", {href: "#", class: "dropdown-item", 
                                                                                onclick: function() {setLocation(loc)}}, loc)})))
                        ]);

m.mount(root, {
    view: function() {
        return m("div", [locationsDropdown, 
                         m("div", {class: "has-text-centered"}, 
                            m("h1", {class: "title"}, currentLocation))]);
    }
});

function setLocation(loc) {
    currentLocation = loc;
}

var dropdown = document.querySelector('.dropdown');
dropdown.addEventListener('click', function(event) {
  event.stopPropagation();
  dropdown.classList.toggle('is-active');
});