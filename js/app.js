var locations = ["fmi-bistro", "ipp-bistro", "mensa-arcisstr", "mensa-garching", "mensa-leopoldstr", "mensa-lothstr", 
                 "mensa-martinsried", "mensa-pasing", "mensa-weihenstephan", "stubistro-arcisstr", "stubistro-goethestr", 
                 "stubistro-großhadern", "stubistro-grosshadern", "stubistro-rosenheim", "stubistro-schellingstr", 
                 "stucafe-adalbertstr", "stucafe-akademie-weihenstephan", "stucafe-boltzmannstr", "stucafe-garching", 
                 "stucafe-karlstr", "stucafe-pasing"];

var root = document.getElementById("app");
var currentLocation = locations[0];

var MenuData = {
    menu: null,
    fetch: function() {
            m.request({
                method: "GET",
                // TODO
                url: currentLocation + "/2017/49.json"
            })
            .then(function(menu) {
                MenuData.menu = menu;
            })
        // TODO error handling
        }
}

var LocationsDropdown = {
    view: function() {
        return m("div", {class: "dropdown"}, [
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
                        ])
    }
}

var Day = {
    view: function(vnode) {
        return [vnode.attrs.dishes.map(function(dish) {
            return m("div", dish.name + ": " + dish.price);
        })]
    }
}

var Menu = {
    oninit: MenuData.fetch,
    view: function() {
        return MenuData.menu ? m("div", MenuData.menu.days.map(function(day) {
            return m("div", {style: "margin-bottom: 1em;"}, [
                m("p", m("b", day.date)), 
                m(Day, {dishes: day.dishes})
            ]);
        })) : m("div", "Loading...")
    }
}

var App = {
    view: function() {
        // TODO
        return m("div", [m(LocationsDropdown), 
                         m("div", {class: "has-text-centered"}, 
                            m("h1", {class: "title"}, currentLocation)), m(Menu)]);
    }
}


m.mount(root, App);

function setLocation(loc) {
    currentLocation = loc;
    MenuData.fetch();
}

var dropdown = document.querySelector('.dropdown');
dropdown.addEventListener('click', function(event) {
  event.stopPropagation();
  dropdown.classList.toggle('is-active');
});