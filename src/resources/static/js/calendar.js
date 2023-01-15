const calendar = document.querySelector(".calendar"),
    date = document.querySelector(".date"),
    daysContainer = document.querySelector(".days"),
    prev = document.querySelector(".prev"),
    next = document.querySelector(".next")

let today = new Date()
let activeDay;
let month = today.getMonth()
let year = today.getFullYear()

document.querySelector(".add-event").addEventListener('click', (e) => {
    showAddEvent(0, 0, 0, false);
});

document.getElementById("btnSubmit").addEventListener('click', (e) => {
    let nome = document.getElementById("nomeAddNew").value.length
    let data = document.getElementById("dataAddNew").value.length
    let hora = document.getElementById("HoraAddNew").value.length
    let desc = document.getElementById("descricaoAddNew").value.length

    if (nome == 0 || data == 0 || hora == 0 || desc == 0) {
        alert("Todos os campos devem ser preenchidos");
    } else {
        document.getElementById("formAdd").submit();
    }
});

const months = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro"
]

// const eventsArray = [
//     {
//         day: 8,
//         month: 1,
//         year: 2023
//     },
//     {
//         day: 10,
//         month: 1,
//         year: 2023
//     }
//
//     /*{
//         id: <id>,
//         name: <name>,
//         day: 28,
//         month: 12,
//         year: 2022,
//         time_begin: <time>,
//         time_end: <time>,
//         description: <str>,
//         notification: <bool>,
//     }*/
// ]

function initCalendar() {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const prevLastDay = new Date(year, month, 0)
    const prevDays = prevLastDay.getDate()
    const lastDate = lastDay.getDate()
    const day = firstDay.getDay()
    const firstWeekDay = firstDay.getDay()
    let nextDays

    // Logic to view each month with 6 weeks

    console.log(lastDate)

    if (lastDate == 31) {
        if (firstWeekDay == 5 || firstWeekDay == 6) {
            nextDays = 7 - lastDay.getDay() - 1
        } else {
            nextDays = 14 - lastDay.getDay() - 1
        }
    } else if (lastDate == 30) {
        if (firstWeekDay == 6) {
            nextDays = 7 - lastDay.getDay() - 1
        } else {
            nextDays = 14 - lastDay.getDay() - 1
        }
    } else if (lastDate == 28) {
        const lastWeekDay = lastDay.getDay()
        if (lastWeekDay == 6) {
            nextDays = 21 - lastDay.getDay() - 1
        } else {
            nextDays = 14 - lastDay.getDay() - 1
        }
    } else {
        nextDays = 14 - lastDay.getDay() - 1
    }

    // Update the date at the top of the calendar
    date.innerHTML = months[month] + " " + year

    let days = ""

    // Previous month days
    for (let p = day; p > 0; p--) {
        days += `<div class="day prev-date">${prevDays - p + 1}</div>`
    }

    // Current month days
    for (let c = 1; c <= lastDate; c++) {
        let hasEvent = false

        eventsArray.forEach((eventObj) => {
            if (
                eventObj.day == c &&
                eventObj.month == month + 1 &&
                eventObj.year == year
            ) {
                hasEvent = true
            }
        })

        if (
            c === new Date().getDate() &&
            year == new Date().getFullYear() &&
            month === new Date().getMonth()
        ) {
            if (hasEvent) {
                days += `<div class="day today event" onclick="showCurrentDayevents(${c},${month + 1},${year});">${c}</div>`
            } else {
                days += `<div class="day today" onclick="showCurrentDayevents(${c},${month + 1},${year});">${c}</div>`
            }
        } else {
            if (hasEvent) {
                days += `<div class="day event" onclick="showCurrentDayevents(${c},${month + 1},${year});">${c}</div>`
            } else {
                days += `<div class="day" onclick="showCurrentDayevents(${c},${month + 1},${year});">${c}</div>`
            }
        }
    }

    // Next month days
    for (let n = 1; n <= nextDays; n++) {
        days += `<div class="day next-date">${n}</div>`
    }

    daysContainer.innerHTML = days
}

function getDayEvents(currentDay, currentMonth, currentYear) {
    let dayEvents = [];
    eventsArray.forEach((eventObj) => {
        if (eventObj.day == currentDay &&
            eventObj.month == currentMonth &&
            eventObj.year == currentYear
        ) {
            dayEvents.push(eventObj);
        }
    });
    return dayEvents.sort(sortByTime);
}

function sortByTime(a, b) {
    let timeA = a.time.split(":");
    let timeB = b.time.split(":");

    return new Date(a.year, a.month, a.day, parseInt(timeA[0]), parseInt(timeA[1])).getTime() - new Date(b.year, b.month, b.day, parseInt(timeB[0]), parseInt(timeB[1])).getTime()
}

