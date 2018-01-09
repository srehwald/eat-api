var locations = ["fmi-bistro", "ipp-bistro", "mensa-arcisstr", "mensa-garching", "mensa-leopoldstr", "mensa-lothstr", 
                 "mensa-martinsried", "mensa-pasing", "mensa-weihenstephan", "stubistro-arcisstr", "stubistro-goethestr", 
                 "stubistro-großhadern", "stubistro-grosshadern", "stubistro-rosenheim", "stubistro-schellingstr", 
                 "stucafe-adalbertstr", "stucafe-akademie-weihenstephan", "stucafe-boltzmannstr", "stucafe-garching", 
                 "stucafe-karlstr", "stucafe-pasing"];

var root = document.getElementById("app");
var currentLocation = locations[0];
var currentWeek = moment(new Date()).week();

var MenuData = {
    menu: null,
    error: "",
    fetch: function() {
            m.request({
                method: "GET",
                url: currentLocation + "/" + (new Date()).getFullYear() + "/" + pad(currentWeek) + ".json"
            })
            .then(function(menu) {
                MenuData.error = "";
                MenuData.menu = menu;
            })
            .catch(function(e) {
                MenuData.error = "Could not load menu."
            })
        }
}

var LocationsDropdown = {
    view: function() {
        return m("div", {class: "dropdown"}, [
                            m("div", {class: "dropdown-trigger"},
                            m("button", {class: "button"},[
                                m("span", currentLocation),
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
            return m("tr", [
                m("td", dish.name),
                m("td", (!isNaN(parseFloat(dish.price)) && isFinite(dish.price)) ? dish.price.toFixed(2) + "€" : dish.price)
            ])
        })]
    }
}

var Menu = {
    oninit: MenuData.fetch,
    view: function() {
        return MenuData.error ? [
            m("div", MenuData.error)
        ] : MenuData.menu ? m("div", 
                              m("table", {class: "table is-hoverable", style: "margin: 0 auto;"}, [
                                m("thead", m("tr", [m("th", "Dish"), m("th", "Price")])),
                                m("tbody", MenuData.menu.days.map(function(day) {
                                    return [
                                        // add id 'today' to today's menu (if exists)
                                        moment(new Date(day.date)).isSame(new Date(), "day") ?
                                            m("tr", {id: "today"}, m("td", {class: "is-light", colspan: "2", style: ""}, m("b", getWeekday(new Date(day.date)) + ", " + day.date))) :
                                            // else
                                            m("tr", m("td", {class: "is-light", colspan: "2", style: ""}, m("b", getWeekday(new Date(day.date)) + ", " + day.date))),
                                        m(Day, {dishes: day.dishes})
                                    ]
                                }))
        ])) 
        : m("div", "Loading...")
    }
}

var App = {
    view: function() {
        return m("div", [m("div", [m(LocationsDropdown), m("a", {class: "button", href: "#today"}, "Today")]), 
                         m("div", {class: "has-text-centered"}, [
                             m("h1", {class: "title"}, currentLocation),
                             m(Menu)
                         ])])
    }
}


m.mount(root, App);

function setLocation(loc) {
    currentLocation = loc;
    MenuData.fetch();
}

function getWeekday(date) {
    // adopted from https://www.w3schools.com/jsref/jsref_getday.asp
    var weekday = new Array(7);
    weekday[0] =  "Sunday";
    weekday[1] = "Monday";
    weekday[2] = "Tuesday";
    weekday[3] = "Wednesday";
    weekday[4] = "Thursday";
    weekday[5] = "Friday";
    weekday[6] = "Saturday";

    return weekday[date.getDay()];
}

// https://stackoverflow.com/questions/8089875/show-a-leading-zero-if-a-number-is-less-than-10
function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}

var dropdown = document.querySelector('.dropdown');
dropdown.addEventListener('click', function(event) {
  event.stopPropagation();
  dropdown.classList.toggle('is-active');
});