function showCurrentDayevents(currentDay, currentMonth, currentYear) {
    let modalTitle = document.getElementById("showEventsTitle");
    let page = document.getElementById("eventsList");
    let bntAdd = document.getElementById("btnAdd");
    let events = getDayEvents(currentDay, currentMonth, currentYear);
    let newHtml = ''

    bntAdd.addEventListener('click', (e) => {
        modalvisualizar.hide();
        showAddEvent(currentDay, currentMonth, currentYear, false);
    });

    modalTitle.innerText = `${currentDay} de ${months[currentMonth - 1]} de ${currentYear}`;

    events.forEach((event) => {
        newHtml += `<p>${event.time} - <a href='javascript:showClickedEvent(${event.id});'>${event.name}</a> </p>`;
    });

    if (newHtml.length == 0) {
        newHtml = `<span>Não há eventos para este dia!</span>`
    }

    page.innerHTML = newHtml;
    modalvisualizar.show();
}

function showAddEvent(currentDay, currentMonth, currentYear, edit) {
    if (currentMonth != 0) {
        let currentDate = ''


        if (currentMonth < 10) {
            currentDate = `${currentYear}-0${currentMonth}`;
        } else {
            currentDate = `${currentYear}-${currentMonth}`;
        }

        if (currentDay < 10) {
            currentDate += `-0${currentDay}`;
        } else {
            currentDate += `-${currentDay}`;
        }

        document.getElementById("dataAddNew").value = currentDate;
    } else {
        document.getElementById("dataAddNew").value = '';
    }

    if (edit == true) {
        document.getElementById("addEventTitle").innerText = "Editar Evento";
        document.getElementById("formAdd").action = '/edit_event';
    } else {
        document.getElementById("addEventTitle").innerText = "Novo Evento";
        document.getElementById("formAdd").action = '/create_event';

        document.getElementById("idAddNew").value = "";
        document.getElementById("nomeAddNew").value = "";
        document.getElementById("HoraAddNew").value = "";
        document.getElementById("descricaoAddNew").value = "";
        document.getElementById("notificarAddNew").value = 1;
    }

    modalAdicionar.show();

}

function showEditevent(eventId) {
    let event = getEventById(eventId);
    console.log(event);
    let id = document.getElementById("idAddNew");
    let nome = document.getElementById("nomeAddNew");
    let Hora = document.getElementById("HoraAddNew");
    let descricao = document.getElementById("descricaoAddNew");
    let notificar = document.getElementById("notificarAddNew");

    id.value = event.id;
    nome.value = event.name;
    Hora.value = event.time;
    descricao.value = event.descricao;
    notificar.value = event.notificar == true ? 1 : 0;

    showAddEvent(event.day, event.month, event.year, true);
}

function getEventById(eventId) {
    let event = null;
    eventsArray.forEach((eventObj) => {
        if (eventObj.id == eventId) {
            event = eventObj;
        }
    });
    return event;
}

function showClickedEvent(eventId) {
    let modalTitle = document.getElementById("seeEventTitle");
    var data = document.getElementById("DataSeeEvent");
    var hora = document.getElementById("HoraSeeEvent");
    var descricao = document.getElementById("descriçãoSeeEvent");
    var notificar = document.getElementById("notificarSeeEvent");

    let event = getEventById(eventId);

    console.log(event);

    let currentDate = ''

    if (event.month < 10) {
        currentDate = `${event.day}/0${event.month}/${event.year}`;
    } else {
        currentDate = `${event.day}/${event.month}/${event.year}`;
    }

    document.getElementById("btnEdit").addEventListener('click', (e) => {
        showEditevent(eventId);
    });

    document.getElementById("btnApagar").addEventListener('click', (e) => {
        if (window.confirm("Deseja mesmo apagar?")) {
            document.getElementById("deleteId").value = eventId;
            document.getElementById("formDelete").submit();
        }
    });

    modalTitle.innerText = event.name;
    data.innerText = currentDate;
    hora.innerText = event.time;
    descricao.innerText = event.descricao
    notificar.innerText = event.notificar == true ? 'Sim' : 'Não';

    modalVer.show();
}

function prevMonth() {
    month--;
    if (month < 0) {
        month = 11;
        year--;
    }
    initCalendar()
}

function nextMonth() {
    month++;
    if (month > 11) {
        month = 0
        year++
    }
    initCalendar()
}

prev.addEventListener("click", prevMonth)
next.addEventListener("click", nextMonth)